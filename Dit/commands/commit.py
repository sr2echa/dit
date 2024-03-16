import rich_click as click
from rich.console import Console
from rich.text import Text

import Dit.utils.utils as utils

console = Console()

@click.command()
@click.option('-m', '--message', required=True, help='Commit message')
@click.option('-d', '--database', required=True, help='Database name')
def cli(message, database):
    """Commit your database changes
    
    Store your changes in the database to version control the current state.
    
    usage : dit commit -m "message" -d "database_name" """
    try:
        result = utils.commit(database, message)
        if result == 1:
            console.print("[bold green]Successfully committed changes.[/bold green]", highlight=False)
        elif result == 0:
            console.print("[yellow]No changes to commit.[/yellow]", highlight=False)

    except Exception as e:
        if str(e) == "dit not initialized":
            console.print("[bold red]Error: Dit not initialized.[/bold red]", highlight=False)
        else:
            console.print(f"[bold red]Error: {e}[/bold red]", highlight=False)
