"""Main module for the project."""

import uuid
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt, Confirm, FloatPrompt
from rich.text import Text

from src.mindsdb_manager import MindsDBManager
from src.models.paper import Paper
from src.sample_data_manager import insert_sample_papers


def collect_paper_info(cli: Console) -> Paper:
    """Collect paper information from user input"""
    cli.print("[bold cyan]Enter Paper Information[/bold cyan]")
    cli.print("[dim]Please provide the following details for the research paper:[/dim]")
    cli.print()

    # Generate unique paper ID
    paper_id = str(uuid.uuid4())

    # Collect required information
    title = Prompt.ask("[bold]Paper Title[/bold]")
    authors = Prompt.ask("[bold]Authors[/bold] [dim](comma-separated)[/dim]")
    category = Prompt.ask(
        "[bold]Category[/bold]",
        choices=[
            "cs.AI",
            "cs.LG",
            "cs.CV",
            "cs.CL",
            "cs.IR",
            "cs.NE",
            "physics",
            "math",
            "biology",
            "other",
        ],
        default="other",
    )

    # Date input with validation
    while True:
        pub_date_str = Prompt.ask(
            "[bold]Publication Date[/bold] [dim](YYYY-MM-DD)[/dim]",
            default=datetime.now().strftime("%Y-%m-%d"),
        )
        try:
            datetime.strptime(pub_date_str, "%Y-%m-%d")
            break
        except ValueError:
            cli.print("[red]Invalid date format. Please use YYYY-MM-DD format.[/red]")

    arxiv_id = Prompt.ask("[bold]ArXiv ID[/bold] [dim](optional)[/dim]", default="")
    journal = Prompt.ask(
        "[bold]Journal/Conference[/bold] [dim](optional)[/dim]", default=""
    )
    research_field = Prompt.ask(
        "[bold]Research Field[/bold]",
        choices=[
            "Machine Learning",
            "Computer Vision",
            "Natural Language Processing",
            "Artificial Intelligence",
            "Data Science",
            "Other",
        ],
        default="Other",
    )
    paper_type = Prompt.ask(
        "[bold]Paper Type[/bold]",
        choices=[
            "Research Paper",
            "Review Paper",
            "Conference Paper",
            "Journal Article",
            "Preprint",
            "Other",
        ],
        default="Research Paper",
    )

    citation_count = IntPrompt.ask(
        "[bold]Citation Count[/bold] [dim](optional)[/dim]", default=0
    )

    cli.print(
        "\n[bold]Abstract[/bold] [dim](Enter the abstract, press Enter twice when done)[/dim]"
    )
    abstract_lines = []
    while True:
        line = input()
        if line.strip() == "":
            if abstract_lines and abstract_lines[-1].strip() == "":
                break
            abstract_lines.append(line)
        else:
            abstract_lines.append(line)

    abstract = "\n".join(abstract_lines).strip()

    return Paper(
        paper_id=paper_id,
        title=title,
        authors=authors,
        category=category,
        pub_date=pub_date_str,
        arxiv_id=arxiv_id,
        journal=journal,
        research_field=research_field,
        paper_type=paper_type,
        citation_count=citation_count,
        abstract=abstract,
    )


def insert_papers_menu(db_manager: MindsDBManager, cli: Console):
    """Handle the paper insertion menu and workflow"""
    papers_to_insert = []

    try:
        while True:
            cli.print()
            insert_menu_text = """[bold cyan]Paper Insertion Options:[/bold cyan]

[bold white]1.[/bold white] Add New Paper
[bold white]2.[/bold white] Review Papers to Insert ([bold cyan]{count}[/bold cyan] papers)
[bold white]3.[/bold white] Insert All Papers into Knowledge Base
[bold white]4.[/bold white] Clear All Papers
[bold white]5.[/bold white] Return to Main Menu""".format(
                count=len(papers_to_insert)
            )

            insert_panel = Panel(
                insert_menu_text,
                title="Paper Insertion",
                border_style="cyan",
                padding=(1, 2),
            )
            cli.print(insert_panel)

            choice = Prompt.ask(
                "Please select an option",
                choices=["1", "2", "3", "4", "5"],
                default="5",
            )

            if choice == "1":
                cli.print()
                try:
                    paper = collect_paper_info(cli)
                    papers_to_insert.append(paper)
                    cli.print(
                        f"[bold green]✓[/bold green] Paper '[bold]{paper.title}[/bold]' added successfully!"
                    )

                    if Confirm.ask(
                        "\nWould you like to add another paper?", default=True
                    ):
                        continue

                except KeyboardInterrupt:
                    cli.print("\n[yellow]Paper addition cancelled.[/yellow]")
                except Exception as e:
                    cli.print(f"[red]Error adding paper: {str(e)}[/red]")

            elif choice == "2":
                if not papers_to_insert:
                    cli.print(
                        "[yellow]No papers to review. Please add papers first.[/yellow]"
                    )
                    continue

                cli.print(
                    f"\n[bold cyan]Review Papers ({len(papers_to_insert)} papers):[/bold cyan]"
                )
                for i, paper in enumerate(papers_to_insert, 1):
                    review_panel = Panel(
                        f"[bold]Title:[/bold] {paper.title}\n"
                        f"[bold]Authors:[/bold] {paper.authors}\n"
                        f"[bold]Category:[/bold] {paper.category}\n"
                        f"[bold]Research Field:[/bold] {paper.research_field}\n"
                        f"[bold]Publication Date:[/bold] {paper.pub_date}\n"
                        f"[bold]Abstract:[/bold] {paper.abstract[:200]}{'...' if len(paper.abstract) > 200 else ''}",
                        title=f"Paper {i}",
                        border_style="blue",
                        padding=(1, 2),
                    )
                    cli.print(review_panel)

            elif choice == "3":
                if not papers_to_insert:
                    cli.print(
                        "[yellow]No papers to insert. Please add papers first.[/yellow]"
                    )
                    continue

                cli.print(
                    f"\n[bold yellow]Ready to insert {len(papers_to_insert)} papers into the knowledge base.[/bold yellow]"
                )
                if Confirm.ask(
                    "Do you want to proceed with the insertion?", default=True
                ):
                    success = db_manager.insert_papers(papers_to_insert)
                    if success:
                        papers_to_insert.clear()
                        cli.print(
                            "[bold green]All papers have been successfully inserted![/bold green]"
                        )
                    else:
                        cli.print(
                            "[red]Some papers failed to insert. Please check the error messages above.[/red]"
                        )

            elif choice == "4":
                if papers_to_insert and Confirm.ask(
                    f"Are you sure you want to clear all {len(papers_to_insert)} papers?",
                    default=False,
                ):
                    papers_to_insert.clear()
                    cli.print("[yellow]All papers cleared.[/yellow]")

            elif choice == "5":
                if papers_to_insert:
                    if not Confirm.ask(
                        f"You have {len(papers_to_insert)} papers that haven't been inserted. Are you sure you want to return to the main menu?",
                        default=False,
                    ):
                        continue
                break
    except KeyboardInterrupt:
        cli.print("\n[yellow]Returning to main menu (Ctrl+C pressed)[/yellow]")


def search_papers_menu(db_manager: MindsDBManager, cli: Console):
    """Handle the paper search menu and workflow"""
    try:
        while True:
            cli.print()
            search_menu_text = """[bold cyan]Paper Search Options:[/bold cyan]

[bold white]1.[/bold white] General Search (Natural Language)
[bold white]2.[/bold white] Search by Research Field
[bold white]3.[/bold white] Search by Category
[bold white]4.[/bold white] Search by Author
[bold white]5.[/bold white] Advanced Search with Filters
[bold white]6.[/bold white] Return to Main Menu"""

            search_panel = Panel(
                search_menu_text,
                title="Search Papers",
                border_style="magenta",
                padding=(1, 2),
            )
            cli.print(search_panel)

            choice = Prompt.ask(
                "Please select a search option",
                choices=["1", "2", "3", "4", "5", "6"],
                default="6",
            )

            if choice == "1":
                # General search
                query = Prompt.ask("\n[bold]Enter your search query[/bold]")

                # Optional relevance threshold
                use_threshold = Confirm.ask(
                    "Set minimum relevance threshold?", default=False
                )
                threshold = None
                if use_threshold:
                    threshold = FloatPrompt.ask(
                        "Relevance threshold (0.0-1.0)", default=0.3
                    )

                # Optional result limit
                limit = IntPrompt.ask("Maximum results to show", default=10)

                cli.print(f"\n[dim]Searching for: '{query}'...[/dim]")
                results = db_manager.search_papers(
                    query, relevance_threshold=threshold, limit=limit
                )
                db_manager.display_search_results(results, query)

            elif choice == "2":
                # Search by research field
                field_choices = [
                    "Machine Learning",
                    "Computer Vision",
                    "Natural Language Processing",
                    "Artificial Intelligence",
                    "Data Science",
                    "Other",
                ]

                field = Prompt.ask(
                    "\n[bold]Select research field[/bold]", choices=field_choices
                )
                query = Prompt.ask("[bold]Enter search query for this field[/bold]")

                use_threshold = Confirm.ask(
                    "Set minimum relevance threshold?", default=False
                )
                threshold = None
                if use_threshold:
                    threshold = FloatPrompt.ask(
                        "Relevance threshold (0.0-1.0)", default=0.3
                    )

                limit = IntPrompt.ask("Maximum results to show", default=10)

                cli.print(f"\n[dim]Searching for '{query}' in {field}...[/dim]")
                results = db_manager.search_by_research_field(
                    query, field, threshold, limit
                )
                db_manager.display_search_results(results, f"{query} (Field: {field})")

            elif choice == "3":
                # Search by category
                category_choices = [
                    "cs.AI",
                    "cs.LG",
                    "cs.CV",
                    "cs.CL",
                    "cs.IR",
                    "cs.NE",
                    "physics",
                    "math",
                    "biology",
                    "other",
                ]

                category = Prompt.ask(
                    "\n[bold]Select category[/bold]", choices=category_choices
                )
                query = Prompt.ask("[bold]Enter search query for this category[/bold]")

                use_threshold = Confirm.ask(
                    "Set minimum relevance threshold?", default=False
                )
                threshold = None
                if use_threshold:
                    threshold = FloatPrompt.ask(
                        "Relevance threshold (0.0-1.0)", default=0.3
                    )

                limit = IntPrompt.ask("Maximum results to show", default=10)

                cli.print(
                    f"\n[dim]Searching for '{query}' in category {category}...[/dim]"
                )
                results = db_manager.search_by_category(
                    query, category, threshold, limit
                )
                db_manager.display_search_results(
                    results, f"{query} (Category: {category})"
                )

            elif choice == "4":
                # Search by author
                author = Prompt.ask(
                    "\n[bold]Enter author name (partial match supported)[/bold]"
                )
                query = Prompt.ask("[bold]Enter search query[/bold]")

                use_threshold = Confirm.ask(
                    "Set minimum relevance threshold?", default=False
                )
                threshold = None
                if use_threshold:
                    threshold = FloatPrompt.ask(
                        "Relevance threshold (0.0-1.0)", default=0.3
                    )

                limit = IntPrompt.ask("Maximum results to show", default=10)

                cli.print(
                    f"\n[dim]Searching for '{query}' by author '{author}'...[/dim]"
                )
                results = db_manager.search_by_author(query, author, threshold, limit)
                db_manager.display_search_results(
                    results, f"{query} (Author: {author})"
                )

            elif choice == "5":
                # Advanced search with multiple filters
                query = Prompt.ask("\n[bold]Enter your search query[/bold]")

                cli.print("\n[bold cyan]Optional Filters:[/bold cyan]")
                cli.print("[dim]Press Enter to skip any filter[/dim]")

                filters = {}

                # Research field filter
                research_field = Prompt.ask(
                    "Research field",
                    choices=[
                        "Machine Learning",
                        "Computer Vision",
                        "Natural Language Processing",
                        "Artificial Intelligence",
                        "Data Science",
                        "Other",
                        "",
                    ],
                    default="",
                )
                if research_field:
                    filters["research_field"] = research_field

                # Category filter
                category = Prompt.ask(
                    "Category",
                    choices=[
                        "cs.AI",
                        "cs.LG",
                        "cs.CV",
                        "cs.CL",
                        "cs.IR",
                        "cs.NE",
                        "physics",
                        "math",
                        "biology",
                        "other",
                        "",
                    ],
                    default="",
                )
                if category:
                    filters["category"] = category

                # Paper type filter
                paper_type = Prompt.ask(
                    "Paper type",
                    choices=[
                        "Research Paper",
                        "Review Paper",
                        "Conference Paper",
                        "Journal Article",
                        "Preprint",
                        "Other",
                        "",
                    ],
                    default="",
                )
                if paper_type:
                    filters["paper_type"] = paper_type

                # Minimum citation count
                min_citations = Prompt.ask(
                    "Minimum citation count (press Enter to skip)", default=""
                )
                if min_citations.isdigit():
                    filters["citation_count"] = int(min_citations)

                # Relevance threshold
                use_threshold = Confirm.ask(
                    "Set minimum relevance threshold?", default=False
                )
                threshold = None
                if use_threshold:
                    threshold = FloatPrompt.ask(
                        "Relevance threshold (0.0-1.0)", default=0.3
                    )

                limit = IntPrompt.ask("Maximum results to show", default=10)

                cli.print(f"\n[dim]Performing advanced search for: '{query}'...[/dim]")
                if filters:
                    cli.print(f"[dim]Filters: {filters}[/dim]")

                results = db_manager.search_papers(query, threshold, limit, **filters)
                db_manager.display_search_results(results, f"{query} (Advanced)")

            elif choice == "6":
                break

    except KeyboardInterrupt:
        cli.print("\n[yellow]Returning to main menu (Ctrl+C pressed)[/yellow]")


if __name__ == "__main__":
    manager = MindsDBManager()
    console = Console()

    # Display welcome header
    welcome_text = Text("Scholar Map", style="bold blue")
    welcome_panel = Panel(
        welcome_text,
        subtitle="Research Paper Knowledge Management System",
        border_style="blue",
        padding=(1, 2),
    )
    console.print(welcome_panel)

    if manager.connect() is False:
        exit(1)

    try:
        while True:
            console.print()
            menu_text = """[bold cyan]Available Options:[/bold cyan]

[bold white]1.[/bold white] Insert Research Papers
[bold white]2.[/bold white] Insert Sample Papers
[bold white]3.[/bold white] Search Research Papers
[bold white]4.[/bold white] Exit Application"""

            menu_panel = Panel(
                menu_text, title="Main Menu", border_style="cyan", padding=(1, 2)
            )
            console.print(menu_panel)

            choice = Prompt.ask(
                "Please select an option", choices=["1", "2", "3", "4"], default="4"
            )

            if choice == "1":
                insert_papers_menu(manager, console)
            elif choice == "2":
                console.print()
                try:
                    insert_sample_papers(manager)
                except KeyboardInterrupt:
                    console.print(
                        "\n[yellow]Sample data insertion cancelled (Ctrl+C)[/yellow]"
                    )
                except Exception as e:
                    console.print(f"\n[red]Error inserting sample data: {str(e)}[/red]")
            elif choice == "3":
                search_papers_menu(manager, console)
            elif choice == "4":
                console.print()
                console.print(
                    "[bold green]Thank you for using Scholar Map![/bold green]"
                )
                console.print("[dim]Application terminated successfully.[/dim]")
                break
    except KeyboardInterrupt:
        console.print("\n\n[yellow]Application interrupted by user (Ctrl+C)[/yellow]")
        console.print("[bold green]Thank you for using Scholar Map![/bold green]")
        console.print("[dim]Application terminated successfully.[/dim]")
