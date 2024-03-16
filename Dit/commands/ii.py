import rich_click as click

@click.command()
@click.argument('name')
def cli(name):
    """Greet a user by name.
    
    Hiii"""
    click.echo(f"Hello, {name}!")
