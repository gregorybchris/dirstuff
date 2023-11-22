# DirStuff

## Summarization

Summarize a directory recursively by file size. This tool can be used to quickly search a drive for large files taking up too much space.

## Installation

Install the current PyPI release:

```bash
pip install dirstuff
```

## Usage

```bash
# Run the tree command to summarize a directory
$ dirstuff tree <root-dir>

# Specify the minimum file size (default is 10MB)
$ dirstuff tree <root-dir> --size 750MB
$ dirstuff tree <root-dir> --size 50KB

# Print full absolute paths to directories instead of directory names
$ dirstuff tree <root-dir> --absolute
```

```bash
# Run the list command to find all directories with a matching name
$ dirstuff list <root-dir> <dir-name>

# Specify the minimum file size (default is 10MB)
$ dirstuff list <root-dir> <dir-name> --size 750MB
$ dirstuff list <root-dir> <dir-name> --size 50KB
```

```bash
from dirstuff.os import Path
```

## Examples

### Tree

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

### List

```bash
# List all node_modules folders under the /home/user/my_code directory
$ dirstuff list ~/Documents/Code/Projects/Current node_modules
```

```python
 |-> 419.6 MB > /user/my_code/portfolio/web/node_modules
 |-> 320.3 MB > /user/my_code/fun_project/node_modules
 |-> 298.1 MB > /user/my_code/simple_game/version_2/node_modules
```
