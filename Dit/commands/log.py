import rich_click as click

import Dit.utils.utils as utils
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

@click.command()
@click.option('-d', '--database', required=True, help='Database name')
def cli(database):
    """Shows the commit log of the dit repo

    View all commits you made to the database in the current branch.
    
    usage : dit log -d "database_name" """
    try:
        logs = utils.log(database)
        if not logs:
            console.print("No commit history found.", style="bold yellow")
            return
        console.print()
        table = Table(show_header=False, box=None)
        table.add_column("S/N", style="grey53", no_wrap=True)  # Grey (dark) serial numbers
        table.add_column("Hash", style="cyan", no_wrap=True)
        table.add_column("Message", style="green", no_wrap=True)

        # Generate serial numbers in descending order
        serial_number = len(logs)
        for log in logs:
            table.add_row(str(serial_number), log['hash'], log['message'])
            serial_number -= 1  # Decrease for the next entry

        panel = Panel(table, title=f"Commit History for [bold]{database}[/bold]", expand=False)
        console.print(panel)

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}", style="bold red")