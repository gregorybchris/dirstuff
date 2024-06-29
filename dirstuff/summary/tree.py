import os
from pathlib import Path
from typing import Iterator

from colorama import Fore

from dirstuff.summary.filter_criteria import FilterCriteria
from dirstuff.summary.memory_utilities import bytes_to_size

# ruff: noqa: T201


class Tree:
    """A tree structure to represent a directory and its children."""

    def __init__(self, path: Path, size: int = 0):
        """Construct a Tree object.

        Args:
            path (Path): The path of the directory.
            size (int): The size of the directory in bytes. Defaults to 0.
        """
        self.size = size
        self.path = path
        self.children: list[Tree] = []

    def set_size(self, n_bytes: int) -> None:
        """Manually set the size of the directory in bytes.

        Args:
            n_bytes (int): The size of the directory in bytes.
        """
        self.size = n_bytes

    def get_size(self) -> int:
        """Get the size of the directory in bytes.

        Returns:
            int: The size of the directory in bytes.
        """
        return self.size

    def add_child(self, child: "Tree") -> None:
        """Add a child to the directory.

        Args:
            child (Tree): The child tree to add as a subtree.
        """
        self.children.append(child)

    def filter(self, filter_criteria: FilterCriteria) -> "Tree":
        """Filter the tree based on the filter criteria.

        Args:
            filter_criteria (FilterCriteria): The filter criteria to apply.

        Returns:
            Tree: The filtered tree.
        """
        filtered_tree = Tree(self.path, size=self.size)
        for child in self.children:
            if child.size >= filter_criteria.min_bytes:
                filtered_child = child.filter(filter_criteria)
                filtered_tree.add_child(filtered_child)

        return filtered_tree

    def print(self, absolute: bool = False, depth: int = 0, recursive: bool = True) -> None:
        """Print the tree structure.

        Args:
            absolute (bool): Print the absolute directory paths. Defaults to False.
            depth (int): The depth of the tree. Defaults to 0.
            recursive (bool): Print the tree recursively. Defaults to True.
        """
        formatted_size = bytes_to_size(self.size)
        indent = "  " * depth
        _, dir_str = os.path.split(str(self.path))
        directory = Path(dir_str)

        if absolute:
            directory = self.path

        print(f"{indent} |-> ", end="")
        print(f"{Fore.BLUE}{formatted_size}", end="")
        print(f"{Fore.RESET} > ", end="")
        print(f"{Fore.GREEN}{directory}", end="")
        print(f"{Fore.RESET}")

        if recursive:
            for child in sorted(self.children, key=lambda tree: -tree.get_size()):
                child.print(absolute=absolute, depth=depth + 1)

    def print_search(self, *, dir_name: str) -> None:
        """Print all directories with the given name.

        Args:
            dir_name (str): The name of the directory to search for.
        """
        trees = self._iter_trees_with_name(self, dir_name)
        for tree in sorted(trees, key=lambda t: -t.get_size()):
            tree.print(absolute=True, recursive=False)

    @classmethod
    def _iter_trees_with_name(cls, tree: "Tree", dir_name: str) -> Iterator["Tree"]:
        if tree.path.name == dir_name:
            yield tree

        for child in tree.children:
            yield from cls._iter_trees_with_name(child, dir_name)
