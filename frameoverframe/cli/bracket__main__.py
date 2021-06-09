#!/usr/bin/env python3
"""
    bracket - module docstring

"""

import argparse
import os
import sys

from frameoverframe.bracket import merge, split


def collect_args():
    """collect commandline arguments"""

    parser = argparse.ArgumentParser(description="commandline file processor python template ")

    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument("-s", "--split", action="store_true", dest="split", help="split the folder")

    group.add_argument("-m", "--merge", action="store_true", dest="merge", help="merge the folders")

    parser.add_argument(
        "-b", "--brackets", required=True, type=int, dest="brackets", help="number of brackets"
    )

    parser.add_argument("input", nargs="*", default=None, help="folder(s)")

    return parser


def main():
    """do the main thing"""

    parser = collect_args()
    args = parser.parse_args()

    print("args==", args)

    if args.brackets < 2:
        print("-brackets must be at least 2.")
        return 1

    if args.split:
        for single_input in args.input:
            if not os.path.isdir(single_input):
                print("ERROR: input is not a directory: " + single_input)
                parser.print_help()
                return 1

            split(args.brackets, single_input)

    if args.merge:
        print(args.brackets, len(args.input))
        merge(args.input)

    return 0


if __name__ == "__main__":
    sys.exit(main())
