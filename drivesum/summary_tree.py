from drivesum.memory_utilties import bytes_to_size

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
        indentation = '  ' * depth
        print(f"{indentation} |-> {formatted_size} > {self._path}")

        sorted_children = sorted(self._children, key=lambda tree: -tree.get_size())

        for child in sorted_children:
            child.print(depth=depth + 1)
            