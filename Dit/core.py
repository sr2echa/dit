# import click
# import os
# import importlib

# # The group that holds all commands
# @click.group()
# def cli():
#     """Your CLI tool description."""
#     pass

# def load_commands():
#     commands_dir = os.path.join(os.path.dirname(__file__), 'commands')
#     for module in os.listdir(commands_dir):
#         if os.path.isdir(os.path.join(commands_dir, module)) and not module.startswith('_'):
#             mod = importlib.import_module(f'.commands.{module}', package='Dit')
#             if hasattr(mod, 'cli'):
#                 cli.add_command(mod.cli)

# load_commands()

# if __name__ == '__main__':
#     cli()

# import rich_click as click
# from pathlib import Path
# import importlib.util
# import sys
# import colorama

# colorama.init()

# @click.group()
# def cli():
#     """Dit CLI tool."""
#     pass

# def load_command(name: str, filepath: Path):
#     spec = importlib.util.spec_from_file_location(name, filepath)
#     if spec and spec.loader:
#         module = importlib.util.module_from_spec(spec)
#         spec.loader.exec_module(module)
#         for attr_name in dir(module):
#             if not attr_name.startswith('_'):
#                 command_function = getattr(module, attr_name)
#                 if callable(command_function):
#                     # If the command is a Typer command, use the callback
#                     if hasattr(command_function, 'callback'):
#                         command_function = command_function.callback
#                     cli.command(name=name)(command_function)

# def setup_dynamic_commands():
#     commands_dir = Path(__file__).resolve().parent / 'commands'
#     for filepath in commands_dir.glob("*.py"):
#         if filepath.name.startswith("_"):  # Skip special or private files
#             continue
#         load_command(filepath.stem, filepath)

# setup_dynamic_commands()

# if __name__ == "__main__":
#     cli()

# import rich_click as click
# from pathlib import Path
# import importlib.util
# import sys
# import colorama

# colorama.init()
# click.use_rich_click()

# @click.group()
# def cli():
#     """Dit CLI tool."""
#     pass

# def setup_dynamic_commands():
#     commands_dir = Path(__file__).resolve().parent / 'commands'
#     for filepath in commands_dir.glob("*.py"):
#         if filepath.name.startswith("_"):
#             continue
#         module_name = filepath.stem
#         spec = importlib.util.spec_from_file_location(module_name, filepath)
#         if spec and spec.loader:
#             module = importlib.util.module_from_spec(spec)
#             spec.loader.exec_module(module)
#             # Assuming each command module has a 'register_to' function
#             if hasattr(module, 'register_to'):
#                 module.register_to(cli)

# setup_dynamic_commands()

# if __name__ == "__main__":
#     cli()

import rich_click as click
from pathlib import Path
import importlib.util

@click.group()
def cli():
    """Dit CLI tool."""
    pass

def load_command(name: str, filepath: Path):
    spec = importlib.util.spec_from_file_location(name, filepath)
    if spec and spec.loader:
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        # Assume there is a Click command function named `cli` in each module
        if hasattr(module, 'cli') and callable(getattr(module, 'cli')):
            command_function = getattr(module, 'cli')
            cli.add_command(command_function, name=name)

def setup_dynamic_commands():
    commands_dir = Path(__file__).resolve().parent / 'commands'
    for filepath in commands_dir.glob("*.py"):
        if filepath.name.startswith("_"):  # Skip special or private files
            continue
        load_command(filepath.stem, filepath)

setup_dynamic_commands()

if __name__ == "__main__":
    cli()
