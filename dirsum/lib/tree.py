import os
from pathlib import Path
from typing import List

from colorama import Fore

from dirsum.lib.filter_criteria import FilterCriteria
from dirsum.lib.memory_utilities import bytes_to_size


class Tree:
    def __init__(self, path: Path, size: int = 0):
        self.size = size
        self.path = path
        self.children: List[Tree] = []

    def set_size(self, n_bytes: int) -> None:
        self.size = n_bytes

    def get_size(self) -> int:
        return self.size

    def add_child(self, child: "Tree") -> None:
        self.children.append(child)

    def filter(self, filter_criteria: FilterCriteria) -> "Tree":
        filtered_tree = Tree(self.path, size=self.size)
        for child in self.children:
            if child.size >= filter_criteria.min_bytes:
                filtered_child = child.filter(filter_criteria)
                filtered_tree.add_child(filtered_child)

        return filtered_tree

    def print(self, absolute: bool = False, depth: int = 0, recursive: bool = True) -> None:
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

    def list(self, *, dir_name: str) -> None:
        trees: List[Tree] = []
        self._collect_trees(self, dir_name, trees)

        for tree in sorted(trees, key=lambda t: -t.get_size()):
            tree.print(absolute=True, recursive=False)

    @classmethod
    def _collect_trees(cls, tree: "Tree", dir_name: str, trees: List["Tree"]) -> None:
        if tree.path.name == dir_name:
            trees.append(tree)
            return

        for child in tree.children:
            cls._collect_trees(child, dir_name, trees)
