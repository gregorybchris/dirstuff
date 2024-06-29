from typing import Iterator

import pytest
from dirstuff import Dir, Path
from tests.utilities.temp_utilities import create_directory, create_file


class TestDir:
    def test_construct_dir_from_filepath_raises(self, tmp_path_factory: pytest.TempPathFactory) -> None:
        # Set up file system
        parent_libpath = tmp_path_factory.mktemp("parent")
        libpath_file = create_file(parent_libpath, "a.txt", text="content")

        # Attempt to construct file from directory
        with pytest.raises(ValueError, match="Tried to create Dir from non-dir path"):
            Dir(libpath_file)

    def test_rename_updates_dir_name(self, tmp_path_factory: pytest.TempPathFactory) -> None:
        # Set up file system
        parent_libpath = tmp_path_factory.mktemp("parent")
        libpath = create_directory(parent_libpath, "folder-a")

        # Rename dir
        dir = Dir(libpath)
        renamed_dir = dir.rename("folder-b")

        # Check dir libpath has changed and old dir is gone
        new_libpath = parent_libpath / "folder-b"
        assert renamed_dir.libpath == new_libpath
        assert not libpath.exists()

    def test_rename_raises_on_same_name(self, tmp_path_factory: pytest.TempPathFactory) -> None:
        # Set up file system
        parent_libpath = tmp_path_factory.mktemp("parent")
        libpath = create_directory(parent_libpath, "folder")

        # Rename dir to same name
        dir = Dir(libpath)
        with pytest.raises(ValueError, match="No change made to dir name: folder"):
            dir.rename("folder")

    def test_rename_does_nothing_on_same_name(self, tmp_path_factory: pytest.TempPathFactory) -> None:
        # Set up file system
        parent_libpath = tmp_path_factory.mktemp("parent")
        libpath = create_directory(parent_libpath, "folder-a")

        # Rename file to same name
        dir = Dir(libpath)
        renamed_dir = dir.rename("folder-a", same_name_ok=True)

        # Check file libpath has not changed
        assert renamed_dir.libpath == libpath

    def test_rename_raises_on_dir_not_found(self, tmp_path_factory: pytest.TempPathFactory) -> None:
        # Set up file system
        parent_libpath = tmp_path_factory.mktemp("parent")
        libpath = parent_libpath / "a.txt"

        # Rename file that does not exist
        dir = Dir(libpath)
        with pytest.raises(FileNotFoundError, match="Dir does not exist"):
            dir.rename("b.txt")

    def test_rename_regex_updates_dir_name(self, tmp_path_factory: pytest.TempPathFactory) -> None:
        # Set up file system
        parent_libpath = tmp_path_factory.mktemp("parent")
        libpath = create_directory(parent_libpath, "folder-a")

        # Rename dir
        dir = Dir(libpath)
        renamed_dir = dir.rename_regex(r"folder-([a-z]*)", r"folder-with-\1-name")

        # Check dir libpath has changed and old dir is gone
        new_libpath = parent_libpath / "folder-with-a-name"
        assert renamed_dir.libpath == new_libpath
        assert not libpath.exists()

    def test_rename_regex_raises_on_same_name(self, tmp_path_factory: pytest.TempPathFactory) -> None:
        # Set up file system
        parent_libpath = tmp_path_factory.mktemp("parent")
        libpath = create_directory(parent_libpath, "folder-a")

        # Rename dir to same name
        dir = Dir(libpath)
        with pytest.raises(ValueError, match="No change made to dir name: folder"):
            dir.rename_regex(r"folder-([a-z]*)", r"folder-\1")

    def test_rename_regex_does_nothing_on_same_name(self, tmp_path_factory: pytest.TempPathFactory) -> None:
        # Set up file system
        parent_libpath = tmp_path_factory.mktemp("parent")
        libpath = create_directory(parent_libpath, "folder-a")

        # Rename dir to same name
        dir = Dir(libpath)
        renamed_dir = dir.rename_regex(r"folder-([a-z]*)", r"folder-\1", same_name_ok=True)

        # Check djr libpath has not changed
        assert renamed_dir.libpath == libpath

    def test_rename_regex_raises_on_not_found(self, tmp_path_factory: pytest.TempPathFactory) -> None:
        # Set up file system
        parent_libpath = tmp_path_factory.mktemp("parent")
        libpath = parent_libpath / "folder"

        # Rename file that does not exist
        dir = Dir(libpath)
        with pytest.raises(FileNotFoundError, match="Dir does not exist"):
            dir.rename_regex(r"folder-([a-z]*)", r"folder-\1", same_name_ok=True)

    def test_move_into_moves_dir_into_dir(self, tmp_path_factory: pytest.TempPathFactory) -> None:
        # Set up file system
        parent_libpath = tmp_path_factory.mktemp("parent")
        libpath_a = create_directory(parent_libpath, "folder-a")
        libpath_b = create_directory(parent_libpath, "folder-b")

        # Move dir into dir
        dir_a = Dir(libpath_a)
        dir_b = Dir(libpath_b)
        moved_dir = dir_a.move_into(dir_b)

        # Check dir libpath has changed
        new_libpath = libpath_b / "folder-a"
        assert moved_dir.libpath == new_libpath
        assert not libpath_a.exists()
        assert new_libpath.exists()

    def test_move_into_raises_when_dir_does_not_exist(self, tmp_path_factory: pytest.TempPathFactory) -> None:
        # Set up file system
        parent_libpath = tmp_path_factory.mktemp("parent")
        libpath_a = create_directory(parent_libpath, "folder-a")
        libpath_b = parent_libpath / "folder-b"

        # Move Dir into non-existent folder
        dir_a = Dir(libpath_a)
        dir_b = Dir(libpath_b)
        with pytest.raises(FileNotFoundError, match="Destination directory does not exist"):
            dir_a.move_into(dir_b)

    def test_copy_to_copies_dir_to_path(self, tmp_path_factory: pytest.TempPathFactory) -> None:
        # Set up file system
        parent_libpath = tmp_path_factory.mktemp("parent")
        libpath_a = create_directory(parent_libpath, "folder-a")
        libpath_b = parent_libpath / "folder-b"

        # Copy dir to path
        dir = Dir(libpath_a)
        path = Path(libpath_b)
        copied_dir = dir.copy_to(path)

        # Check dir libpath has changed and old libpath still exists
        assert copied_dir.libpath == libpath_b
        assert libpath_a.exists()
        assert libpath_b.exists()

    def test_copy_to_raises_on_existing_destination(self, tmp_path_factory: pytest.TempPathFactory) -> None:
        # Set up file system
        parent_libpath = tmp_path_factory.mktemp("parent")
        libpath_a = create_directory(parent_libpath, "folder-a")
        libpath_b = create_directory(parent_libpath, "folder-b")

        # Copy dir to path
        dir = Dir(libpath_a)
        path = Path(libpath_b)
        with pytest.raises(FileExistsError, match="Destination path already exists"):
            dir.copy_to(path)

    def test_copy_to_overwrites_existing_destination(self, tmp_path_factory: pytest.TempPathFactory) -> None:
        # Set up file system
        parent_libpath = tmp_path_factory.mktemp("parent")
        libpath_a = create_directory(parent_libpath, "folder-a")
        libpath_b = create_directory(parent_libpath, "folder-b")

        # Copy dir to path
        dir = Dir(libpath_a)
        path = Path(libpath_b)
        copied_dir = dir.copy_to(path, overwrite_ok=True)

        # Check dir libpath has changed and old libpath still exists
        assert copied_dir.libpath == libpath_b
        assert libpath_a.exists()
        assert libpath_b.exists()

    def test_copy_into_copies_dir_into_dir(self, tmp_path_factory: pytest.TempPathFactory) -> None:
        # Set up file system
        parent_libpath = tmp_path_factory.mktemp("parent")
        libpath_a = create_directory(parent_libpath, "folder-a")
        libpath_b = create_directory(parent_libpath, "folder-b")

        # Copy dir into dir
        dir_a = Dir(libpath_a)
        dir_b = Dir(libpath_b)
        copied_dir = dir_a.copy_into(dir_b)

        # Check dir libpath has changed and old libpath still exists
        new_libpath = libpath_b / "folder-a"
        assert copied_dir.libpath == new_libpath
        assert libpath_a.exists()
        assert new_libpath.exists()

    def test_copy_into_raises_when_dir_does_not_exist(self, tmp_path_factory: pytest.TempPathFactory) -> None:
        # Set up file system
        parent_libpath = tmp_path_factory.mktemp("parent")
        libpath_a = create_directory(parent_libpath, "folder-a")
        libpath_b = parent_libpath / "folder-b"

        # Copy Dir into non-existent folder
        dir_a = Dir(libpath_a)
        dir_b = Dir(libpath_b)
        with pytest.raises(FileNotFoundError, match="Destination directory does not exist"):
            dir_a.copy_into(dir_b)

    def test_delete_removes_dir(self, tmp_path_factory: pytest.TempPathFactory) -> None:
        # Set up file system
        parent_libpath = tmp_path_factory.mktemp("parent")
        libpath = create_directory(parent_libpath, "folder")

        # Delete dir
        dir = Dir(libpath)
        dir.delete()

        # Check dir is gone
        assert not libpath.exists()

    def test_delete_raises_on_not_found(self) -> None:
        # Set up file system
        libpath = Path("folder")

        # Delete dir that does not exist
        dir = Dir(libpath)
        with pytest.raises(FileNotFoundError, match="Dir does not exist"):
            dir.delete()

    def test_delete_does_nothing_on_not_found(self) -> None:
        # Set up file system
        libpath = Path("folder")

        # Delete dir that does not exist
        dir = Dir(libpath)
        dir.delete(missing_ok=True)

        # Check nothing happened
        assert not libpath.exists()

    def test_walk_returns_children(self, tmp_path_factory: pytest.TempPathFactory) -> None:
        # Set up file system
        parent_libpath = tmp_path_factory.mktemp("parent")
        create_directory(parent_libpath, "folder-a")
        create_directory(parent_libpath, "folder-b")
        create_file(parent_libpath, "a.txt", text="content")
        create_file(parent_libpath, "b.txt", text="content")
        create_file(parent_libpath, "c.txt", text="content")

        # Get child files and dirs
        dir = Dir(parent_libpath)
        walked_files, walked_dirs = dir.walk()

        # Check walk returns children
        assert len(walked_files) == 3
        assert len(walked_dirs) == 2

    def test_iter_dirs_returns_dirs(self, tmp_path_factory: pytest.TempPathFactory) -> None:
        # Set up file system
        parent_libpath = tmp_path_factory.mktemp("parent")
        create_directory(parent_libpath, "folder-a")
        create_directory(parent_libpath, "folder-b")
        create_file(parent_libpath, "a.txt", text="content")

        # Get child dirs
        dir = Dir(parent_libpath)
        dirs_iterator = dir.iter_dirs()

        # Check iter_dirs returns dirs
        assert isinstance(dirs_iterator, Iterator)
        walked_dirs = list(dirs_iterator)
        assert len(walked_dirs) == 2

    def test_iter_files_returns_files(self, tmp_path_factory: pytest.TempPathFactory) -> None:
        # Set up file system
        parent_libpath = tmp_path_factory.mktemp("parent")
        create_directory(parent_libpath, "folder-a")
        create_file(parent_libpath, "a.txt", text="content")
        create_file(parent_libpath, "b.txt", text="content")
        create_file(parent_libpath, "c.txt", text="content")

        # Get child files
        dir = Dir(parent_libpath)
        files_iterator = dir.iter_files()

        # Check iter_files returns files
        assert isinstance(files_iterator, Iterator)
        walked_files = list(files_iterator)
        assert len(walked_files) == 3

    def test_make_creates_a_dir(self, tmp_path_factory: pytest.TempPathFactory) -> None:
        # Set up file system
        parent_libpath = tmp_path_factory.mktemp("parent")
        libpath = parent_libpath / "folder"
        assert not libpath.exists()

        # Create the dir
        dir = Dir(libpath)
        dir.make()

        # Check the dir was created
        assert libpath.exists()

    def test_parent_property_returns_parent_dir(self, tmp_path_factory: pytest.TempPathFactory) -> None:
        # Set up file system
        parent_libpath = tmp_path_factory.mktemp("parent")
        libpath = create_directory(parent_libpath, "folder")

        # Check parent property returns parent dir
        dir = Dir(libpath)
        assert dir.parent.libpath == parent_libpath

    def test_parent_property_raises_on_file_not_found(self) -> None:
        # Set up file system
        libpath = Path("folder")

        # Check parent dir raises on file not found
        dir = Dir(libpath)
        with pytest.raises(FileNotFoundError, match="Dir does not exist"):
            dir.parent  # noqa: B018

    def test_get_path_for_file(self, tmp_path_factory: pytest.TempPathFactory) -> None:
        # Set up file system
        parent_libpath = tmp_path_factory.mktemp("parent")
        libpath_dir = parent_libpath / "folder"

        # Check dir path is correct
        dir = Dir(libpath_dir)
        path = dir.path
        assert isinstance(path, Path)
        assert path.libpath == libpath_dir
