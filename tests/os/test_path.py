import pytest
from dirstuff import Path


class TestPath:
    def test_constructor_accepts_libpath(self, tmp_path_factory: pytest.TempPathFactory) -> None:
        libpath = tmp_path_factory.mktemp("folder")
        path = Path(libpath)
        assert path.libpath == libpath

    def test_constructor_accepts_str_path(self, tmp_path_factory: pytest.TempPathFactory) -> None:
        libpath = tmp_path_factory.mktemp("folder")
        str_path = str(libpath)
        path = Path(str_path)
        assert path.libpath == libpath

    def test_constructor_accepts_path(self, tmp_path_factory: pytest.TempPathFactory) -> None:
        libpath = tmp_path_factory.mktemp("folder")
        path = Path(libpath)
        assert path.libpath == libpath

    def test_parent_property_returns_parent_path(self, tmp_path_factory: pytest.TempPathFactory) -> None:
        parent_libpath = tmp_path_factory.mktemp("parent")
        child_libpath = parent_libpath / "child"
        path = Path(child_libpath)
        assert path.parent.libpath == parent_libpath

    def test_name_property_returns_path_name(self, tmp_path_factory: pytest.TempPathFactory) -> None:
        libpath = tmp_path_factory.mktemp("folder")
        path = Path(libpath)
        assert path.name == libpath.name

    def test_get_path_str_repr(self, tmp_path_factory: pytest.TempPathFactory) -> None:
        libpath = tmp_path_factory.mktemp("folder")
        path = Path(libpath)
        assert str(path) == str(libpath)
