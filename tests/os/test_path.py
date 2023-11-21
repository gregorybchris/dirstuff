# pylint: disable=redefined-builtin
from pytest import TempPathFactory

from dirstuff.os import Dir, File


class TestFile:
    def test_file_rename(self, tmp_path_factory: TempPathFactory) -> None:
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

    def test_file_regex_rename(self, tmp_path_factory: TempPathFactory) -> None:
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

    def test_file_move_into(self, tmp_path_factory: TempPathFactory) -> None:
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

    def test_file_copy_to(self, tmp_path_factory: TempPathFactory) -> None:
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

    def test_file_copy_into(self, tmp_path_factory: TempPathFactory) -> None:
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

    def test_file_delete(self, tmp_path_factory: TempPathFactory) -> None:
        base_dirpath = tmp_path_factory.mktemp("base")
        path = base_dirpath / "file_a.txt"
        path.write_text("A")
        assert path.exists()
        file = File(path)
        file.delete()
        assert not path.exists()


class TestDir:
    def test_dir_rename(self, tmp_path_factory: TempPathFactory) -> None:
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

    def test_dir_rename_regex(self, tmp_path_factory: TempPathFactory) -> None:
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

    def test_dir_move(self, tmp_path_factory: TempPathFactory) -> None:
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

    def test_dir_copy_to(self, tmp_path_factory: TempPathFactory) -> None:
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

    def test_dir_copy_into(self, tmp_path_factory: TempPathFactory) -> None:
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

    def test_dir_delete(self, tmp_path_factory: TempPathFactory) -> None:
        base_dirpath = tmp_path_factory.mktemp("base")
        path_a = base_dirpath / "folder_a"
        path_a.mkdir()
        assert path_a.exists()
        dir_a = Dir(path_a)
        dir_a.delete()
        assert not path_a.exists()

    def test_dir_walk(self, tmp_path_factory: TempPathFactory) -> None:
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

    def test_dir_make(self, tmp_path_factory: TempPathFactory) -> None:
        base_dirpath = tmp_path_factory.mktemp("base")
        path = base_dirpath / "path"
        dir = Dir(path)
        assert not path.exists()
        dir.make()
        assert path.exists()
