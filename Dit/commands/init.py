import rich_click as click
import mysql.connector
from mysql.connector import Error
import questionary
from questionary import Choice
from rich.console import Console
import Dit.utils.utils as utils

console = Console()

@click.command()
@click.option('-d', '--default', 'use_defaults', is_flag=True, help='Use default values for username, host, and port.')
def cli(use_defaults):
    """Initialize Dit Repository
    
    Sets up the versioning control for your database.
    Get started by running `dit init`
    """

    if use_defaults:
        username = "root" 
        host = "localhost"
        port = 3306
    else:
        username = questionary.text("Please enter your MySQL username:", default="root").ask()
        password = questionary.password("Please enter your MySQL password:").ask()
        host = questionary.text("Please enter your MySQL host:", default="localhost").ask()
        port = questionary.text("Please enter your MySQL port:", default="3306").ask()

    port = str(int(port))

    databases = []
    try:
        with mysql.connector.connect(host=host, user=username, password=password, port=port) as connection:
            console.print("✅ Successfully connected to MySQL server.", style="bold green")
            cursor = connection.cursor()
            cursor.execute("SHOW DATABASES")
            databases = [db[0] for db in cursor]
    except Error as e:
        console.print(f"Unable to connect to MySQL server: {str(e)}", style="bold red")
        return

    databases.append("🌟 Create a new database")
    userDbOption = questionary.select("Choose a database or create a new one:", choices=databases).ask()

    if userDbOption == "🌟 Create a new database":
        database = questionary.text("Enter the name of the new database to create:").ask()
        try:
            with mysql.connector.connect(host=host, user=username, password=password, port=port) as connection:
                cursor = connection.cursor()
                cursor.execute(f"CREATE DATABASE `{database}`")
                console.print(f"🆕 Database `{database}` created successfully.", style="bold green")
        except Error as e:
            console.print(f"💥 Failed to create database `{database}`: {str(e)}", style="bold red")
            return
    else:
        database = userDbOption

    details = {"username": username, "password": password, "host": host, "port": port, "database": database}
    utils.init(details)

    console.print("💾 Dit Repository Initialized.", style="bold blue")

if __name__ == "__main__":
    cli()


