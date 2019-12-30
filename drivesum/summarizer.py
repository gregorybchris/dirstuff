import os


class Summarizer:
    def __init__(self, min_bytes, max_children):
        self._min_bytes = min_bytes
        self._max_children = max_children

    def _format_bytes(self, n_bytes):
        suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
        for scale, suffix in enumerate(suffixes):
            multiplier = 10 ** (3 * (scale + 1))
            if n_bytes < multiplier:
                value = round(n_bytes / multiplier * 1000, 1)
                return '{:5.1f} {}'.format(value, suffix)
        raise ValueError("Bytes could not be converted")

    def summarize(self, root, depth=0):
        if os.path.islink(root):
            return 0

        child_paths = [os.path.join(root, f) for f in os.listdir(root)]
        child_dirs = [p for p in child_paths if os.path.isdir(p)]
        child_files = [p for p in child_paths if os.path.isfile(p)]

        total_dirs_size = 0
        for child_dir in child_dirs:
            child_size = self.summarize(child_dir, depth + 1)
            total_dirs_size += child_size

        total_files_size = 0
        for child_file in child_files:
            child_file_size = os.path.getsize(child_file)
            total_files_size += child_file_size

        root_size = total_files_size + total_dirs_size
        if root_size > self._min_bytes:
            indentation = '  ' * depth
            formatted_size = self._format_bytes(root_size)
            print(f"{indentation} |-> {formatted_size} > {root}")
        return root_size

