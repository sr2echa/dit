import rich_click as click 
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
import questionary

import Dit.utils.utils as utils

console = Console()

@click.command()
@click.option('-d', '--database', required=True, help='Host Database')
@click.argument('branchname', required=True)
def cli(database, branchname):
    """
    Merge a branch into the current branch.

    Usage: dit merge -d "database_name" "branch_name"
    """
    utils.merge(database, branchname)


    