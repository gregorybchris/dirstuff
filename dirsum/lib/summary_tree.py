import os
from pathlib import Path
from typing import List, Optional

from colorama import Fore

from dirsum.lib.filter_criteria import FilterCriteria
from dirsum.lib.memory_utilities import bytes_to_size


class SummaryTree:
    def __init__(self, path: Path, size: int = 0):
        self.size = size
        self.path = path
        self.children: List[SummaryTree] = []

    def set_size(self, n_bytes: int) -> None:
        self.size = n_bytes

    def get_size(self) -> int:
        return self.size

    def add_child(self, child_tree: "SummaryTree") -> None:
        self.children.append(child_tree)

    def filter(self, filter_criteria: FilterCriteria) -> Optional["SummaryTree"]:
        if self.size < filter_criteria.min_bytes:
            return None

        filtered_tree = SummaryTree(self.path, size=self.size)

        if filter_criteria.names is not None:
            if any(name == self.path.name for name in filter_criteria.names):
                return filtered_tree
            if len(self.children) == 0:
                return None

        for child in self.children:
            filtered_child = child.filter(filter_criteria)
            if filtered_child is not None:
                filtered_tree.add_child(filtered_child)

        if filter_criteria.names is not None:
            if len(filtered_tree.children) == 0 and all(name != self.path.name for name in filter_criteria.names):
                return None

        return filtered_tree

    def print(self, absolute: bool = False, list_mode: bool = False, depth: int = 0) -> None:
        formatted_size = bytes_to_size(self.size)
        indent = "  " * depth
        _, dir_str = os.path.split(str(self.path))
        directory = Path(dir_str)

        if absolute:
            directory = self.path

        if list_mode:
            indent = ""

        if not list_mode or len(self.children) == 0:
            print(f"{indent} |-> ", end="")
            print(f"{Fore.BLUE}{formatted_size}", end="")
            print(f"{Fore.RESET} > ", end="")
            print(f"{Fore.GREEN}{directory}", end="")
            print(f"{Fore.RESET}")

        for child in sorted(self.children, key=lambda tree: -tree.get_size()):
            child.print(absolute=absolute, list_mode=list_mode, depth=depth + 1)
