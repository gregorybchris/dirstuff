import logging
from pathlib import Path

import click

from dirsum.lib.filter_criteria import FilterCriteria
from dirsum.lib.memory_utilities import size_to_bytes
from dirsum.lib.parser import Parser
from dirsum.lib.tree import Tree

logger = logging.getLogger(__name__)


@click.group()
def main() -> None:
    """Main CLI entrypoint."""


def get_tree(root: Path, min_size: str) -> Tree:
    min_bytes = size_to_bytes(min_size)
    filter_criteria = FilterCriteria(min_bytes=min_bytes)
    parser = Parser(filter_criteria=filter_criteria)
    absolute_root = Path.absolute(root)
    tree = parser.parse(absolute_root)
    filtered = tree.filter(filter_criteria)
    if filtered is None:
        raise ValueError("No paths matched filters")
    return filtered


@main.command(name="tree")
@click.argument("root", type=Path)
@click.option("--size", "min_size", type=str, default="10MB", help="Minimum size of directory to show.")
@click.option("--absolute", type=bool, is_flag=True, help="Print the absolute directory paths.")
def tree_command(
    root: Path,
    min_size: str,
    absolute: bool,
) -> None:
    tree = get_tree(root, min_size)
    tree.print(absolute=absolute)


@main.command(name="list")
@click.argument("root", type=Path)
@click.argument("dir_name", type=str)
@click.option("--size", "min_size", type=str, default="10MB", help="Minimum size of directory to show.")
def list_command(
    root: Path,
    dir_name: str,
    min_size: str,
) -> None:
    tree = get_tree(root, min_size)
    tree.list(dir_name=dir_name)
