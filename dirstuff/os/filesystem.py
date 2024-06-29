import re
import shutil
from pathlib import Path as PathlibPath
from typing import Any, Iterator, Protocol


class Path(Protocol):
    """Abstract base class for system paths."""

    libpath: PathlibPath

    def __init__(self, *args: Any, **kwargs: Any):
        """Construct a Path object."""
        self.libpath = PathlibPath(*args, **kwargs)

    @property
    def name(self) -> str:
        """Get the name of the file or directory."""
        return self.libpath.name

    def exists(self) -> bool:
        """Check if the path exists."""
        return self.libpath.exists()

    def __str__(self) -> str:
        """Get the string representation of the path."""
        return str(self.libpath)


class Dir(Path):
    """A directory."""

    def __init__(self, *args: Any, **kwargs: Any):
        """Construct a Dir object.

        This constructor takes the same arguments as the pathlib.Path constructor.

        Raises:
            ValueError: If the path is not a directory.
        """
        super().__init__(*args, **kwargs)
        if self.libpath.exists() and not self.libpath.is_dir():
            msg = f"Tried to create Dir from non-dir path: {self.libpath}"
            raise ValueError(msg)

    def walk(self) -> tuple[list["File"], list["Dir"]]:
        """Walk the directory and return its files and subdirectories.

        Returns:
            tuple[list[File], list[Dir]]: A tuple containing the files and subdirectories.

        Raises:
            ValueError: If the path is neither a file nor a directory.
        """
        files: list["File"] = []
        dirs: list["Dir"] = []
        for libpath in self.libpath.iterdir():
            if libpath.is_file():
                files.append(File(libpath))
            elif libpath.is_dir():
                dirs.append(Dir(libpath))
            else:
                msg = f"Could not parse path as file or directory: {libpath}"
                raise ValueError(msg)
        return files, dirs

    def iter_files(self) -> Iterator["File"]:
        """Iterate over the files in the directory.

        Yields:
            Iterator[File]: An iterator over the files in the directory.
        """
        for libpath in self.libpath.iterdir():
            if libpath.is_file():
                yield File(libpath)

    def iter_dirs(self) -> Iterator["Dir"]:
        """Iterate over the subdirectories in the directory.

        Yields:
            Iterator[Dir]: An iterator over the subdirectories in the directory.
        """
        for libpath in self.libpath.iterdir():
            if libpath.is_dir():
                yield Dir(libpath)

    def rename(self, new_name: str, same_name_ok: bool = False) -> "Dir":
        """Rename the directory.

        Args:
            new_name (str): The new name of the directory.
            same_name_ok (bool): Whether to allow the same name. Defaults to False.

        Returns:
            Dir: The renamed directory.

        Raises:
            ValueError: If the name is the same and same_name_ok is False.
            FileNotFoundError: If the directory does not exist and missing_ok is False.
        """
        if new_name == self.name and not same_name_ok:
            msg = f"No change made to dir name: {self.name}"
            raise ValueError(msg)
        if not self.libpath.exists():
            msg = f"Dir does not exist: {self.libpath}"
            raise FileNotFoundError(msg)
        new_path = self.libpath.parent / new_name
        self.libpath = self.libpath.rename(new_path)
        return self

    def rename_regex(self, pattern: str, replace: str, same_name_ok: bool = False) -> "Dir":
        """Rename the directory using a regular expression.

        Args:
            pattern (str): The regular expression pattern.
            replace (str): The replacement string.
            same_name_ok (bool): Whether to allow the same name. Defaults to False.

        Returns:
            Dir: The renamed directory

        Raises:
            ValueError: If the name is the same and same_name_ok is False.
            FileNotFoundError: If the directory does not exist and missing_ok is False.
        """
        new_name = re.sub(pattern, replace, self.name)
        if new_name == self.name and not same_name_ok:
            msg = f"No change made to dir name: {self.name}"
            raise ValueError(msg)
        if not self.libpath.exists():
            msg = f"Dir does not exist: {self.libpath}"
            raise FileNotFoundError(msg)
        new_path = self.libpath.parent / new_name
        self.libpath = self.libpath.rename(new_path)
        return self

    def move_into(self, dir: "Dir") -> "Dir":
        """Move the directory into another directory.

        Args:
            dir (Dir): The directory to move into.

        Returns:
            Dir: The moved directory.
        """
        path = dir.libpath / self.libpath.name
        shutil.move(self.libpath, path)
        self.libpath = PathlibPath(path)
        return self

    def copy_to(self, dir: "Dir") -> "Dir":
        """Copy the directory to another directory.

        Args:
            dir (Dir): The directory to copy to.

        Returns:
            Dir: The copied directory.
        """
        shutil.copytree(self.libpath, dir.libpath)
        self.libpath = dir.libpath
        return self

    def copy_into(self, dir: "Dir") -> "Dir":
        """Copy the directory into another directory.

        Args:
            dir (Dir): The directory to copy into.

        Returns:
            Dir: The copied directory
        """
        path = dir.libpath / self.libpath.name
        shutil.copytree(self.libpath, path)
        self.libpath = path
        return self

    def delete(self, missing_ok: bool = False) -> None:
        """Delete the directory.

        Args:
            missing_ok (bool): Whether to allow the directory to be missing. Defaults to False.

        Raises:
            FileNotFoundError: If the directory does not exist and missing_ok is False.
        """
        if not self.libpath.exists() and not missing_ok:
            msg = f"No directory at {self.libpath}"
            raise FileNotFoundError(msg)
        shutil.rmtree(self.libpath)

    def make(self, parents: bool = True, exist_ok: bool = True) -> "Dir":
        """Create the directory on disk.

        Args:
            parents (bool): Whether to make parent directories. Defaults to True.
            exist_ok (bool): Whether to allow the directory to exist. Defaults to True.

        Returns:
            Dir: The created directory.
        """
        self.libpath.mkdir(parents=parents, exist_ok=exist_ok)
        return self

    @property
    def parent(self) -> "Dir":
        """Get the parent directory.

        Returns:
            Dir: The parent directory.
        """
        return Dir(self.libpath.parent)


class File(Path):
    """A file."""

    def __init__(self, *args: Any, **kwargs: Any):
        """Construct a File object.

        This constructor takes the same arguments as the pathlib.Path constructor.

        Raises:
            ValueError: If the path is not a file.
        """
        super().__init__(*args, **kwargs)
        if self.libpath.exists() and not self.libpath.is_file():
            msg = f"Tried to create File from non-file path: {self.libpath}"
            raise ValueError(msg)

    def rename(self, new_name: str, same_name_ok: bool = False) -> "File":
        """Rename the file.

        Args:
            new_name (str): The new name of the file.
            same_name_ok (bool): Whether to allow the same name. Defaults to False.

        Returns:
            File: The renamed file.

        Raises:
            ValueError: If the name is the same and same_name_ok is False.
            FileNotFoundError: If the file does not exist and missing_ok is False.
        """
        if new_name == self.name and not same_name_ok:
            msg = f"No change made to file name: {self.name}"
            raise ValueError(msg)
        if not self.libpath.exists():
            msg = f"File does not exist: {self.libpath}"
            raise FileNotFoundError(msg)
        new_path = self.libpath.parent / new_name
        self.libpath = self.libpath.rename(new_path)
        return self

    def rename_regex(self, pattern: str, replace: str, same_name_ok: bool = False) -> "File":
        """Rename the file using a regular expression.

        Args:
            pattern (str): The regular expression pattern.
            replace (str): The replacement string.
            same_name_ok (bool): Whether to allow the same name. Defaults to False.

        Returns:
            File: The renamed file.

        Raises:
            ValueError: If the name is the same and same_name_ok is False.
            FileNotFoundError: If the file does not exist and missing_ok is False.
        """
        new_name = re.sub(pattern, replace, self.name)
        if new_name == self.name and not same_name_ok:
            msg = f"No change made to file name: {self.name}"
            raise ValueError(msg)
        new_path = self.libpath.parent / new_name
        if not self.libpath.exists():
            msg = f"File does not exist: {self.libpath}"
            raise FileNotFoundError(msg)
        self.libpath = self.libpath.rename(new_path)
        return self

    def move_into(self, dir: "Dir") -> "File":
        """Move the file into a directory.

        Args:
            dir (Dir): The directory to move into.

        Returns:
            File: The moved file.
        """
        path = dir.libpath / self.libpath.name
        self.libpath = self.libpath.rename(path)
        return self

    def copy_to(self, file: "File") -> "File":
        """Copy the file to another file.

        Args:
            file (File): The file to copy to.

        Returns:
            File: The copied file.
        """
        shutil.copy(self.libpath, file.libpath)
        self.libpath = file.libpath
        return self

    def copy_into(self, dir: "Dir") -> "File":
        """Copy the file into a directory.

        Args:
            dir (Dir): The directory to copy into.

        Returns:
            File: The copied file.
        """
        path = dir.libpath / self.libpath.name
        shutil.copy(self.libpath, path)
        self.libpath = path
        return self

    def delete(self, missing_ok: bool = False) -> None:
        """Delete the file.

        Args:
            missing_ok (bool): Whether to allow the file to be missing. Defaults to False.
        """
        self.libpath.unlink(missing_ok=missing_ok)

    @property
    def name_no_extension(self) -> str:
        """Get the name of the file without the file extension.

        Returns:
            str: The name of the file without the file extension
        """
        return self.libpath.stem

    @property
    def extension(self) -> str:
        """Get the file extension.

        Returns:
            str: The file extension.
        """
        return self.libpath.suffix

    @property
    def parent(self) -> "Dir":
        """Get the parent directory.

        Returns:
            Dir: The parent directory.
        """
        return Dir(self.libpath.parent)
