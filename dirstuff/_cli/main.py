import logging
from pathlib import Path

import click

from dirstuff.summary.filter_criteria import FilterCriteria
from dirstuff.summary.memory_utilities import size_str_to_bytes
from dirstuff.summary.parser import Parser
from dirstuff.summary.tree import Tree

logger = logging.getLogger(__name__)


@click.group()
def main() -> None:
    pass


def get_tree(root: Path, min_size_str: str) -> Tree:
    min_bytes = size_str_to_bytes(min_size_str)
    filter_criteria = FilterCriteria(min_bytes=min_bytes)
    parser = Parser(filter_criteria=filter_criteria)
    absolute_root = Path.absolute(root)
    tree = parser.parse(absolute_root)
    filtered = tree.filter(filter_criteria)
    if filtered is None:
        msg = "No paths matched filters"
        raise ValueError(msg)
    return filtered


@main.command(name="tree")
@click.argument("root", type=Path)
@click.option("--size", "min_size_str", type=str, default="10MB", help="Minimum size of directory to show.")
@click.option("--absolute", type=bool, is_flag=True, help="Print the absolute directory paths.")
def tree_command(
    root: Path,
    min_size_str: str,
    absolute: bool,
) -> None:
    tree = get_tree(root, min_size_str)
    tree.print(absolute=absolute)


@main.command(name="search")
@click.argument("root", type=Path)
@click.argument("dir_name", type=str)
@click.option("--size", "min_size_str", type=str, default="10MB", help="Minimum size of directory to show.")
def search_command(
    root: Path,
    dir_name: str,
    min_size_str: str,
) -> None:
    tree = get_tree(root, min_size_str)
    tree.print_search(dir_name=dir_name)
