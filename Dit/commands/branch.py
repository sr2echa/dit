import rich_click as click 
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

import Dit.utils.utils as utils

console = Console()

@click.command()
@click.option('-d', '--database', required=True, help='Database name')
@click.argument('branchname', required=True)
def cli(database, branchname):
    """
    Create a new branch from the current commit.
    
    Usage: dit branch -d "database_name" "branch_name"
    """
    branch = utils.branch(database, branchname)

    if branch:
        console.print(f"[bold green]Branch {branchname} created successfully[/bold green]")
        console.print(f"[light]Switch to the new branch using 'USE {branch}' in MySQL[/light]")
        console.print(f"[grey]All changes mad to {branch} database will be under the {branchname} branch[/grey]")
    else:
        console.print(f"[bold red]Error: Branch {branchname} already exists[/bold red]")


    