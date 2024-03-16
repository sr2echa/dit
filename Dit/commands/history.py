import rich_click as click 
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from flask import Flask, render_template, request, redirect, url_for

import Dit.utils.utils as utils

console = Console()
app = Flask(__name__, template_folder='./templates')

@click.command()
@click.option('-d', '--database', required=True, help='Host Database')
def cli(database):
    """
    Vistualize the database.

    Usage: dit history -d "database_name"
    """
    json_data = utils.get_history(database)
    @app.route('/')
    def index():
        length = len(json_data["dummy"])
        return render_template('commit_v.html',data=json_data,length=length)

    console.print(f"Starting Flask server to visualize {database}...", style="bold green")
    # Start the Flask server
    app.run(debug=True, port=5000)

    

