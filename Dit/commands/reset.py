import rich_click as click

import Dit.utils.utils as utils
from rich.console import Console

console = Console()

@click.command()
@click.option('-d', '--database', required=True, help='Database name')
# @click.option('-h', '--hash', required=False, help='Commit hash')
@click.argument('hash', required=False)
def cli(database, hash):
    """Reset the database to a specific state by commit hash."""
    try:
        utils.reset(database, hash)
        console.print(f"[bold green]Successfully reset {database} to {hash if hash else 'latest'}[/bold green]")
    except Exception as e:
        console.print(f"[bold red]Error: {str(e)}[/bold red]", style="bold red")
    
