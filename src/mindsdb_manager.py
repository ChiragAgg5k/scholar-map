"""MindsDB Manager"""
import os
from typing import List
import mindsdb_sdk
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from dotenv import load_dotenv
from models.paper import Paper

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
            self.server = mindsdb_sdk.connect(self.connection_url)
            if self.server.knowledge_bases.research_papers_kb:
                self.research_papers_kb = self.server.knowledge_bases.research_papers_kb
                console.print(
                    "✅ Research papers knowledge base already exists!", style="green"
                )
            else:
                self.create_research_papers_kb()
            console.print("✅ Connected to MindsDB successfully!", style="green")
        except (ConnectionError, TimeoutError, ValueError, OSError) as e:
            console.print(f"❌ Failed to connect to MindsDB: {str(e)}", style="red")
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
                "✅ Created research papers knowledge base successfully!", style="green"
            )
            return True
        except (ConnectionError, TimeoutError, ValueError, OSError) as e:
            console.print(
                f"❌ Failed to create research papers knowledge base: {str(e)}",
                style="red",
            )
            return False

    def insert_papers(self, papers: List[Paper]):
        """Insert papers into the knowledge base"""
        if not papers:
            console.print("⚠️  No papers to insert", style="yellow")
            return False

        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console,
            ) as progress:
                task = progress.add_task(
                    "Inserting papers into knowledge base...", total=len(papers)
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

            console.print(
                f"✅ Successfully inserted {len(papers)} papers!", style="green"
            )
            return True

        except (ConnectionError, TimeoutError, ValueError, OSError) as e:
            console.print(f"❌ Failed to insert papers: {str(e)}", style="red")
            return False
