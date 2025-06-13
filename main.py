"""Main module for the project."""

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.text import Text

from src.mindsdb_manager import MindsDBManager

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

    while True:
        console.print()
        menu_text = """[bold cyan]Available Options:[/bold cyan]

[bold white]1.[/bold white] Insert Research Papers
[bold white]2.[/bold white] Exit Application"""

        menu_panel = Panel(
            menu_text, title="Main Menu", border_style="cyan", padding=(1, 2)
        )
        console.print(menu_panel)

        choice = Prompt.ask("Please select an option", choices=["1", "2"], default="2")

        if choice == "1":
            console.print()
            console.print(
                "[yellow]Paper insertion feature is currently under development.[/yellow]"
            )
            console.print(
                "[dim]This feature will be available in the next update.[/dim]"
            )
            # Here you can call manager.insert_papers() with actual data
        elif choice == "2":
            console.print()
            console.print("[bold green]Thank you for using Scholar Map![/bold green]")
            console.print("[dim]Application terminated successfully.[/dim]")
            break
