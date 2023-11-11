# DirSum

Summarize a directory recursively by file size. This tool can be used to quickly search a drive for large files taking up too much space.

## Installation

Install the current PyPI release:

```bash
pip install dirsum
```

## Usage

```bash
# Run the summarize command to summarize a directory
dirsum summarize <path-to-directory>

# Specify the minimum file size (default is 1GB)
dirsum summarize <path-to-directory> --size 750MB
dirsum summarize <path-to-directory> --size 50KB

# Print full absolute paths to directories instead of directory names
dirsum summarize <path-to-directory> --absolute
```

## Example Output

```bash
# Summarize the /home/user/my_documents directory
# showing only directories greater than 20MB in size
dirsum summarize /home/user/my_documents --size 20MB
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
