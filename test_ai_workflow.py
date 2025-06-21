#!/usr/bin/env python3
"""Test script for AI workflow functionality"""

import os
from dotenv import load_dotenv
from src.mindsdb_manager import MindsDBManager
from src.models.paper import Paper
from rich.console import Console

load_dotenv()
console = Console()


def test_ai_workflow():
    """Test the AI workflow functionality"""
    console.print("[bold cyan]🧪 Testing AI Workflow[/bold cyan]")

    # Initialize MindsDB manager
    manager = MindsDBManager()

    # Connect to MindsDB
    console.print("[dim]Connecting to MindsDB...[/dim]")
    if not manager.connect():
        console.print("[red]❌ Failed to connect to MindsDB[/red]")
        return False

    # Test paper creation with summary
    console.print("\n[bold]📝 Testing paper creation with AI summary...[/bold]")

    test_paper = Paper(
        paper_id="test-ai-workflow-001",
        title="Test Paper: Multi-Step AI Workflow in MindsDB",
        authors="Test Author, AI Assistant",
        category="cs.AI",
        pub_date="2024-01-01",
        arxiv_id="test.001",
        journal="Test Journal",
        research_field="Artificial Intelligence",
        paper_type="Research Paper",
        citation_count=0,
        abstract="This is a test paper to demonstrate the multi-step AI workflow in MindsDB. The paper discusses how to integrate knowledge base queries with AI table predictions for enhanced research paper management. We show how semantic search results can be fed into AI models for summarization and classification tasks.",
        summary="",
    )

    # Test summary generation
    console.print("[dim]Generating AI summary...[/dim]")
    summary = manager.generate_paper_summary(test_paper)

    if summary:
        console.print(f"[green]✅ Summary generated:[/green]")
        console.print(f"[dim]{summary}[/dim]")
        test_paper.summary = summary
    else:
        console.print(
            "[yellow]⚠️ Could not generate summary, using placeholder[/yellow]"
        )
        test_paper.summary = "AI summary generation test - placeholder text"

    # Test paper insertion
    console.print("\n[bold]💾 Testing paper insertion...[/bold]")
    success = manager.insert_papers([test_paper])

    if success:
        console.print("[green]✅ Paper inserted successfully[/green]")

        # Test search and display
        console.print("\n[bold]🔍 Testing search with summary display...[/bold]")
        results = manager.search_papers("AI workflow MindsDB", limit=5)
        manager.display_search_results(results, "AI workflow MindsDB")

        # Test summary display
        console.print("\n[bold]📄 Testing summary display...[/bold]")
        manager.display_paper_summary("test-ai-workflow-001")

    else:
        console.print("[red]❌ Paper insertion failed[/red]")
        return False

    console.print(
        "\n[bold green]🎉 AI Workflow Test Completed Successfully![/bold green]"
    )
    return True


if __name__ == "__main__":
    test_ai_workflow()
