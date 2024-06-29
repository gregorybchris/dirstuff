<div align="center">
  <img src="assets/dirstuff-banner.png">
  <h1>dirstuff</h1>

  <p>
    <strong>utilities for filesystem operations</strong>
  </p>

  <br>
  <div>
    <a href="https://badge.fury.io/py/dirstuff"><img src="https://badge.fury.io/py/dirstuff.svg" alt="PyPI"></a>
    <a href="https://pepy.tech/project/dirstuff"><img src="https://pepy.tech/badge/dirstuff" alt="Downloads"></a>
  </div>
  <br>
</div>

## Installation

Install the current PyPI release:

```bash
pip install dirstuff
```

## Path utilities

dirstuff provides some Python utilities for interacting with the filesystem.

- rename
- move
- copy
- delete
- walk

### Rename files with a regex

In this example we iterate over nested folders that contain .txt files and rename them to have .md extensions.

```python
from dirstuff import Dir

d = Dir("my_folder")
for sub in d.iter_dirs():
    for f in sub.iter_files():
        f.rename_regex(r"([a-z]*)\.txt", r"\1.md")
```

### Delete a folder

No need to switch between `pathlib` and `shutil` packages. All filesystem utilities are available on the `Dir` class.

```python
from dirstuff import Dir

d = Dir("my_folder")
d.delete()
```

## Summarization

### Tree

Summarize a directory recursively by file size. This tool can be used to quickly search a drive for large files taking up too much space.

```bash
# Summarize the /home/user/my_documents directory
# showing only directories greater than 20MB in size
$ dirstuff tree /home/user/my_documents --size 20MB
```

```python
|->  69.0 GB > my_documents
    |->  67.8 GB > movies
        |->  62.0 GB > from_the_internet
        |->   5.8 GB > home_movies
    |-> 638.1 MB > photos
        |-> 368.2 MB > rock_concert
        |-> 251.6 MB > vacation_2019
        |->  18.4 MB > family_photos
    |-> 521.6 MB > work
        |-> 263.8 MB > boring_docs
        |-> 257.7 MB > reports
    |->  22.5 MB > games
```

> You can show the full absolute paths with `--absolute`

### Search

Search for all folders with a matching name.

```bash
# List all node_modules folders under the /code/projects directory
$ dirstuff search /code/projects node_modules --absolute
```

```python
 |-> 419.6 MB > /code/projects/portfolio/web/node_modules
 |-> 320.3 MB > /code/projects/fun_project/node_modules
 |-> 298.1 MB > /code/projects/simple_game/version_2/node_modules
```

> The same `--size` option also works with the search command
