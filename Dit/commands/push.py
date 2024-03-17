import rich_click as click 
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
import questionary

import Dit.utils.utils as utils

console = Console()

@click.command()
@click.option('-d', '--database', required=True, help='Host Database')
def cli(database):
    """
    Push the current branch to remote repo.
    """
    host = r"https://a833-122-187-117-178.ngrok-free.app"
    try:
        utils.push(database, host)
        console.print(f"[bold green] Repo successfully pushed to {host}[/bold green]")
    except Exception as e:
        console.print(f"[bold red]Error: {str(e)}[/bold red]", style="bold red")


    