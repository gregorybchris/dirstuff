import pytest
from dirstuff import Dir, File, Path
from tests.utilities.temp_utilities import create_directory, create_file, file_has_text


class TestFile:
    def test_construct_file_from_dirpath_raises(self, tmp_path_factory: pytest.TempPathFactory) -> None:
        # Set up file system
        parent_libpath = tmp_path_factory.mktemp("parent")
        libpath_dir = create_directory(parent_libpath, "dir")

        # Attempt to construct file from directory
        with pytest.raises(ValueError, match="Tried to create File from non-file path"):
            File(libpath_dir)

    def test_rename_updates_file_name(self, tmp_path_factory: pytest.TempPathFactory) -> None:
        # Set up file system
        parent_libpath = tmp_path_factory.mktemp("parent")
        libpath = create_file(parent_libpath, "a.txt", text="content")

        # Rename file
        file = File(libpath)
        renamed_file = file.rename("b.txt")

        # Check file libpath has changed and file content has moved correctly
        new_libpath = parent_libpath / "b.txt"
        assert renamed_file.libpath == new_libpath
        assert file_has_text(new_libpath, "content")
        assert not libpath.exists()

    def test_rename_raises_on_same_name(self, tmp_path_factory: pytest.TempPathFactory) -> None:
        # Set up file system
        parent_libpath = tmp_path_factory.mktemp("parent")
        libpath = create_file(parent_libpath, "file.txt", text="content")

        # Rename file to same name
        file = File(libpath)
        with pytest.raises(ValueError, match="No change made to file name: file.txt"):
            file.rename("file.txt")

    def test_rename_does_nothing_on_same_name(self, tmp_path_factory: pytest.TempPathFactory) -> None:
        # Set up file system
        parent_libpath = tmp_path_factory.mktemp("parent")
        libpath = create_file(parent_libpath, "file.txt", text="content")

        # Rename file to same name
        file = File(libpath)
        renamed_file = file.rename("file.txt", same_name_ok=True)

        # Check file libpath has not changed and file content has not moved
        assert renamed_file.libpath == libpath
        assert file_has_text(libpath, "content")

    def test_rename_raises_on_not_found(self, tmp_path_factory: pytest.TempPathFactory) -> None:
        # Set up file system
        parent_libpath = tmp_path_factory.mktemp("parent")
        libpath = parent_libpath / "a.txt"

        # Rename file that does not exist
        file = File(libpath)
        with pytest.raises(FileNotFoundError, match="File does not exist"):
            file.rename("b.txt")

    def test_rename_regex_updates_file_name(self, tmp_path_factory: pytest.TempPathFactory) -> None:
        # Set up file system
        parent_libpath = tmp_path_factory.mktemp("parent")
        libpath = create_file(parent_libpath, "file-a.txt", text="A")

        # Rename file using regex
        file = File(libpath)
        renamed_file = file.rename_regex(r"file-([a-z]*)", r"file-with-\1-name")

        # Check file libpath has changed and file content has moved correctly
        new_libpath = parent_libpath / "file-with-a-name.txt"
        assert renamed_file.libpath == new_libpath
        assert file_has_text(new_libpath, "A")
        assert not libpath.exists()

    def test_rename_regex_raises_on_same_name(self, tmp_path_factory: pytest.TempPathFactory) -> None:
        # Set up file system
        parent_libpath = tmp_path_factory.mktemp("parent")
        libpath = create_file(parent_libpath, "file-a.txt", text="A")

        # Rename file to same name
        file = File(libpath)
        with pytest.raises(ValueError, match="No change made to file name: file-a.txt"):
            file.rename_regex(r"file-([a-z]*)", r"file-\1")

    def test_rename_regex_does_nothing_on_same_name(self, tmp_path_factory: pytest.TempPathFactory) -> None:
        # Set up file system
        parent_libpath = tmp_path_factory.mktemp("parent")
        libpath = create_file(parent_libpath, "file-a.txt", text="A")

        # Rename file to same name
        file = File(libpath)
        renamed_file = file.rename_regex(r"file-([a-z]*)", r"file-\1", same_name_ok=True)

        # Check file libpath has not changed and file content has not moved
        assert renamed_file.libpath == libpath
        assert file_has_text(libpath, "A")

    def test_rename_regex_raises_on_not_found(self, tmp_path_factory: pytest.TempPathFactory) -> None:
        # Set up file system
        parent_libpath = tmp_path_factory.mktemp("parent")
        libpath = parent_libpath / "file.txt"

        # Rename file that does not exist
        file = File(libpath)
        with pytest.raises(FileNotFoundError, match="File does not exist"):
            file.rename_regex(r"file-([a-z]*)", r"file-\1", same_name_ok=True)

    def test_move_into_moves_file_into_dir(self, tmp_path_factory: pytest.TempPathFactory) -> None:
        # Set up file system
        parent_libpath = tmp_path_factory.mktemp("parent")
        libpath_folder_a = create_directory(parent_libpath, "folder-a")
        libpath_file = create_file(libpath_folder_a, "file.txt", text="content")
        libpath_folder_b = create_directory(parent_libpath, "folder-b")

        # Move file from folder_a into folder_b
        file = File(libpath_file)
        dir = Dir(libpath_folder_b)
        moved_file = file.move_into(dir)

        # Check file libpath has changed, file content has moved correctly, old file is removed
        new_libpath = libpath_folder_b / "file.txt"
        assert moved_file.libpath == new_libpath
        assert file_has_text(new_libpath, "content")
        assert not libpath_file.exists()

    def test_move_into_raises_when_dir_does_not_exist(self, tmp_path_factory: pytest.TempPathFactory) -> None:
        # Set up file system
        parent_libpath = tmp_path_factory.mktemp("parent")
        libpath_file = create_file(parent_libpath, "file.txt", text="content")
        libpath_folder = parent_libpath / "folder"

        # Move file into non-existent folder
        file = File(libpath_file)
        dir = Dir(libpath_folder)
        with pytest.raises(FileNotFoundError, match="Destination directory does not exist"):
            file.move_into(dir)

    def test_copy_to_copies_file_to_path(self, tmp_path_factory: pytest.TempPathFactory) -> None:
        # Set up file system
        parent_libpath = tmp_path_factory.mktemp("parent")
        libpath_folder_a = create_directory(parent_libpath, "folder-a")
        libpath_file_a = create_file(libpath_folder_a, "a.txt", text="content")
        libpath_folder_b = create_directory(parent_libpath, "folder-b")
        libpath_file_b = libpath_folder_b / "b.txt"

        # Copy file from folder_a to a path in folder_b
        file = File(libpath_file_a)
        path = Path(libpath_file_b)
        copied_file = file.copy_to(path)

        # Check file libpath has changed, file content has copied correctly, old file still exists
        assert copied_file.libpath == libpath_file_b
        assert file_has_text(libpath_file_a, "content")
        assert file_has_text(libpath_file_b, "content")

    def test_copy_to_raises_on_existing_destination(self, tmp_path_factory: pytest.TempPathFactory) -> None:
        # Set up file system
        parent_libpath = tmp_path_factory.mktemp("parent")
        libpath_folder_a = create_directory(parent_libpath, "folder-a")
        libpath_file_a = create_file(libpath_folder_a, "a.txt", text="A")
        libpath_folder_b = create_directory(parent_libpath, "folder-b")
        libpath_file_b = create_file(libpath_folder_b, "b.txt", text="B")

        # Attempt to copy file from folder_a to a path in folder_b
        file = File(libpath_file_a)
        path = Path(libpath_file_b)
        with pytest.raises(FileExistsError, match="Destination path already exists"):
            file.copy_to(path)

    def test_copy_to_overwrites_existing_destination(self, tmp_path_factory: pytest.TempPathFactory) -> None:
        # Set up file system
        parent_libpath = tmp_path_factory.mktemp("parent")
        libpath_folder_a = create_directory(parent_libpath, "folder-a")
        libpath_file_a = create_file(libpath_folder_a, "a.txt", text="A")
        libpath_folder_b = create_directory(parent_libpath, "folder-b")
        libpath_file_b = create_file(libpath_folder_b, "b.txt", text="B")

        # Copy file from folder_a to a path in folder_b, overwriting existing file
        file = File(libpath_file_a)
        path = Path(libpath_file_b)
        copied_file = file.copy_to(path, overwrite_ok=True)

        # Check file libpath has changed, file content has copied correctly, old file has been overwritten
        assert copied_file.libpath == libpath_file_b
        assert file_has_text(libpath_file_a, "A")
        assert file_has_text(libpath_file_b, "A")

    def test_copy_into_copies_file_into_dir(self, tmp_path_factory: pytest.TempPathFactory) -> None:
        # Set up file system
        parent_libpath = tmp_path_factory.mktemp("parent")
        libpath_folder = create_directory(parent_libpath, "folder")
        libpath_file = create_file(parent_libpath, "file.txt", text="content")

        # Copy file from folder_a into folder_b
        file = File(libpath_file)
        dir = Dir(libpath_folder)
        copied_file = file.copy_into(dir)

        # Check file libpath has changed, file content has copied correctly, old file still exists
        new_libpath = libpath_folder / "file.txt"
        assert copied_file.libpath == new_libpath
        assert file_has_text(new_libpath, "content")
        assert file_has_text(libpath_file, "content")

    def test_copy_into_raises_when_dir_does_not_exist(self, tmp_path_factory: pytest.TempPathFactory) -> None:
        # Set up file system
        parent_libpath = tmp_path_factory.mktemp("parent")
        libpath_file = create_file(parent_libpath, "file.txt", text="content")
        libpath_folder = parent_libpath / "folder"

        # Copy file into non-existent folder
        file = File(libpath_file)
        dir = Dir(libpath_folder)
        with pytest.raises(FileNotFoundError, match="Destination directory does not exist"):
            file.copy_into(dir)

    def test_delete_removes_file(self, tmp_path_factory: pytest.TempPathFactory) -> None:
        # Set up file system
        parent_libpath = tmp_path_factory.mktemp("parent")
        libpath_file = create_file(parent_libpath, "file.txt", text="content")

        # Delete file
        file = File(libpath_file)
        file.delete()

        # Check file has been removed
        assert not libpath_file.exists()

    def test_delete_raises_on_not_found(self, tmp_path_factory: pytest.TempPathFactory) -> None:
        # Set up file system
        parent_libpath = tmp_path_factory.mktemp("parent")
        libpath = parent_libpath / "file.txt"

        # Delete file that does not exist
        file = File(libpath)
        with pytest.raises(FileNotFoundError, match="File does not exist"):
            file.delete()

    def test_delete_does_nothing_on_not_found(self, tmp_path_factory: pytest.TempPathFactory) -> None:
        # Set up file system
        parent_libpath = tmp_path_factory.mktemp("parent")
        libpath = parent_libpath / "file.txt"

        # Delete file that does not exist
        file = File(libpath)
        file.delete(missing_ok=True)

    def test_parent_property_returns_parent_dir(self, tmp_path_factory: pytest.TempPathFactory) -> None:
        # Set up file system
        parent_libpath = tmp_path_factory.mktemp("parent")
        libpath_file = create_file(parent_libpath, "file.txt", text="content")

        # Check parent dir is correct
        file = File(libpath_file)
        assert isinstance(file.parent, Dir)
        assert file.parent.libpath == parent_libpath

    def test_parent_property_raises_on_not_found(self, tmp_path_factory: pytest.TempPathFactory) -> None:
        # Set up file system
        parent_libpath = tmp_path_factory.mktemp("parent")
        libpath = parent_libpath / "file.txt"

        # Check parent dir raises on file not found
        file = File(libpath)
        with pytest.raises(FileNotFoundError, match="File does not exist"):
            file.parent  # noqa: B018

    def test_name_no_extension_property_returns_file_name(self, tmp_path_factory: pytest.TempPathFactory) -> None:
        # Set up file system
        parent_libpath = tmp_path_factory.mktemp("parent")
        libpath_file = create_file(parent_libpath, "file.txt", text="content")

        # Check file name without extension is correct
        file = File(libpath_file)
        assert file.name_no_extension == "file"

    def test_extension_property_returns_file_extension(self, tmp_path_factory: pytest.TempPathFactory) -> None:
        # Set up file system
        parent_libpath = tmp_path_factory.mktemp("parent")
        libpath_file = create_file(parent_libpath, "file.txt", text="content")

        # Check file extension is correct
        file = File(libpath_file)
        assert file.extension == ".txt"

    def test_get_path_for_file(self, tmp_path_factory: pytest.TempPathFactory) -> None:
        # Set up file system
        parent_libpath = tmp_path_factory.mktemp("parent")
        libpath_file = create_file(parent_libpath, "file.txt", text="content")

        # Check file path is correct
        file = File(libpath_file)
        path = file.path
        assert isinstance(path, Path)
        assert path.libpath == libpath_file
