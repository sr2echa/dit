import rich_click as click 
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

import Dit.utils.utils as utils

console = Console()

@click.command()
@click.option('-d', '--database', required=True, help='Database name')
@click.argument('hash', required=True)
def cli(database, hash):
    """
    Compare the current database with a specific commit hash.

    Usage: dit diff -d "database_name" "commit_hash"
    """
    
    diff = utils.diff(database, hash)
    
    changes_count = 0  # To keep track of the number of changes
    
    if diff:
        table = Table(title=f"Diff for [bold]{database}[/] at commit [bold]{hash}[/]", show_header=False, box=None)
        
        # Tables Removed
        if diff['minus_tables']:
            changes_count += len(diff['minus_tables'])
            for table_name in diff['minus_tables']:
                table.add_row(f"[bold red]- Table removed:[/] {table_name}")
        
        # Tables Added
        if diff['plus_tables']:
            changes_count += len(diff['plus_tables'])
            for table_name in diff['plus_tables']:
                table.add_row(f"[bold green]+ Table added:[/] {table_name}")
        
        # Rows Removed
        if diff['minus_rows']:
            for table_name, rows in diff['minus_rows'].items():
                changes_count += len(rows)
                for row in rows:
                    table.add_row(f"[bold red]- Row removed from {table_name}:[/] {row}")
        
        # Rows Added
        if diff['plus_rows']:
            for table_name, rows in diff['plus_rows'].items():
                changes_count += len(rows)
                for row in rows:
                    table.add_row(f"[bold green]+ Row added to {table_name}:[/] {row}")

        if changes_count > 0:
            console.print(Panel.fit(table, border_style="blue"))
            console.print(f"[bold]{changes_count} changes detected.[/]")
        else:
            console.print("No differences found.", style="yellow")
    else:
        console.print("Diff data is empty or an error occurred.", style="bold red")
