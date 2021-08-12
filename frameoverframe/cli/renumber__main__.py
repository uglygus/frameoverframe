#!/usr/bin/env python3
"""
renumber

Renumbers image sequences by renaming them sequentially.
Can be used as a module or a called from the commandline.

For example: prodeng01.jpg prodeng11.png prodeng27.jpg
$renumber.py .
Would become: (split by sequence)
prodeng_00001.jpg prodeng_00002.jpg prodeng_00003.jpg

Includes options for adding padding, rename files in place or create new ones,
Includes options for adding padding, rename files in place or create new ones,
specify the start number of sequence etc. Please read through the renumber()
docstring for more.

"""

import argparse
import os
import sys
import logging.config

#   logging.config.dictConfig() and logging.getLogger()
#   must come after importing LOGGING_CONFIG
#   but before any other frameoverframe modules.
from frameoverframe.config import LOGGING_CONFIG

logging.config.dictConfig(LOGGING_CONFIG)
log = logging.getLogger("frameoverframe")

from frameoverframe.renumber import renumber

def collect_args():
    """collect commandline arguments"""

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "src_dirs",
        nargs="+",
        help="Source directory. ",
    )

    parser.add_argument(
        "-o",
        "--dst_dir",
        type=str,
        default=None,
        help="Destination directory",
    )

    parser.add_argument(
        "--safe",
        action="store_true",
        default=False,
        help="Copy files to a new direcotory otherwise they are renamed inplace. (default False)",
    )

    parser.add_argument(
        "-s",
        "--sort-method",
        type=str,
        default=None,
        choices=["name", "exif_date"],
        help="Method to use when sorting files: 'name' or 'exif_date' ",
    )

    parser.add_argument(
        "-S",
        "--start_at",
        type=int,
        default=0,
        help="Start number for renaming sequence. (default 0)",
    )

    parser.add_argument(
        "-x",
        "--prefix",
        type=str,
        default=None,
        help="Prefix. (default no prefix). '' empty string will strip any "
        "existing prefix. The special word :folder will use the enclosing "
        "folder's name as the prefix.",
    )

    parser.add_argument(
        "-p",
        "--padding",
        type=int,
        default=5,
        help="How many digits for number. (default 5) eg. 00001.jpg",
    )

    verbosity = parser.add_mutually_exclusive_group()
    verbosity.add_argument(
        "--quiet",
        "-q",
        action="store_const",
        const=logging.WARN,
        dest="loglevel",
        help="Only output when necessary.",
    )

    verbosity.add_argument(
        "--verbose",
        "-v",
        action="store_const",
        const=logging.DEBUG,
        dest="loglevel",
        help="Increase output verbosity.",
    )

    parser.set_defaults(loglevel=logging.INFO)
    args = parser.parse_args()

    return args

def main():
    """
    Can be called from the commmandline:
    usage: renumber.py [-h] [-o DST_DIR] [-i] [-s START_AT] [-x PREFIX] [-p PADDING] src_dir

    """


    args = collect_args()
    log.setLevel(args.loglevel)

    log.debug(f"args= {args} -- {log.level=}")

    for directory in args.src_dirs:
        log.info(f"renumbering {directory} ...")


        print('args.prefix=', args.prefix)
        input('...')
        if args.prefix == ":folder":
            prefix = os.path.basename(os.path.normpath(directory))
        else:
            prefix=args.prefix
#            args.prefix = prefix


        try:
            renumber(
                directory,
                dst_dir=args.dst_dir,
                inplace=not args.safe,
                sort_method=args.sort_method,
                start_at=args.start_at,
                prefix=prefix,
                padding=args.padding,
            )
        except FileNotFoundError as e:
            log.warn(e)
            return 1
    return 0



    #
    # if args.prefix == ":folder":
    #     prefix = os.path.basename(os.path.normpath(args.src_dir))
    #     args.prefix = prefix
    #
    # renumber(
    #     args.src_dir,
    #     dst_dir=args.dst_dir,
    #     inplace=not args.safe,
    #     sort_method=args.sort_method,
    #     start_at=args.start_at,
    #     prefix=args.prefix,
    #     padding=args.padding,
    # )


if __name__ == "__main__":
    sys.exit(main())
