import rich_click as click 
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from flask import Flask, render_template, request, redirect, url_for

import Dit.utils.utils as utils

console = Console()
app = Flask(__name__)

@click.command()
@click.option('-d', '--database', required=True, help='Host Database')
@click.argument('hash', required=True)
def cli(database, hash):
    """
    Vistualize the database.

    Usage: dit vitualize -d "database_name" "hash"
    """
    json_data1 = utils.get_visualize(database, hash)
    @app.route('/')
    def index():
        meta_data = json_data1.get("__meta__", [])
        data_without_meta = {key: value for key, value in json_data1.items() if key != "__meta__"}
        return render_template('template_vis.html', data=data_without_meta, meta_data= meta_data)

    console.print(f"Starting Flask server to visualize {database} at {hash}...", style="bold green")
    # Start the Flask server
    app.run(debug=True, port=5000)

    


    