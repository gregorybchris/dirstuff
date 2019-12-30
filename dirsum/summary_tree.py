"""Tree to represent file system of directories."""
import os

from dirsum.memory_utilties import bytes_to_size
from colorama import Fore


class SummaryTree:
    """Tree to represent file system of directories."""

    def __init__(self, path, size=0):
        """
        Construct a SummaryTree.

        :param path: Filepath to the tree's root node directory.
        :param size: Size in bytes of the tree's root node directory.
        """
        self._size = size
        self._path = path
        self._children = []

    def set_size(self, n_bytes):
        """
        Set the tree's root node size.

        :param n_bytes: Number of bytes for the tree's root node.
        """
        self._size = n_bytes

    def get_size(self):
        """
        Get the tree's root node size.

        :return: The tree's root node size.
        """
        return self._size

    def add_child(self, child_tree):
        """
        Add a child node to the tree at the root.

        :param child_tree: SummaryTree to add as child to the current tree.
        """
        self._children.append(child_tree)

    def print(self, depth=0):
        """
        Print the formatted tree.

        :param depth: Internal parameter used to control indentation.
        """
        formatted_size = bytes_to_size(self._size)
        indent = '  ' * depth
        _, path_tail = os.path.split(self._path)

        print(f"{indent} |-> ", end='')
        print(f"{Fore.BLUE}{formatted_size}", end='')
        print(f"{Fore.RESET} > ", end='')
        print(f"{Fore.GREEN}{path_tail}", end='')
        print(f"{Fore.RESET}")

        for child in sorted(self._children, key=lambda tree: -tree.get_size()):
            child.print(depth=depth + 1)
