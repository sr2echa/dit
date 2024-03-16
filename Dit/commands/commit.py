import rich_click as click

@click.command('c2')
def cli():
    """Description for command1."""
    click.echo('Executing command1')

# import typer

# app = typer.Typer(pretty_exceptions_enable=True)

# @app.command()
# def main():
#     """Execute the commit command."""
#     typer.echo("Committing changes.")

# # Make sure each command file has a Typer app object that can be loaded.

