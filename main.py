"""Main module for the project."""

import uuid
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt, Confirm
from rich.text import Text

from src.mindsdb_manager import MindsDBManager
from src.models.paper import Paper


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
[bold white]2.[/bold white] Exit Application"""

            menu_panel = Panel(
                menu_text, title="Main Menu", border_style="cyan", padding=(1, 2)
            )
            console.print(menu_panel)

            choice = Prompt.ask(
                "Please select an option", choices=["1", "2"], default="2"
            )

            if choice == "1":
                insert_papers_menu(manager, console)
            elif choice == "2":
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
