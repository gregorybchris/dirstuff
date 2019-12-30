# DirSum

Summarize a directory recursively by file size. This tool can be used to quickly search a drive for large files taking up too much space.

## Installation

Install the current PyPI release:

```bash
pip install dirsum
```

Or install from source:

```bash
pip install git+https://github.com/gregorybchris/dirsum
```

## Usage

```bash
# Run the dirsum command to summarize a directory
dirsum <path-to-directory>

# Specify the minimum file size (default is 1GB)
dirsum <path-to-directory> --size 750MB
dirsum <path-to-directory> --size 50KB
```
