#trimws

### Trimming of trailing white space in text files


## About
This script will recursively remove all trailing white spaces in all text files in a given directory. Binary files are skipped. Files are identified as text or binary by mimetypes.


## Installation
 * System requirement: Python 3.x


## Usage:

   usage: trimws.py [-h] filepath [filepath ...]

Trims trailing whitespace from text files. Checks files mimetype to determine
if they are text files. Recurses into directories.

positional arguments:
  filepath    files or directories

optional arguments:
  -h, --help  show this help message and exit

## License
See [UNLICENSE](UNLICENSE) file
