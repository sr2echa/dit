import rich_click as click 
from rich.console import Console

import Dit.utils.utils as utils

console = Console()

@click.command()
@click.option('-d', '--database', required=True, help='Database name')
@click.argument('hash', required=True)
def cli(database, hash):
    """
    Compare the current database with a specific commit hash
    
    usage : dit diff -d "database_name" "commit_hash"
    """

    print(utils.diff(database, hash))