from pathlib import Path as PathlibPath


def create_file(parent: PathlibPath, name: str, text: str = "") -> PathlibPath:
    path = parent / name
    path.write_text(text)
    return path


def file_has_text(path: PathlibPath, text: str) -> bool:
    return path.read_text() == text


def create_directory(parent: PathlibPath, name: str) -> PathlibPath:
    path = parent / name
    path.mkdir()
    return path
