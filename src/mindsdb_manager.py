"""MindsDB Manager"""

import os
from typing import List, Optional, Dict, Any, Union
import mindsdb_sdk
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel
from rich.table import Table
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

            try:
                self.research_papers_kb = self.server.knowledge_bases.research_papers_kb
                console.print(
                    "[bold green]Connection established successfully![/bold green]"
                )
                console.print(
                    "[dim]Research papers knowledge base is ready for use.[/dim]"
                )
            except Exception:
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

        if not OPENAI_API_KEY:
            error_panel = Panel(
                f"[bold red]OpenAI API Key Missing[/bold red]\n\n"
                f"The application requires an OpenAI API key to function.\n\n"
                f"[yellow]Please ensure that:[/yellow]\n"
                f"• The OPENAI_API_KEY environment variable is set\n"
                f"• The API key is valid and has not expired\n"
                f"• The .env file is properly configured (if using one)",
                title="Configuration Error",
                border_style="red",
                padding=(1, 2),
            )
            console.print(error_panel)
            raise SystemExit(1)

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
            project = self.server.projects.mindsdb
            query = project.query(kb_query)
            query.fetch()
            self.research_papers_kb = self.server.knowledge_bases.research_papers_kb
            console.print(
                "[bold green]Knowledge base created successfully![/bold green]"
            )
            console.print(
                "[dim]Research papers knowledge base is now ready for use.[/dim]"
            )

            add_index_query = """
            CREATE INDEX ON KNOWLEDGE_BASE research_papers_kb;
            """
            query = project.query(add_index_query)
            query.fetch()

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

    def search_papers(
        self,
        query: str,
        relevance_threshold: Optional[float] = None,
        limit: int = 10,
        **filters,
    ) -> List[Dict[str, Any]]:
        """
        Perform semantic search on research papers using natural language query.

        Args:
            query: Natural language search query
            relevance_threshold: Minimum relevance score (0.0 to 1.0)
            limit: Maximum number of results to return
            **filters: Additional metadata filters (research_field, category, paper_type, etc.)

        Returns:
            List of search results with metadata and relevance scores
        """
        try:
            # Build the WHERE clause
            escaped_query = query.replace("'", "''")
            where_conditions = [f"content = '{escaped_query}' "]

            if relevance_threshold is not None:
                where_conditions.append(f"relevance >= {relevance_threshold}")

            # Add metadata filters
            for key, value in filters.items():
                if key in [
                    "title",
                    "authors",
                    "category",
                    "research_field",
                    "paper_type",
                    "journal",
                ]:
                    escaped_value = str(value).replace("'", "''")
                    where_conditions.append(f"{key} = '{escaped_value}'")
                elif key == "citation_count":
                    where_conditions.append(f"citation_count >= {value}")

            where_clause = " AND ".join(where_conditions)

            search_query = f"""
            SELECT * 
            FROM research_papers_kb 
            WHERE {where_clause}
            ORDER BY relevance DESC
            LIMIT {limit}
            """

            result = self.server.query(search_query)
            return result.fetch()

        except Exception as e:
            console.print(f"[red]Search error: {str(e)}[/red]")
            return []

    def search_by_research_field(
        self,
        query: str,
        field: str,
        relevance_threshold: Optional[float] = None,
        limit: int = 10,
    ) -> List[Dict[str, Any]]:
        """Search papers by specific research field"""
        return self.search_papers(
            query=query,
            relevance_threshold=relevance_threshold,
            limit=limit,
            research_field=field,
        )

    def search_by_category(
        self,
        query: str,
        category: str,
        relevance_threshold: Optional[float] = None,
        limit: int = 10,
    ) -> List[Dict[str, Any]]:
        """Search papers by category"""
        return self.search_papers(
            query=query,
            relevance_threshold=relevance_threshold,
            limit=limit,
            category=category,
        )

    def search_by_author(
        self,
        query: str,
        author: str,
        relevance_threshold: Optional[float] = None,
        limit: int = 10,
    ) -> List[Dict[str, Any]]:
        """Search papers by author (partial match supported)"""
        try:
            escaped_query = query.replace("'", "''")
            escaped_author = author.replace("'", "''")
            where_conditions = [
                f"content = '{escaped_query}' ",
                f"authors LIKE '%{escaped_author}%'",
            ]

            if relevance_threshold is not None:
                where_conditions.append(f"relevance >= {relevance_threshold}")

            where_clause = " AND ".join(where_conditions)

            search_query = f"""
            SELECT * 
            FROM research_papers_kb 
            WHERE {where_clause}
            ORDER BY relevance DESC
            LIMIT {limit}
            """

            result = self.server.query(search_query)
            return result.fetch()

        except Exception as e:
            console.print(f"[red]Author search error: {str(e)}[/red]")
            return []

    def display_search_results(
        self, results: Union[List[Dict[str, Any]], Any], query: str
    ):
        """Display search results in a formatted table"""
        # Handle both DataFrame and list results
        if hasattr(results, "empty"):
            # It's a DataFrame
            if results.empty:
                console.print(
                    f"[yellow]🔍 No results found for query: '{query}'[/yellow]"
                )
                return
            # Convert DataFrame to list of dicts for processing
            results = results.to_dict("records")
        elif not results:
            # It's a list or other iterable
            console.print(f"[yellow]🔍 No results found for query: '{query}'[/yellow]")
            return

        console.print(f"\n[bold cyan]🔍 Search Results for: '{query}'[/bold cyan]")
        console.print(f"[dim]📊 Found {len(results)} matching papers[/dim]\n")

        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Relevance", style="green", width=10)
        table.add_column("Title", style="white", width=40)
        table.add_column("Authors", style="cyan", width=25)
        table.add_column("Field", style="yellow", width=20)
        table.add_column("Category", style="blue", width=10)

        for result in results:
            metadata = result.get("metadata", {})
            if isinstance(metadata, str):
                import json

                try:
                    metadata = json.loads(metadata)
                except:
                    metadata = {}

            relevance = result.get("relevance", 0)
            title = metadata.get("title", "N/A")
            authors = metadata.get("authors", "N/A")
            research_field = metadata.get("research_field", "N/A")
            category = metadata.get("category", "N/A")

            # Truncate long text for table display
            title = (title[:37] + "...") if len(title) > 40 else title
            authors = (authors[:22] + "...") if len(authors) > 25 else authors
            research_field = (
                (research_field[:17] + "...")
                if len(research_field) > 20
                else research_field
            )

            table.add_row(f"{relevance:.3f}", title, authors, research_field, category)

        console.print(table)

    def get_paper_details(self, paper_id: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a specific paper"""
        try:
            detail_query = f"""
            SELECT *
            FROM research_papers_kb
            WHERE paper_id = '{paper_id}'
            """

            result = self.server.query(detail_query)
            results = result.fetch()

            return results[0] if results else None

        except Exception as e:
            console.print(f"[red]Error fetching paper details: {str(e)}[/red]")
            return None
