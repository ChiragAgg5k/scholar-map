"""Job Manager for MindsDB"""

import os
from datetime import datetime, timedelta
from typing import Optional
from rich.console import Console
from rich.panel import Panel
from faker import Faker
from src.models.paper import Paper
import uuid

console = Console()
fake = Faker()


class JobManager:
    """Manager for MindsDB jobs"""

    def __init__(self, mindsdb_manager):
        self.mindsdb_manager = mindsdb_manager
        self.job_name = "periodic_paper_insertion"
        self.project = None

    def create_insertion_job(self, interval_minutes: int = 60) -> bool:
        """
        Create a job that periodically inserts new papers into the knowledge base.

        Args:
            interval_minutes: Interval in minutes between job executions
        """
        try:
            self.project = self.mindsdb_manager.server.projects.mindsdb

            # Create the job
            job_query = f"""
            CREATE JOB IF NOT EXISTS mindsdb.{self.job_name} AS (
                INSERT INTO research_papers_kb 
                (paper_id, title, authors, category, pub_date, arxiv_id, journal, 
                research_field, paper_type, citation_count, abstract)
                VALUES (
                    '{uuid.uuid4()}' as paper_id,
                    '{fake.sentence()}' as title,
                    '{fake.name()}' as authors,
                    'cs.AI' as category,
                    '{datetime.now().strftime('%Y-%m-%d')}' as pub_date,
                    CONCAT('arxiv:', '{uuid.uuid4()}') as arxiv_id,
                    '{fake.company()}' as journal,
                    'Machine Learning' as research_field,
                    'Research Paper' as paper_type,
                    '{fake.random_int(min=0, max=100)}' as citation_count,
                    '{fake.text(max_nb_chars=500)}' as abstract
                )
            )
            EVERY {interval_minutes} minutes;
            """

            query = self.project.query(job_query)
            result = query.fetch()
            print(result)

            console.print(
                Panel(
                    f"[bold green]✅ Successfully created job '{self.job_name}'[/bold green]\n"
                    f"Job will run every {interval_minutes} minutes to insert new papers.",
                    title="Job Created",
                    border_style="green",
                )
            )
            return True

        except Exception as e:
            console.print(
                Panel(
                    f"[bold red]❌ Failed to create job[/bold red]\n\n"
                    f"Error details: {str(e)}",
                    title="Job Creation Error",
                    border_style="red",
                )
            )
            return False

    def delete_job(self) -> bool:
        """Delete the periodic paper insertion job"""
        try:
            if not self.project:
                self.project = self.mindsdb_manager.server.projects.mindsdb

            delete_query = f"DROP JOB mindsdb.{self.job_name};"
            query = self.project.query(delete_query)
            query.fetch()

            console.print(
                Panel(
                    f"[bold green]✅ Successfully deleted job '{self.job_name}'[/bold green]",
                    title="Job Deleted",
                    border_style="green",
                )
            )
            return True

        except Exception as e:
            console.print(
                Panel(
                    f"[bold red]❌ Failed to delete job[/bold red]\n\n"
                    f"Error details: {str(e)}",
                    title="Job Deletion Error",
                    border_style="red",
                )
            )
            return False

    def get_job_status(self) -> Optional[dict]:
        """Get the status of the periodic paper insertion job"""
        try:
            if not self.project:
                self.project = self.mindsdb_manager.server.projects.mindsdb

            # First try to get from jobs table
            status_query = f"""
            SELECT * FROM mindsdb.jobs 
            WHERE name = '{self.job_name}';
            """

            result = self.project.query(status_query)
            jobs = result.fetch()

            if not jobs.empty:
                return jobs.iloc[0].to_dict()

            # If not found in jobs table, check jobs history
            history_query = f"""
            SELECT * FROM log.jobs_history 
            WHERE project = 'mindsdb' AND name = '{self.job_name}';
            """

            result = self.project.query(history_query)
            history = result.fetch()

            if not history.empty:
                return history.iloc[0].to_dict()

            return None

        except Exception as e:
            console.print(f"[red]Error getting job status: {str(e)}[/red]")
            return None

    def display_job_status(self):
        """Display the current status of the job"""
        status = self.get_job_status()

        if status:
            console.print(
                Panel(
                    f"[bold]Job Name:[/bold] {status.get('name', 'N/A')}\n"
                    f"[bold]Status:[/bold] {status.get('status', 'N/A')}\n"
                    f"[bold]Next Run:[/bold] {status.get('next_run_at', 'N/A')}\n"
                    f"[bold]Last Run:[/bold] {status.get('last_run_at', 'N/A')}",
                    title="Job Status",
                    border_style="blue",
                )
            )
        else:
            console.print(
                Panel(
                    "[yellow]No active job found[/yellow]",
                    title="Job Status",
                    border_style="yellow",
                )
            )
