import argparse
import os

from dirsum.summarizer import Summarizer


def create_summary(root, min_size):
    summarizer = Summarizer(min_size)
    absolute_root = os.path.abspath(root)
    tree = summarizer.summarize(absolute_root)
    tree.print()


def parse_args():
    parser = argparse.ArgumentParser(description='Summarize drive contents.')
    parser.add_argument('root', help='Root directory to summarize.')
    parser.add_argument('--size', dest='min_size', default='1GB',
                        help='Minimum size of directory to show (default bytes).')

    return parser.parse_args()


def run():
    args = parse_args()
    create_summary(args.root, args.min_size)
