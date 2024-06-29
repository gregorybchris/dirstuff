import pytest
from dirstuff import Dir, Path
from tests.utilities.temp_utilities import create_directory


class TestDir:
    def test_rename_updates_dir_name(self, tmp_path_factory: pytest.TempPathFactory) -> None:
        # TODO(chris): Refactor this test
        base_dirpath = tmp_path_factory.mktemp("base")
        path = base_dirpath / "folder_a"
        path.mkdir()
        dir = Dir(path)
        result = dir.rename("folder_b")
        assert result == dir
        new_path = base_dirpath / "folder_b"
        assert not path.exists()
        assert new_path.exists()
        assert dir.libpath == new_path

    # TODO(chris): Add test for rename with existing destination raises
    # TODO(chris): Add test for rename with existing destination does nothing

    def test_rename_regex_updates_dir_name(self, tmp_path_factory: pytest.TempPathFactory) -> None:
        # TODO(chris): Refactor this test
        base_dirpath = tmp_path_factory.mktemp("base")
        path = base_dirpath / "folder_a"
        path.mkdir()
        assert path.exists()
        dir = Dir(path)
        result = dir.rename_regex(r"folder_([a-z]*)", r"folder_with_\1_name")
        assert result == dir
        new_path = base_dirpath / "folder_with_a_name"
        assert not path.exists()
        assert new_path.exists()
        assert dir.libpath == new_path

    # TODO(chris): Add test for rename_regex with existing destination raises
    # TODO(chris): Add test for rename_regex with existing destination does nothing

    def test_move_into_moves_dir_into_dir(self, tmp_path_factory: pytest.TempPathFactory) -> None:
        # TODO(chris): Refactor this test
        base_dirpath = tmp_path_factory.mktemp("base")
        path_a = base_dirpath / "folder_a"
        path_a.mkdir()
        path_b = base_dirpath / "folder_b"
        path_b.mkdir()
        path_c = path_b / "folder_a"
        assert path_a.exists()
        assert not path_c.exists()
        dir_a = Dir(path_a)
        dir_b = Dir(path_b)
        result = dir_a.move_into(dir_b)
        assert result == dir_a
        assert not path_a.exists()
        assert path_c.exists()
        assert dir_a.libpath == path_c

    # TODO(chris): Add test for move_into with missing destination raises

    def test_copy_to_copies_dir_to_path(self, tmp_path_factory: pytest.TempPathFactory) -> None:
        # TODO(chris): Refactor this test
        base_dirpath = tmp_path_factory.mktemp("base")
        path_a = base_dirpath / "folder_a"
        path_a.mkdir()
        path_b = base_dirpath / "folder_b"
        dir_a = Dir(path_a)
        dir_b = Dir(path_b)
        result = dir_a.copy_to(dir_b)
        assert result == dir_a
        assert path_a.exists()
        assert path_b.exists()
        assert dir_a.libpath == path_b

    def test_copy_to_raises_on_existing_destination(self, tmp_path_factory: pytest.TempPathFactory) -> None:
        # TODO(chris): Refactor this test
        base_dirpath = tmp_path_factory.mktemp("base")
        path_a = base_dirpath / "folder_a"
        path_a.mkdir()
        path_b = base_dirpath / "folder_b"
        path_b.mkdir()
        dir_a = Dir(path_a)
        dir_b = Dir(path_b)
        with pytest.raises(FileExistsError):
            dir_a.copy_to(dir_b)

    def test_copy_to_overwrites_existing_destination(self, tmp_path_factory: pytest.TempPathFactory) -> None:
        # TODO(chris): Refactor this test
        base_dirpath = tmp_path_factory.mktemp("base")
        path_a = base_dirpath / "folder_a"
        path_a.mkdir()
        path_b = base_dirpath / "folder_b"
        path_b.mkdir()
        dir_a = Dir(path_a)
        dir_b = Dir(path_b)
        result = dir_a.copy_to(dir_b, overwrite_ok=True)
        assert result == dir_a
        assert path_a.exists()
        assert path_b.exists()
        assert dir_a.name == "folder_b"

    def test_copy_into_copies_dir_into_dir(self, tmp_path_factory: pytest.TempPathFactory) -> None:
        # TODO(chris): Refactor this test
        base_dirpath = tmp_path_factory.mktemp("base")
        path_a = base_dirpath / "folder_a"
        path_a.mkdir()
        path_b = base_dirpath / "folder_b"
        path_b.mkdir()
        path_c = path_b / "folder_a"
        dir_a = Dir(path_a)
        dir_b = Dir(path_b)
        result = dir_a.copy_into(dir_b)
        assert result == dir_a
        assert path_a.exists()
        assert path_c.exists()
        assert dir_a.libpath == path_c

    # TODO(chris): Add test for copy_into with missing destination raises

    def test_delete_removes_dir(self, tmp_path_factory: pytest.TempPathFactory) -> None:
        # TODO(chris): Refactor this test
        base_dirpath = tmp_path_factory.mktemp("base")
        path_a = base_dirpath / "folder_a"
        path_a.mkdir()
        assert path_a.exists()
        dir_a = Dir(path_a)
        dir_a.delete()
        assert not path_a.exists()

    def test_walk_returns_children(self, tmp_path_factory: pytest.TempPathFactory) -> None:
        # TODO(chris): Refactor this test
        base_dirpath = tmp_path_factory.mktemp("base")
        filepath_a = base_dirpath / "file_a.txt"
        filepath_b = base_dirpath / "file_b.txt"
        dirpath_a = base_dirpath / "path"
        dirpath_a.mkdir()
        filepath_a.write_text("A")
        filepath_b.write_text("B")
        dir = Dir(base_dirpath)
        walk_files, walk_dirs = dir.walk()
        assert len(walk_files) == 2
        assert len(walk_dirs) == 1

    def test_make_creates_a_dir(self, tmp_path_factory: pytest.TempPathFactory) -> None:
        # TODO(chris): Refactor this test
        base_dirpath = tmp_path_factory.mktemp("base")
        path = base_dirpath / "path"
        dir = Dir(path)
        assert not path.exists()
        dir.make()
        assert path.exists()

    def test_parent_property_returns_parent_dir(self, tmp_path_factory: pytest.TempPathFactory) -> None:
        # Set up file system
        parent_libpath = tmp_path_factory.mktemp("base")
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
