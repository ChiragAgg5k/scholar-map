"""MindsDB Manager"""

import os
from typing import List
import mindsdb_sdk
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel
from dotenv import load_dotenv
from src.models.paper import Paper

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

console = Console()


class MindsDBManager:
    """
    Manager for MindsDB server.

    Args:
        connection_url: URL of the MindsDB server.

    Attributes:
        server: MindsDB server instance.
    """

    def __init__(self, connection_url: str = None):
        self.connection_url = connection_url or "http://127.0.0.1:47334"
        self.research_papers_kb = None
        self.server = None

    def connect(self):
        """Connect to MindsDB server"""
        try:
            console.print("[dim]Attempting to connect to MindsDB server...[/dim]")
            self.server = mindsdb_sdk.connect(self.connection_url)

            if self.server.knowledge_bases.research_papers_kb:
                self.research_papers_kb = self.server.knowledge_bases.research_papers_kb
                console.print(
                    "[bold green]Connection established successfully![/bold green]"
                )
                console.print(
                    "[dim]Research papers knowledge base is ready for use.[/dim]"
                )
            else:
                console.print(
                    "[bold green]Connection established successfully![/bold green]"
                )
                console.print(
                    "[yellow]Setting up research papers knowledge base...[/yellow]"
                )
                self.create_research_papers_kb()

        except (ConnectionError, TimeoutError, ValueError, OSError) as e:
            error_panel = Panel(
                f"[bold red]Connection Failed[/bold red]\n\n"
                f"Unable to connect to MindsDB server at {self.connection_url}\n\n"
                f"[dim]Error details: {str(e)}[/dim]\n\n"
                f"[yellow]Please ensure that:[/yellow]\n"
                f"• MindsDB server is running\n"
                f"• The connection URL is correct\n"
                f"• Network connectivity is available",
                title="Connection Error",
                border_style="red",
                padding=(1, 2),
            )
            console.print(error_panel)
            return False

    def create_research_papers_kb(self):
        """Create research papers knowledge base"""
        try:
            kb_query = f"""
            CREATE KNOWLEDGE_BASE research_papers_kb
            USING
                embedding_model = {
                    "provider": "openai",
                    "model_name" : "text-embedding-3-large",
                    "api_key": "{OPENAI_API_KEY}"
                },
                reranking_model = {
                    "provider": "openai",
                    "model_name": "gpt-4o",
                    "api_key": "{OPENAI_API_KEY}"
                },
                metadata_columns = [
                    'title', 
                    'authors', 
                    'category', 
                    'pub_date', 
                    'arxiv_id', 
                    'journal',
                    'research_field',
                    'paper_type',
                    'citation_count'
                ],
                content_columns = ['abstract', 'full_text'],
                id_column = 'paper_id';
            """
            self.server.query(kb_query)
            self.research_papers_kb = self.server.knowledge_bases.research_papers_kb
            console.print(
                "[bold green]Knowledge base created successfully![/bold green]"
            )
            console.print(
                "[dim]Research papers knowledge base is now ready for use.[/dim]"
            )
            return True
        except (ConnectionError, TimeoutError, ValueError, OSError) as e:
            error_panel = Panel(
                f"[bold red]Knowledge Base Creation Failed[/bold red]\n\n"
                f"Unable to create the research papers knowledge base.\n\n"
                f"[dim]Error details: {str(e)}[/dim]\n\n"
                f"[yellow]Please check:[/yellow]\n"
                f"• OpenAI API key configuration\n"
                f"• MindsDB server permissions\n"
                f"• Network connectivity",
                title="Setup Error",
                border_style="red",
                padding=(1, 2),
            )
            console.print(error_panel)
            return False

    def insert_papers(self, papers: List[Paper]):
        """Insert papers into the knowledge base"""
        if not papers:
            console.print("[yellow]No papers provided for insertion.[/yellow]")
            return False

        try:
            console.print(
                f"[bold cyan]Preparing to insert {len(papers)} papers...[/bold cyan]"
            )

            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console,
            ) as progress:
                task = progress.add_task(
                    "Processing and inserting papers into knowledge base...",
                    total=len(papers),
                )

                for paper in papers:
                    insert_query = f"""
                    INSERT INTO research_papers_kb 
                    (paper_id, title, authors, category, pub_date, arxiv_id, journal, research_field, paper_type, citation_count, abstract)
                    VALUES (
                        '{paper.paper_id}',
                        '{paper.title.replace("'", "''")}',
                        '{paper.authors.replace("'", "''")}',
                        '{paper.category}',
                        '{paper.pub_date}',
                        '{paper.arxiv_id}',
                        '{paper.journal.replace("'", "''")}',
                        '{paper.research_field}',
                        '{paper.paper_type}',
                        {paper.citation_count},
                        '{paper.abstract.replace("'", "''")}'
                    )
                    """

                    self.server.query(insert_query)
                    progress.advance(task)

            success_panel = Panel(
                f"[bold green]Papers Inserted Successfully[/bold green]\n\n"
                f"Successfully processed and inserted {len(papers)} research papers into the knowledge base.\n\n"
                f"[dim]The papers are now available for search and analysis.[/dim]",
                title="Operation Complete",
                border_style="green",
                padding=(1, 2),
            )
            console.print(success_panel)
            return True

        except (ConnectionError, TimeoutError, ValueError, OSError) as e:
            error_panel = Panel(
                f"[bold red]Paper Insertion Failed[/bold red]\n\n"
                f"An error occurred while inserting papers into the knowledge base.\n\n"
                f"[dim]Error details: {str(e)}[/dim]\n\n"
                f"[yellow]Please verify:[/yellow]\n"
                f"• Database connectivity\n"
                f"• Paper data format\n"
                f"• Knowledge base availability",
                title="Insertion Error",
                border_style="red",
                padding=(1, 2),
            )
            console.print(error_panel)
            return False
