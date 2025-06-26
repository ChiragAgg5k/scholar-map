"""Main module for the project."""

import uuid
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt, Confirm, FloatPrompt
from rich.text import Text
from rich.table import Table
import json

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
            prompt_text = "[bold]Action[/bold] ([dim]i[/dim]nsert, [dim]s[/dim]earch, [dim]a[/dim]i, [dim]ag[/dim]ent, [dim]d[/dim]emo, [dim]j[/dim]ob, [dim]q[/dim]uit)"
            choices = [
                "i",
                "insert",
                "s",
                "search",
                "a",
                "ai",
                "ag",
                "agent",
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
        elif context == "ai":
            prompt_text = "[bold]AI Features[/bold] ([dim]s[/dim]ummary, [dim]g[/dim]enerate, [dim]b[/dim]ack)"
            choices = ["s", "summary", "g", "generate", "b", "back"]
        elif context == "agent":
            prompt_text = "[bold]Agent[/bold] ([dim]c[/dim]hat, [dim]l[/dim]ist, [dim]d[/dim]elete, [dim]r[/dim]ecreate, [dim]b[/dim]ack)"
            choices = [
                "c",
                "chat",
                "l",
                "list",
                "d",
                "delete",
                "r",
                "recreate",
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

    def handle_ai_features(self):
        """Handle AI-related features"""
        self.current_context = "ai"

        while True:
            action = self.get_quick_action("ai")

            if action in ["s", "summary"]:
                self.view_paper_summary()
            elif action in ["g", "generate"]:
                self.generate_summary_for_paper()
            elif action in ["b", "back"]:
                break

    def handle_agent_features(self):
        """Handle agent-related features"""
        self.current_context = "agent"

        while True:
            action = self.get_quick_action("agent")

            if action in ["c", "chat"]:
                self.chat_with_agent()
            elif action in ["l", "list"]:
                self.list_agents()
            elif action in ["d", "delete"]:
                self.delete_agent()
            elif action in ["r", "recreate"]:
                self.recreate_agent()
            elif action in ["b", "back"]:
                break

    def chat_with_agent(self):
        """Interactive chat with the research papers agent"""
        self.console.print("\n[bold cyan]🤖 Research Papers Agent Chat[/bold cyan]")
        self.console.print(
            "[dim]Ask questions about research papers, trends, authors, or topics.[/dim]"
        )
        self.console.print("[dim]Type 'quit' to exit the chat.[/dim]\n")

        while True:
            try:
                question = Prompt.ask("💭 [bold]Your question[/bold]")

                if question.lower() in ["quit", "exit", "q"]:
                    break

                if not question.strip():
                    continue

                self.console.print("\n[dim]🤖 Agent is thinking...[/dim]")

                # Query the agent
                answer = self.manager.query_agent(question)

                # Display the answer in a formatted panel
                answer_panel = Panel(
                    answer,
                    title="🤖 Agent Response",
                    border_style="green",
                    padding=(1, 2),
                    width=80,
                )
                self.console.print(answer_panel)
                self.console.print()

            except KeyboardInterrupt:
                self.console.print("\n[yellow]Chat interrupted[/yellow]")
                break
            except Exception as e:
                self.console.print(f"[red]Error: {str(e)}[/red]")

    def list_agents(self):
        """List all available agents"""
        self.console.print("\n[bold cyan]📋 Available Agents[/bold cyan]")

        try:
            agents = self.manager.list_agents()

            if not agents:
                self.console.print("[yellow]No agents found.[/yellow]")
                return

            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("Name", style="cyan", width=30)
            table.add_column("Model", style="green", width=20)
            table.add_column("Status", style="yellow", width=15)

            for agent in agents:
                name = agent.get("name", "N/A")
                model = agent.get("model", "N/A")
                status = agent.get("status", "N/A")

                table.add_row(name, model, status)

            self.console.print(table)

        except Exception as e:
            self.console.print(f"[red]Error listing agents: {str(e)}[/red]")

    def delete_agent(self):
        """Delete an agent"""
        self.console.print("\n[bold cyan]🗑️ Delete Agent[/bold cyan]")

        try:
            agents = self.manager.list_agents()

            if not agents:
                self.console.print("[yellow]No agents found to delete.[/yellow]")
                return

            # Show available agents
            self.console.print("[bold]Available agents:[/bold]")
            for i, agent in enumerate(agents, 1):
                name = agent.get("name", "N/A")
                self.console.print(f"{i}. {name}")

            # Let user select agent to delete
            choice = IntPrompt.ask(
                "📋 [bold]Select agent number to delete[/bold]", default=1
            )

            if 1 <= choice <= len(agents):
                selected_agent = agents[choice - 1]
                agent_name = selected_agent.get("name", "")

                if Confirm.ask(f"Delete agent '{agent_name}'?", default=False):
                    success = self.manager.delete_agent(agent_name)
                    if success:
                        self.console.print(
                            f"[bold green]✅ Agent '{agent_name}' deleted successfully![/bold green]"
                        )
                    else:
                        self.console.print(
                            f"[red]❌ Failed to delete agent '{agent_name}'[/red]"
                        )
            else:
                self.console.print("[red]❌ Invalid selection.[/red]")

        except Exception as e:
            self.console.print(f"[red]Error deleting agent: {str(e)}[/red]")

    def recreate_agent(self):
        """Recreate the research papers agent"""
        self.console.print("\n[bold cyan]🔄 Recreate Research Papers Agent[/bold cyan]")

        if Confirm.ask("Recreate the research papers agent?", default=False):
            try:
                # First try to delete existing agent
                try:
                    self.manager.delete_agent("research_papers_agent")
                except:
                    pass  # Agent might not exist

                # Create new agent
                success = self.manager.create_research_agent()
                if success:
                    self.console.print(
                        "[bold green]✅ Research papers agent recreated successfully![/bold green]"
                    )
                else:
                    self.console.print("[red]❌ Failed to recreate agent[/red]")

            except Exception as e:
                self.console.print(f"[red]Error recreating agent: {str(e)}[/red]")

    def view_paper_summary(self):
        """View AI-generated summary for a specific paper"""
        self.console.print("\n[bold cyan]🤖 View Paper Summary[/bold cyan]")

        # First, let user search for papers
        query = Prompt.ask(
            "💭 [bold]Search for papers[/bold] [dim](to find paper ID)[/dim]"
        )
        limit = IntPrompt.ask("📑 Max results", default=5)

        try:
            results = self.manager.search_papers(query, limit=limit)

            # Handle both DataFrame and list results
            if hasattr(results, "empty"):
                # It's a DataFrame
                if results.empty:
                    self.console.print(
                        "[yellow]❌ No papers found for the search query.[/yellow]"
                    )
                    return
                # Convert DataFrame to list of dicts for processing
                results = results.to_dict("records")
            elif not results:
                # It's a list or other iterable
                self.console.print(
                    "[yellow]❌ No papers found for the search query.[/yellow]"
                )
                return

            # Debug: Show the structure of the first result
            if results:
                self.console.print(
                    f"[dim]Debug: First result keys: {list(results[0].keys())}[/dim]"
                )
                self.console.print(
                    f"[dim]Debug: First result structure: {results[0]}[/dim]"
                )

            # Display search results for selection
            self.console.print(f"\n[bold]Found {len(results)} papers:[/bold]")
            for i, result in enumerate(results, 1):
                metadata = result.get("metadata", {})
                if isinstance(metadata, str):
                    try:
                        metadata = json.loads(metadata)
                    except:
                        metadata = {}

                title = metadata.get("title", "N/A")
                authors = metadata.get("authors", "N/A")

                # Try to get paper_id from different possible locations
                paper_id = (
                    result.get("paper_id", "")
                    or result.get("id", "")
                    or metadata.get("paper_id", "")
                )

                self.console.print(f"{i}. [bold]{title}[/bold]")
                self.console.print(f"   👥 {authors}")
                self.console.print(f"   🆔 {paper_id}")
                self.console.print()

            # Let user select a paper
            choice = IntPrompt.ask(
                "📋 [bold]Select paper ID (not number!)[/bold]", default=1
            )
            if 1 <= choice <= len(results):
                selected_paper = results[choice - 1]

                # Try to get paper_id from different possible locations
                metadata = selected_paper.get("metadata", {})
                if isinstance(metadata, str):
                    try:
                        metadata = json.loads(metadata)
                    except:
                        metadata = {}

                paper_id = (
                    selected_paper.get("paper_id", "")
                    or selected_paper.get("id", "")
                    or metadata.get("paper_id", "")
                )

                if paper_id:
                    self.manager.display_paper_summary(paper_id)
                else:
                    self.console.print("[red]❌ Could not retrieve paper ID.[/red]")
            else:
                self.console.print("[red]❌ Invalid selection.[/red]")

        except Exception as e:
            self.console.print(f"[red]❌ Error: {str(e)}[/red]")

    def generate_summary_for_paper(self):
        """Generate AI summary for a specific paper"""
        self.console.print("\n[bold cyan]🤖 Generate AI Summary[/bold cyan]")

        # Let user input paper details manually
        title = Prompt.ask("📖 [bold]Paper title[/bold]")
        authors = Prompt.ask("👥 [bold]Authors[/bold]")
        research_field = Prompt.ask("🔍 [bold]Research field[/bold]")

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

        if not abstract:
            self.console.print(
                "[red]❌ Abstract is required for summary generation.[/red]"
            )
            return

        # Create a temporary paper object for summary generation
        temp_paper = Paper(
            paper_id="temp",
            title=title,
            authors=authors,
            category="temp",
            pub_date="",
            arxiv_id="",
            journal="",
            research_field=research_field,
            paper_type="",
            citation_count=0,
            abstract=abstract,
        )

        try:
            self.console.print("\n[dim]Generating AI summary...[/dim]")
            summary = self.manager.generate_paper_summary(temp_paper)

            if summary:
                self.console.print(
                    f"\n[bold green]🤖 AI-Generated Summary:[/bold green]"
                )
                self.console.print(f"[green]{summary}[/green]")
            else:
                self.console.print(
                    "[yellow]❌ Could not generate summary. Please check your input and try again.[/yellow]"
                )

        except Exception as e:
            self.console.print(f"[red]❌ Error generating summary: {str(e)}[/red]")

    def handle_evaluate_knowledge_base(self):
        """Handle evaluation of the knowledge base via CLI"""
        self.console.print("\n[bold cyan]🧪 Evaluate Knowledge Base[/bold cyan]")
        try:
            kb_name = Prompt.ask("Knowledge base name", default="research_papers_kb")
            test_table = Prompt.ask("Test table (e.g. my_datasource.my_test_table)")
            version = Prompt.ask("Version column or value", default="doc_id")
            from_sql = Prompt.ask(
                "SQL to generate data (from_sql)",
                default="SELECT content FROM my_datasource.my_table",
            )
            count = IntPrompt.ask("Number of rows to generate (count)", default=100)
            evaluate = Confirm.ask("Run evaluation (True/False)?", default=False)
            llm_provider = Prompt.ask("LLM provider", default="openai")
            llm_api_key = Prompt.ask(
                "LLM API key",
                default=OPENAI_API_KEY if "OPENAI_API_KEY" in globals() else "",
            )
            llm_model_name = Prompt.ask("LLM model name", default="gpt-4o")
            save_to = Prompt.ask(
                "Save results to table (e.g. my_datasource.my_result_table)"
            )

            result = self.manager.evaluate_knowledge_base(
                kb_name=kb_name,
                test_table=test_table,
                version=version,
                generate_data={"from_sql": from_sql, "count": count},
                evaluate=evaluate,
                llm_provider=llm_provider,
                llm_api_key=llm_api_key,
                llm_model_name=llm_model_name,
                save_to=save_to,
            )
            self.console.print("[bold green]Evaluation results:[/bold green]")
            self.console.print(result)
        except Exception as e:
            self.console.print(f"[red]Error during evaluation: {str(e)}[/red]")

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
                elif action in ["a", "ai"]:
                    self.handle_ai_features()
                elif action in ["ag", "agent"]:
                    self.handle_agent_features()
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
                elif action in ["eval", "evaluate"]:
                    self.handle_evaluate_knowledge_base()
                elif action in ["q", "quit"]:
                    self.console.print(
                        "\n[bold green]👋 Thank you for using Scholar Map![bold green]"
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
