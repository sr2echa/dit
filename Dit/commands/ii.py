import typer

app = typer.Typer(pretty_exceptions_enable=True)

@app.command()
def main():
    """Execute the commit command."""
    typer.echo("Committing changes.")