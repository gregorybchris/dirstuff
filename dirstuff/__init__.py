import importlib.metadata

from dirstuff.os.filesystem import Dir, File

__version__ = importlib.metadata.version("dirstuff")

__all__ = [
    "Dir",
    "File",
]
