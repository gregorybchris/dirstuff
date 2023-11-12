import os
from pathlib import Path, PurePath

from dirsum.lib.filter_criteria import FilterCriteria
from dirsum.lib.tree import Tree


class Parser:
    def __init__(self, *, filter_criteria: FilterCriteria):
        self.filter_criteria = filter_criteria

    def parse(self, root_dirpath: Path) -> Tree:
        tree = Tree(root_dirpath)
        child_paths = [PurePath.joinpath(root_dirpath, f) for f in Path.iterdir(root_dirpath)]

        total_files_size = 0
        child_files = [p for p in child_paths if Path.is_file(p)]
        for child_file in child_files:
            child_file_size = os.path.getsize(child_file)
            total_files_size += child_file_size

        total_size = 0
        child_paths = [p for p in child_paths if Path.is_dir(p)]
        for child_path in child_paths:
            if Path.is_symlink(child_path):
                continue
            child_tree = self.parse(child_path)
            if child_tree is None:
                continue
            total_size += child_tree.get_size()
            tree.add_child(child_tree)

        tree.set_size(total_files_size + total_size)
        return tree
