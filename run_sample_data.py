#!/usr/bin/env python3
"""
Standalone script to insert sample research papers into Scholar Map database.

This script can be run independently to populate the database with sample data
for testing and demonstration purposes.

Usage:
    python run_sample_data.py
"""

import sys
import os

# Add src directory to Python path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from src.sample_data_manager import insert_sample_papers
from src.mindsdb_manager import MindsDBManager
from rich.console import Console
from rich.panel import Panel
from rich.text import Text


def main():
    """Main function to run sample data insertion"""
    console = Console()

    # Display header
    header_text = Text("Scholar Map - Sample Data Installer", style="bold blue")
    header_panel = Panel(
        header_text,
        subtitle="Standalone script to populate the database with sample research papers",
        border_style="blue",
        padding=(1, 2),
    )
    console.print(header_panel)

    # Initialize manager
    manager = MindsDBManager()

    # Connect to database
    console.print("[dim]Connecting to MindsDB...[/dim]")
    if manager.connect() is False:
        console.print(
            "[red]Failed to connect to MindsDB. Please ensure the server is running.[/red]"
        )
        console.print("[yellow]Exiting...[/yellow]")
        return 1

    # Insert sample papers
    try:
        success = insert_sample_papers(manager)
        if success:
            console.print(
                "\n[bold green]✓ Sample data installation completed successfully![/bold green]"
            )
            return 0
        else:
            console.print("\n[red]✗ Sample data installation failed.[/red]")
            return 1
    except KeyboardInterrupt:
        console.print("\n[yellow]Installation cancelled by user (Ctrl+C)[/yellow]")
        return 1
    except Exception as e:
        console.print(f"\n[red]Unexpected error during installation: {str(e)}[/red]")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
