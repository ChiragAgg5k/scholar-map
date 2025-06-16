"""Main module for the project."""

import uuid
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt, Confirm, FloatPrompt
from rich.text import Text
from rich.live import Live
from rich.layout import Layout
from rich.align import Align

from src.mindsdb_manager import MindsDBManager
from src.models.paper import Paper
from src.sample_data_manager import insert_sample_papers
from src.job_manager import JobManager


class ScholarMapCLI:
    """Enhanced CLI interface for Scholar Map"""

    def __init__(self):
        self.console = Console()
        self.manager = MindsDBManager()
        self.job_manager = JobManager(self.manager)
        self.current_context = "main"
        self.papers_to_insert = []

    def clear_screen(self):
        """Clear the terminal screen"""
        self.console.clear()

    def show_header(self):
        """Display the application header"""
        welcome_text = Text("Scholar Map", style="bold blue")
        welcome_panel = Panel(
            welcome_text,
            subtitle="Research Paper Knowledge Management System",
            border_style="blue",
            padding=(0, 2),
        )
        self.console.print(welcome_panel)

    def show_status(self, message: str, style: str = "dim"):
        """Show a status message"""
        self.console.print(f"[{style}]{message}[/{style}]")

    def get_quick_action(self, context: str = "main") -> str:
        """Get next action from user with minimal interface"""
        if context == "main":
            self.console.print("\n[bold cyan]Quick Actions:[/bold cyan]")
            prompt_text = "[bold]Action[/bold] ([dim]i[/dim]nsert, [dim]s[/dim]earch, [dim]d[/dim]emo, [dim]j[/dim]ob, [dim]q[/dim]uit)"
            choices = [
                "i",
                "insert",
                "s",
                "search",
                "d",
                "demo",
                "j",
                "job",
                "q",
                "quit",
            ]
        elif context == "insert":
            if self.papers_to_insert:
                self.console.print(
                    f"\n[dim]📄 {len(self.papers_to_insert)} papers ready to insert[/dim]"
                )
            prompt_text = "[bold]Action[/bold] ([dim]a[/dim]dd, [dim]r[/dim]eview, [dim]i[/dim]nsert, [dim]c[/dim]lear, [dim]b[/dim]ack)"
            choices = [
                "a",
                "add",
                "r",
                "review",
                "i",
                "insert",
                "c",
                "clear",
                "b",
                "back",
            ]
        elif context == "search":
            prompt_text = "[bold]Search[/bold] ([dim]g[/dim]eneral, [dim]f[/dim]ield, [dim]c[/dim]ategory, [dim]a[/dim]uthor, [dim]adv[/dim]anced, [dim]b[/dim]ack)"
            choices = [
                "g",
                "general",
                "f",
                "field",
                "c",
                "category",
                "a",
                "author",
                "adv",
                "advanced",
                "b",
                "back",
            ]
        elif context == "job":
            prompt_text = "[bold]Job Action[/bold] ([dim]c[/dim]reate, [dim]d[/dim]elete, [dim]s[/dim]tatus, [dim]b[/dim]ack)"
            choices = ["c", "create", "d", "delete", "s", "status", "b", "back"]
        else:
            choices = ["b", "back"]
            prompt_text = "[bold]Action[/bold] ([dim]b[/dim]ack)"

        return Prompt.ask(prompt_text, choices=choices, default="b")

    def collect_paper_info(self) -> Paper:
        """Collect paper information from user input with improved UX"""
        self.console.print("\n[bold cyan]📝 New Paper Entry[/bold cyan]")
        self.console.print("[dim]Fill in the details (press Ctrl+C to cancel)[/dim]\n")

        # Generate unique paper ID
        paper_id = str(uuid.uuid4())

        try:
            # Collect required information with streamlined prompts
            title = Prompt.ask("📖 [bold]Title[/bold]")
            authors = Prompt.ask("👥 [bold]Authors[/bold] [dim](comma-separated)[/dim]")

            category = Prompt.ask(
                "🏷️ [bold]Category[/bold]",
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
                    "📅 [bold]Publication Date[/bold] [dim](YYYY-MM-DD or press Enter for today)[/dim]",
                    default=datetime.now().strftime("%Y-%m-%d"),
                )
                try:
                    datetime.strptime(pub_date_str, "%Y-%m-%d")
                    break
                except ValueError:
                    self.console.print(
                        "[red]❌ Invalid date format. Please use YYYY-MM-DD[/red]"
                    )

            arxiv_id = Prompt.ask(
                "🔬 [bold]ArXiv ID[/bold] [dim](optional)[/dim]", default=""
            )
            journal = Prompt.ask(
                "📰 [bold]Journal/Conference[/bold] [dim](optional)[/dim]", default=""
            )

            research_field = Prompt.ask(
                "🔍 [bold]Research Field[/bold]",
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
                "📋 [bold]Paper Type[/bold]",
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
                "📊 [bold]Citation Count[/bold] [dim](optional)[/dim]", default=0
            )

            self.console.print(
                "\n📝 [bold]Abstract[/bold] [dim](Enter text, then press Enter twice when done)[/dim]"
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

        except KeyboardInterrupt:
            self.console.print("\n[yellow]❌ Paper entry cancelled[/yellow]")
            return None

    def handle_insert_papers(self):
        """Handle paper insertion with improved workflow"""
        self.current_context = "insert"

        while True:
            action = self.get_quick_action("insert")

            if action in ["a", "add"]:
                paper = self.collect_paper_info()
                if paper:
                    self.papers_to_insert.append(paper)
                    self.console.print(
                        f"[bold green]✅ Added '[bold]{paper.title}[/bold]'[/bold green]"
                    )

            elif action in ["r", "review"]:
                if not self.papers_to_insert:
                    self.console.print("[yellow]📭 No papers to review[/yellow]")
                    continue

                self.console.print(
                    f"\n[bold cyan]📋 Review Queue ({len(self.papers_to_insert)} papers)[/bold cyan]"
                )
                for i, paper in enumerate(self.papers_to_insert, 1):
                    self.console.print(
                        f"\n[bold blue]{i}.[/bold blue] [bold]{paper.title}[/bold]"
                    )
                    self.console.print(f"   👥 {paper.authors}")
                    self.console.print(
                        f"   🏷️ {paper.category} | 🔍 {paper.research_field}"
                    )
                    self.console.print(f"   📅 {paper.pub_date}")
                    abstract_preview = (
                        paper.abstract[:150] + "..."
                        if len(paper.abstract) > 150
                        else paper.abstract
                    )
                    self.console.print(f"   📝 {abstract_preview}")

            elif action in ["i", "insert"]:
                if not self.papers_to_insert:
                    self.console.print("[yellow]📭 No papers to insert[/yellow]")
                    continue

                self.console.print(
                    f"\n[bold yellow]🚀 Ready to insert {len(self.papers_to_insert)} papers[/bold yellow]"
                )
                if Confirm.ask("Proceed with insertion?", default=True):
                    success = self.manager.insert_papers(self.papers_to_insert)
                    if success:
                        self.papers_to_insert.clear()
                        self.console.print(
                            "[bold green]✅ All papers inserted successfully![/bold green]"
                        )
                    else:
                        self.console.print("[red]❌ Some papers failed to insert[/red]")

            elif action in ["c", "clear"]:
                if self.papers_to_insert and Confirm.ask(
                    f"Clear all {len(self.papers_to_insert)} papers?", default=False
                ):
                    self.papers_to_insert.clear()
                    self.console.print("[yellow]🗑️ Papers cleared[/yellow]")

            elif action in ["b", "back"]:
                if self.papers_to_insert and not Confirm.ask(
                    f"You have {len(self.papers_to_insert)} unsaved papers. Return anyway?",
                    default=False,
                ):
                    continue
                break

    def perform_search(self, search_type: str):
        """Perform different types of searches with streamlined interface"""
        self.console.print(f"\n[bold cyan]🔍 {search_type.title()} Search[/bold cyan]")

        if search_type == "general":
            query = Prompt.ask("💭 [bold]Search query[/bold]")

        elif search_type == "field":
            field_choices = [
                "Machine Learning",
                "Computer Vision",
                "Natural Language Processing",
                "Artificial Intelligence",
                "Data Science",
                "Other",
            ]
            field = Prompt.ask("🔍 [bold]Research field[/bold]", choices=field_choices)
            query = Prompt.ask("💭 [bold]Search query[/bold]")

        elif search_type == "category":
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
            category = Prompt.ask("🏷️ [bold]Category[/bold]", choices=category_choices)
            query = Prompt.ask("💭 [bold]Search query[/bold]")

        elif search_type == "author":
            author = Prompt.ask(
                "👥 [bold]Author name[/bold] [dim](partial match supported)[/dim]"
            )
            query = Prompt.ask("💭 [bold]Search query[/bold]")

        elif search_type == "advanced":
            return self.advanced_search()

        # Common search options
        use_threshold = Confirm.ask("🎯 Set relevance threshold?", default=False)
        threshold = (
            FloatPrompt.ask("📊 Threshold (0.0-1.0)", default=0.3)
            if use_threshold
            else None
        )
        limit = IntPrompt.ask("📑 Max results", default=10)

        # Perform search based on type
        self.show_status(f"Searching...")
        results = []
        try:
            if search_type == "general":
                results = self.manager.search_papers(query, threshold, limit)
            elif search_type == "field":
                results = self.manager.search_by_research_field(
                    query, field, threshold, limit
                )
            elif search_type == "category":
                results = self.manager.search_by_category(
                    query, category, threshold, limit
                )
            elif search_type == "author":
                results = self.manager.search_by_author(query, author, threshold, limit)

            self.manager.display_search_results(results, query)

        except Exception as e:
            self.console.print(f"[red]❌ Search error: {str(e)}[/red]")

    def advanced_search(self):
        """Handle advanced search with multiple filters"""
        self.console.print("\n[bold cyan]🔧 Advanced Search[/bold cyan]")

        query = Prompt.ask("💭 [bold]Search query[/bold]")

        self.console.print("\n[dim]🎛️ Optional filters (press Enter to skip):[/dim]")

        filters = {}

        # Research field filter
        research_field = Prompt.ask(
            "🔍 Research field",
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
            "🏷️ Category",
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
            "📋 Paper type",
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
        min_citations = Prompt.ask("📊 Min citations", default="")
        if min_citations.isdigit():
            filters["citation_count"] = int(min_citations)

        # Search options
        use_threshold = Confirm.ask("🎯 Set relevance threshold?", default=False)
        threshold = (
            FloatPrompt.ask("📊 Threshold (0.0-1.0)", default=0.3)
            if use_threshold
            else None
        )
        limit = IntPrompt.ask("📑 Max results", default=10)

        self.show_status("Performing advanced search...")
        if filters:
            self.show_status(f"Filters: {filters}")

        try:
            results = self.manager.search_papers(query, threshold, limit, **filters)
            self.manager.display_search_results(results, f"{query} (Advanced)")
        except Exception as e:
            self.console.print(f"[red]❌ Search error: {str(e)}[/red]")

    def handle_search_papers(self):
        """Handle paper search with improved workflow"""
        self.current_context = "search"

        while True:
            action = self.get_quick_action("search")

            if action in ["g", "general"]:
                self.perform_search("general")
            elif action in ["f", "field"]:
                self.perform_search("field")
            elif action in ["c", "category"]:
                self.perform_search("category")
            elif action in ["a", "author"]:
                self.perform_search("author")
            elif action in ["adv", "advanced"]:
                self.perform_search("advanced")
            elif action in ["b", "back"]:
                break

    def handle_job_management(self):
        """Handle job management operations"""
        self.current_context = "job"

        while True:
            action = self.get_quick_action("job")

            if action in ["c", "create"]:
                interval = IntPrompt.ask(
                    "⏱️ [bold]Job interval (minutes)[/bold]", default=60
                )
                if Confirm.ask("Create periodic paper insertion job?", default=True):
                    self.job_manager.create_insertion_job(interval)

            elif action in ["d", "delete"]:
                if Confirm.ask("Delete periodic paper insertion job?", default=False):
                    self.job_manager.delete_job()

            elif action in ["s", "status"]:
                self.job_manager.display_job_status()

            elif action in ["b", "back"]:
                break

    def run(self):
        """Main application loop with improved UX"""
        try:
            # Initial setup
            self.clear_screen()
            self.show_header()

            self.show_status("Connecting to MindsDB...")
            if self.manager.connect() is False:
                return

            self.show_status("✅ Connected successfully")

            # Main application loop
            while True:
                action = self.get_quick_action("main")

                if action in ["i", "insert"]:
                    self.handle_insert_papers()
                elif action in ["s", "search"]:
                    self.handle_search_papers()
                elif action in ["d", "demo"]:
                    self.console.print(
                        "\n[bold cyan]🎯 Loading sample data...[/bold cyan]"
                    )
                    try:
                        insert_sample_papers(self.manager)
                    except Exception as e:
                        self.console.print(f"[red]❌ Error: {str(e)}[/red]")
                elif action in ["j", "job"]:
                    self.handle_job_management()
                elif action in ["q", "quit"]:
                    self.console.print(
                        "\n[bold green]👋 Thank you for using Scholar Map![/bold green]"
                    )
                    break

        except KeyboardInterrupt:
            self.console.print("\n\n[yellow]👋 Application interrupted[/yellow]")
            self.console.print(
                "[bold green]Thank you for using Scholar Map![/bold green]"
            )


if __name__ == "__main__":
    app = ScholarMapCLI()
    app.run()
