"""Main module for the project."""
from src.mindsdb_manager import MindsDBManager
from rich.console import Console

if __name__ == "__main__":
    manager = MindsDBManager()
    manager.connect()

    console = Console()
    console.print("Welcome to Scholar Map!", style="bold green")
