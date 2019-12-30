"""Main module for running dirsum commands."""
import argparse
import os

from dirsum.summarizer import Summarizer


def create_summary(root, min_size):
    """Create and print a formatted recursive summary."""
    summarizer = Summarizer(min_size)
    absolute_root = os.path.abspath(root)
    summarizer.summarize(absolute_root).print()


def parse_args():
    """Parse the arguments to the main dirsum script."""
    parser = argparse.ArgumentParser(description='Summarize drive contents.')
    parser.add_argument('root', help='Root directory to summarize.')
    parser.add_argument('--size', dest='min_size', default='1GB',
                        help='Minimum size of directory to show (default bytes).')

    return parser.parse_args()


def run():
    """Entrypoint for the dirsum script."""
    args = parse_args()
    create_summary(args.root, args.min_size)
