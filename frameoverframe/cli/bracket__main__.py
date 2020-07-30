#!/usr/bin/env python3

import argparse
import os
import shutil
import sys

#import frameoverframe.bracket as bracket

from frameoverframe.bracket import split, merge
from frameoverframe.renumber import renumber


def main():
    '''
        do the main thing
    '''
    parser = argparse.ArgumentParser(
        description='commandline file processor python template ')

    verbs = parser.add_subparsers(dest='verb', help='verbs')

    # split command
    split_parser = verbs.add_parser(
        'split', help='Split one folder into several')

    split_parser.add_argument('-b', '--brackets', required=True, type=int,
                              dest='brackets', help='number of brackets')

    split_parser.add_argument("input", nargs='*',
                              default=None, help="folder(s)")

    # merge command
    merge_parser = verbs.add_parser(
        'merge', help='Merge several folders into one')

    merge_parser.add_argument('-b', '--brackets', required=True, type=int,
                              dest='brackets', help='number of brackets')

    merge_parser.add_argument("input", nargs='*',
                              default=None, help="folder(s)")

    args = parser.parse_args()

    print('args==', args)

    if not args.verb or not args.input or not args.brackets:
        parser.print_help()
        split_parser.print_help()
        merge_parser.print_help()
        return 0

    if args.brackets < 2:
        print('-brackets must be at least 2.')
        return 1

    if args.verb == 'split':

        for single_input in args.input:
            if not os.path.isdir(single_input):
                print('ERROR: input is not a directory: ' + single_input)
                parser.print_help()
                return 1

            split(args.brackets, single_input)

    if args.verb == 'merge':

        print(args.brackets, len(args.input))
        merge(args.input)

    return 0


if __name__ == "__main__":
    sys.exit(main())
