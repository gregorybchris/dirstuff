"""Recursive directory summarizer."""
import os
from pathlib import Path, PurePath

from dirsum.lib.memory_utilities import size_to_bytes
from dirsum.lib.summary_tree import SummaryTree


class Summarizer:
    """Recursive directory summarizer."""

    def __init__(self, min_size: str):
        """
        Construct a Summarizer.

        :param min_size: Minimum directory size to include in the summary.
        """
        self._min_bytes = size_to_bytes(min_size)

    def summarize(self, root_dir: Path) -> SummaryTree:
        """
        Summarize the directory contents.

        :param root_dir: Root directory to summarize.
        :return: A SummaryTree representation of the file system.
        """
        return self._get_tree(root_dir)

    def _get_empty_tree(self) -> SummaryTree:
        """Construct an empty tree for symlinked directories."""
        return SummaryTree(None, size=0)

    def _get_tree(self, root_dir: Path) -> SummaryTree:
        """Recursively build a tree of directories."""
        if Path.is_symlink(root_dir):
            return self._get_empty_tree()

        child_paths = [PurePath.joinpath(root_dir, f) for f in Path.iterdir(root_dir)]

        root_tree = SummaryTree(root_dir)

        total_files_size = 0
        child_files = [p for p in child_paths if Path.is_file(p)]
        for child_file in child_files:
            child_file_size = os.path.getsize(child_file)
            total_files_size += child_file_size

        total_dirs_size = 0
        child_dirs = [p for p in child_paths if Path.is_dir(p)]
        for child_dir in child_dirs:
            child_tree = self._get_tree(child_dir)
            child_size = child_tree.get_size()
            total_dirs_size += child_size
            if child_size > self._min_bytes:
                root_tree.add_child(child_tree)

        root_tree.set_size(total_files_size + total_dirs_size)
        return root_tree
