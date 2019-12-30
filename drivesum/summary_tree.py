class SummaryTree:
    def __init__(self, path):
        self._path = path
        self._children = []
    
    def set_size(self, n_bytes):
        self._size = n_bytes
    
    def add_child(self, child_tree):
        self._children.append(child_tree)