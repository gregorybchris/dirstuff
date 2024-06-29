import pytest
from dirstuff import Dir, File


class TestFile:
    def test_file_rename(self, tmp_path_factory: pytest.TempPathFactory) -> None:
        base_dirpath = tmp_path_factory.mktemp("base")
        path_a = base_dirpath / "file_a.txt"
        path_a.write_text("A")
        assert path_a.exists()
        file = File(path_a)
        result = file.rename("file_b.txt")
        assert result == file
        path_b = base_dirpath / "file_b.txt"
        assert not path_a.exists()
        assert path_b.exists()
        assert file.libpath == path_b

    def test_file_rename_regex(self, tmp_path_factory: pytest.TempPathFactory) -> None:
        base_dirpath = tmp_path_factory.mktemp("base")
        path_a = base_dirpath / "file_a.txt"
        path_a.write_text("A")
        assert path_a.exists()
        file = File(path_a)
        result = file.rename_regex(r"file_([a-z]*)", r"file_with_\1_name")
        assert result == file
        path_b = base_dirpath / "file_with_a_name.txt"
        assert not path_a.exists()
        assert path_b.exists()
        assert file.libpath == path_b

    def test_file_move_into(self, tmp_path_factory: pytest.TempPathFactory) -> None:
        base_dirpath = tmp_path_factory.mktemp("base")
        dirpath_a = base_dirpath / "folder_a"
        dirpath_a.mkdir()
        dirpath_b = base_dirpath / "folder_b"
        dirpath_b.mkdir()
        path_a = dirpath_a / "file.txt"
        path_b = dirpath_b / "file.txt"
        path_a.write_text("A")
        assert path_a.exists()
        assert not path_b.exists()
        file = File(path_a)
        dir_b = Dir(dirpath_b)
        result = file.move_into(dir_b)
        assert result == file
        assert not path_a.exists()
        assert path_b.exists()
        assert file.libpath == path_b

    def test_file_copy_to(self, tmp_path_factory: pytest.TempPathFactory) -> None:
        base_dirpath = tmp_path_factory.mktemp("base")
        path_a = base_dirpath / "file_a.txt"
        path_a.write_text("A")
        assert path_a.exists()
        file_a = File(path_a)
        path_b = base_dirpath / "file_b.txt"
        file_b = File(path_b)
        result = file_a.copy_to(file_b)
        assert result == file_a
        assert path_a.exists()
        assert path_b.exists()
        assert file_a.libpath == path_b

    def test_file_copy_into(self, tmp_path_factory: pytest.TempPathFactory) -> None:
        base_dirpath = tmp_path_factory.mktemp("base")
        path_a = base_dirpath / "file.txt"
        path_a.write_text("A")
        assert path_a.exists()
        path_b = base_dirpath / "folder"
        path_b.mkdir()
        path_c = path_b / "file.txt"
        assert path_a.exists()
        file = File(path_a)
        dir = Dir(path_b)
        result = file.copy_into(dir)
        assert result == file
        assert path_a.exists()
        assert path_c.exists()
        assert file.libpath == path_c

    def test_file_delete(self, tmp_path_factory: pytest.TempPathFactory) -> None:
        base_dirpath = tmp_path_factory.mktemp("base")
        path = base_dirpath / "file_a.txt"
        path.write_text("A")
        assert path.exists()
        file = File(path)
        file.delete()
        assert not path.exists()

    def test_file_parent(self, tmp_path_factory: pytest.TempPathFactory) -> None:
        base_dirpath = tmp_path_factory.mktemp("base")
        filepath = base_dirpath / "file.txt"
        file = File(filepath)
        parent_dir = file.parent
        assert parent_dir.libpath == base_dirpath

    def test_file_name_no_extension(self, tmp_path_factory: pytest.TempPathFactory) -> None:
        base_dirpath = tmp_path_factory.mktemp("base")
        filepath = base_dirpath / "my-file.txt"
        file = File(filepath)
        assert file.name_no_extension == "my-file"

    def test_file_extension(self, tmp_path_factory: pytest.TempPathFactory) -> None:
        base_dirpath = tmp_path_factory.mktemp("base")
        filepath = base_dirpath / "my-file.txt"
        file = File(filepath)
        assert file.extension == ".txt"
