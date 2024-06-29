import pytest
from dirstuff import Dir


class TestDir:
    def test_dir_rename(self, tmp_path_factory: pytest.TempPathFactory) -> None:
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

    def test_dir_rename_regex(self, tmp_path_factory: pytest.TempPathFactory) -> None:
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

    def test_dir_move(self, tmp_path_factory: pytest.TempPathFactory) -> None:
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

    def test_dir_copy_to(self, tmp_path_factory: pytest.TempPathFactory) -> None:
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

    def test_dir_copy_into(self, tmp_path_factory: pytest.TempPathFactory) -> None:
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

    def test_dir_delete(self, tmp_path_factory: pytest.TempPathFactory) -> None:
        base_dirpath = tmp_path_factory.mktemp("base")
        path_a = base_dirpath / "folder_a"
        path_a.mkdir()
        assert path_a.exists()
        dir_a = Dir(path_a)
        dir_a.delete()
        assert not path_a.exists()

    def test_dir_walk(self, tmp_path_factory: pytest.TempPathFactory) -> None:
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

    def test_dir_make(self, tmp_path_factory: pytest.TempPathFactory) -> None:
        base_dirpath = tmp_path_factory.mktemp("base")
        path = base_dirpath / "path"
        dir = Dir(path)
        assert not path.exists()
        dir.make()
        assert path.exists()

    def test_dir_parent(self, tmp_path_factory: pytest.TempPathFactory) -> None:
        base_dirpath = tmp_path_factory.mktemp("base")
        dirpath = base_dirpath / "my_dir"
        dir = Dir(dirpath)
        parent_dirpath = dir.parent
        assert parent_dirpath.libpath == base_dirpath
