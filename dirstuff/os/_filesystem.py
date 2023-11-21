# pylint: disable=redefined-builtin
import re
import shutil
from abc import ABC
from pathlib import Path as PathlibPath
from typing import Any, List, Tuple


class Path(ABC):
    def __init__(self, *args: Any, **kwargs: Any):
        self.libpath = PathlibPath(*args, **kwargs)

    @property
    def name(self) -> str:
        return self.libpath.name

    def to_dir(self) -> "Dir":
        return Dir(self.libpath)

    def to_file(self) -> "File":
        return File(self.libpath)

    def exists(self) -> bool:
        return self.libpath.exists()


class File(Path):
    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        if self.libpath.exists() and not self.libpath.is_file():
            raise ValueError(f"Tried to create File from non-file path: {self.libpath}")

    def rename(self, new_name: str) -> "File":
        new_path = self.libpath.parent / new_name
        self.libpath = self.libpath.rename(new_path)
        return self

    def rename_regex(self, search: str, replace: str) -> "File":
        new_name = re.sub(search, replace, self.name)
        new_path = self.libpath.parent / new_name
        self.libpath = self.libpath.rename(new_path)
        return self

    def move_into(self, dir: "Dir") -> "File":
        path = dir.libpath / self.libpath.name
        self.libpath = self.libpath.rename(path)
        return self

    def copy_to(self, file: "File") -> "File":
        shutil.copy(self.libpath, file.libpath)
        self.libpath = file.libpath
        return self

    def copy_into(self, dir: "Dir") -> "File":
        path = dir.libpath / self.libpath.name
        shutil.copy(self.libpath, path)
        self.libpath = path
        return self

    def delete(self, missing_ok: bool = False) -> None:
        self.libpath.unlink(missing_ok=missing_ok)


class Dir(Path):
    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        if self.libpath.exists() and not self.libpath.is_dir():
            raise ValueError(f"Tried to create Dir from non-dir path: {self.libpath}")

    def walk(self) -> Tuple[List["File"], List["Dir"]]:
        files: List[File] = []
        dirs: List[Dir] = []
        for libpath in self.libpath.iterdir():
            if libpath.is_file():
                files.append(File(libpath))
            elif libpath.is_dir():
                dirs.append(Dir(libpath))
            else:
                raise ValueError(f"Could not parse path as file or directory: {libpath}")
        return files, dirs

    def iter_files(self) -> List["File"]:
        files, _ = self.walk()
        return files

    def iter_dirs(self) -> List["Dir"]:
        _, dirs = self.walk()
        return dirs

    def rename(self, new_name: str) -> "Dir":
        new_path = self.libpath.parent / new_name
        self.libpath = self.libpath.rename(new_path)
        return self

    def rename_regex(self, search: str, replace: str) -> "Dir":
        new_name = re.sub(search, replace, self.name)
        new_path = self.libpath.parent / new_name
        self.libpath = self.libpath.rename(new_path)
        return self

    def move_into(self, dir: "Dir") -> "Dir":
        path = dir.libpath / self.libpath.name
        shutil.move(self.libpath, path)
        self.libpath = PathlibPath(path)
        return self

    def copy_to(self, dir: "Dir") -> "Dir":
        shutil.copytree(self.libpath, dir.libpath)
        self.libpath = dir.libpath
        return self

    def copy_into(self, dir: "Dir") -> "Dir":
        path = dir.libpath / self.libpath.name
        shutil.copytree(self.libpath, path)
        self.libpath = path
        return self

    def delete(self, missing_ok: bool = False) -> None:
        if not self.libpath.exists() and not missing_ok:
            raise FileNotFoundError(f"No directory at {self.libpath}")
        shutil.rmtree(self.libpath)

    def make(self, parents: bool = True, exist_ok: bool = True) -> "Dir":
        self.libpath.mkdir(parents=parents, exist_ok=exist_ok)
        return self
