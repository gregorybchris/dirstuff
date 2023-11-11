"""Tree to represent file system of directories."""
import os
from pathlib import Path
from typing import List, Optional

from colorama import Fore

from dirsum.lib.memory_utilities import bytes_to_size


class SummaryTree:
    """Tree to represent file system of directories."""

    def __init__(self, path: Optional[Path], size: int = 0):
        """
        Construct a SummaryTree.

        :param path: Filepath to the tree's root node directory.
        :param size: Size in bytes of the tree's root node directory.
        """
        self._size = size
        self._path = path
        self._children: List[SummaryTree] = []

    def set_size(self, n_bytes: int) -> None:
        """
        Set the tree's root node size.

        :param n_bytes: Number of bytes for the tree's root node.
        """
        self._size = n_bytes

    def get_size(self) -> int:
        """
        Get the tree's root node size.

        :return: The tree's root node size.
        """
        return self._size

    def add_child(self, child_tree: "SummaryTree") -> None:
        """
        Add a child node to the tree at the root.

        :param child_tree: SummaryTree to add as child to the current tree.
        """
        self._children.append(child_tree)

    def print(self, absolute: bool = False, depth: int = 0) -> None:
        """
        Print the formatted tree.

        :param depth: Internal parameter used to control indentation.
        """
        formatted_size = bytes_to_size(self._size)
        indent = "  " * depth
        _, dir_str = os.path.split(str(self._path))
        directory: Optional[Path] = Path(dir_str)

        if absolute:
            directory = self._path

        print(f"{indent} |-> ", end="")
        print(f"{Fore.BLUE}{formatted_size}", end="")
        print(f"{Fore.RESET} > ", end="")
        print(f"{Fore.GREEN}{directory}", end="")
        print(f"{Fore.RESET}")

        for child in sorted(self._children, key=lambda tree: -tree.get_size()):
            child.print(absolute=absolute, depth=depth + 1)
