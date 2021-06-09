#!/usr/bin/env python3
"""
unmix

unmix's images that are stored in the same folder. This helps with Canon folders
which store the CR2 and JPG files in the same folder.

For example:
/fireants/000001.CR2
/fireants/000001.JPG
/fireants/000002.CR2
/fireants/000002.JPG

becomes:
/fireants_CR2/000001.CR2
/fireants_CR2/000002.CR2
/fireants_JPG/000001.JPG
/fireants_JPG/000002.JPG

ignores .DS_Store files

"""

import os
import shutil
import argparse
import sys
import re

from frameoverframe.unmix import unmix


def collect_args():
    """collect commandline arguments"""

    parser = argparse.ArgumentParser(
        description="Unmix's images that are stored in the same folder. This helps with Canon folders which store the CR2 and JPG files in the same folder."
    )

    parser.add_argument(
        "src_dirs",
        nargs="+",
        help="Source directory. ",
    )

    return parser


def main():
    """
    Can be called from the commmandline:
    usage: renumber.py [-h] [-o DST_DIR] [-i] [-s START_AT] [-x PREFIX] [-p PADDING] src_dir

    """

    parser = collect_args()
    args = parser.parse_args()

    for directory in args.src_dirs:
        print("unmixing", directory, "...")
        unmix(directory)


if __name__ == "__main__":
    sys.exit(main())
