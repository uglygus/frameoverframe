#!/usr/bin/env python3
"""
thin

copies file like cp but skips files. Copy every other file, or every 10th file, etc
Used to thin timelapses that have too many frames for their movement.
Timelapses we end up using at 10x or 20x speed should be thinned.

"""

import argparse
import os
import re
import shutil
import sys
import uuid

from frameoverframe.thin import thin


def collect_args():
    """ collect commandline arguments """

    parser = argparse.ArgumentParser()

    parser.add_argument('src_dir', nargs='+',
        help="Source directory. ")

    parser.add_argument( '-e','--every', type=int, required=True,
        help="copy every nth file")

    parser.add_argument( "-o", "--dst_dir", type=str, default=None,
        help="Destination directory")

    parser.add_argument( "--inplace", action="store_false", default=False,
        help="Copy files to a new direcotory otherwise they are renamed inplace. (default False)",)

    return parser

def main():
    """
    Can be called from the commmandline:
    usage: renumber.py [-h] [-o DST_DIR] [-i] [-s START_AT] [-x PREFIX] [-p PADDING] src_dir

    """

    parser = collect_args()
    args = parser.parse_args()

    print(f"{args=}")

    thin(
        args.src_dir,
        args.every,
        dst_dir = args.dst_dir,
        inplace = args.inplace,
    )

if __name__ == "__main__":
    sys.exit(main())
