#!/usr/bin/env python3

"""
Recombines folders of images

        accepts a list of directories to be combined and renumbered. Combines files into
        directories with max_files in each directory.


"""


import os
import shutil
import argparse
import sys
import re
import math
from pathlib import Path

from frameoverframe.renumber import renumber
#from rename_uniq import rename_uniq_dir

from frameoverframe.recombine import recombine


def dir_path(path):
    ''' for argparse directory type test. '''
    if os.path.isdir(path):
        return path
    else:
        raise argparse.ArgumentTypeError(f"readable_dir:{path} is not a valid path")


def main():
    '''
        Can be called from the commmandline:
    usage: renumber.py [-h] [-o DST_DIR] [-i] [-s START_AT] [-x PREFIX] [-p PADDING] src_dir src_dir src_dir ...

    '''
    parser = argparse.ArgumentParser()

    parser.add_argument('src_dirs', nargs='+', type=dir_path,
                        help="Source directories. ",
                        )

    parser.add_argument("-m", "--max_files", type=int, default=10000,
                        help="Max number of files per directory. (default 100000)",
                        )

    parser.add_argument("-o", "--dst_dir", type=str, default=None,
                        help="Destination directory",
                        )

    parser.add_argument("--copy_files", action="store_true", default=False,
                        help="Copy files to a new direcotory otherwise they are moved. Default: False",
                        )

    parser.add_argument("-x", "--prefix", type=str, default=':folder',
                        help="Prefix. (default no prefix). '' empty string will strip any existing prefix. The special word :folder will use the enclosing first folder's name as the prefix. default :folder",
                        )

    parser.add_argument("-p", "--padding", type=int, default=5,
                        help="How many digits for number. (default 5) eg. 00001.jpg",
                        )

    args = parser.parse_args()

   # print('args=', args)

    recombine(
        args.src_dirs,
        max_files=args.max_files,
        dst_dir=args.dst_dir,
        copy_files=args.copy_files,
        prefix=args.prefix,
        padding=args.padding,
    )


if __name__ == "__main__":
    sys.exit(main())