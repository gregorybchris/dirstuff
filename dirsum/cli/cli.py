import logging
from pathlib import Path
from typing import Tuple

import click

from dirsum.lib.filter_criteria import FilterCriteria
from dirsum.lib.memory_utilities import size_to_bytes
from dirsum.lib.summarizer import Summarizer

logger = logging.getLogger(__name__)


@click.group()
def main() -> None:
    """Main CLI entrypoint."""


@main.command(name="summarize")
@click.argument("root", type=Path)
@click.option("--size", "min_size", type=str, default="1GB", help="Minimum size of directory to show.")
@click.option("--absolute", type=bool, is_flag=True, help="Print the absolute directory paths.")
@click.option("--name", "-n", type=str, multiple=True, help="Names of folder names to filter.")
@click.option("--list", "list_mode", type=bool, is_flag=True, help="Turn on list mode.")
def summarize_command(
    root: Path,
    min_size: str,
    absolute: bool,
    name: Tuple[str, ...],
    list_mode: bool,
) -> None:
    min_bytes = size_to_bytes(min_size)
    names_list = None if len(name) == 0 else list(name)
    filter_criteria = FilterCriteria(
        min_bytes=min_bytes,
        names=names_list,
    )
    summarizer = Summarizer(filter_criteria=filter_criteria)
    absolute_root = Path.absolute(root)
    summary_tree = summarizer.summarize(absolute_root)
    summary_tree.print(absolute=absolute, list_mode=list_mode)
