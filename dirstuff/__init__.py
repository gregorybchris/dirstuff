import importlib.metadata

from dirstuff.os.filesystem import Dir, File, Path

__version__ = importlib.metadata.version("dirstuff")

__all__ = [
    "Dir",
    "File",
    "Path",
]
