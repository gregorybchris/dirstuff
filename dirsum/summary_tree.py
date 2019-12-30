import os

from dirsum.memory_utilties import bytes_to_size
from colorama import Fore


class SummaryTree:
    def __init__(self, path, size=0):
        self._size = size
        self._path = path
        self._children = []
    
    def set_size(self, n_bytes):
        self._size = n_bytes
    
    def get_size(self):
        return self._size

    def add_child(self, child_tree):
        self._children.append(child_tree)

    def print(self, depth=0):
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
