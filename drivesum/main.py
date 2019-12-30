import argparse
import os

from drivesum.summarizer import Summarizer


def create_summary(root, min_bytes, max_children):
    summarizer = Summarizer(min_bytes, max_children)
    absolute_root = os.path.abspath(root)
    print(f"Summarizing {absolute_root}")
    summarizer.summarize(absolute_root)


def parse_args():
    parser = argparse.ArgumentParser(description='Summarize drive contents.')
    parser.add_argument('root', help='Root directory to summarize.')
    parser.add_argument('--size', dest='min_bytes', default=500000000, type=int,
                        help='Minimum size of directory to show in bytes.')
    parser.add_argument('--breadth', dest='max_children', default=5, type=int,
                        help='Maximum number of children to show per directory.')

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()

    create_summary(args.root, args.min_bytes, args.max_children)
