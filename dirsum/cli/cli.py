import logging
from pathlib import Path

import click

from dirsum.lib.summarizer import Summarizer

logger = logging.getLogger(__name__)


@click.group()
def main() -> None:
    """Main CLI entrypoint."""


@main.command(name="summarize")
@click.argument("root", type=Path)
@click.option("--size", "min_size", type=str, default="1GB", help="Minimum size of directory to show (default bytes).")
@click.option("--absolute", type=bool, is_flag=True, help="Whether to print the absolute directory paths.")
def summarize_command(
    root: Path,
    min_size: str,
    absolute: bool,
) -> None:
    summarizer = Summarizer(min_size)
    absolute_root = Path.absolute(root)
    summary_tree = summarizer.summarize(absolute_root)
    summary_tree.print(absolute=absolute)
