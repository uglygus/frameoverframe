#!/usr/bin/env python3
"""
rename_uniq

commandline interface

"""

import argparse
import os
import errno
import subprocess
import sys

from frameoverframe.rename_uniq import rename_uniq_file, rename_uniq_dir


def main():
    ''' do the main thing '''

    parser = argparse.ArgumentParser(
        description='commandline file processor python template ')

    parser.add_argument("input", nargs='*',
                        default=None, help="folder(s) of files to rename")

    args = parser.parse_args()

    if not args.input:
        parser.print_help()
        return 0

    for single_input in args.input:
        if not  os.path.isdir(single_input):
            print('ERROR: input is not a directory: ' + single_input)
            parser.print_help()
            return 1

        if os.path.isdir(single_input):
            rename_uniq_dir(single_input)


    return 0


if __name__ == "__main__":
    sys.exit(main())