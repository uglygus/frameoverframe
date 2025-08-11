#!/usr/bin/env python3
"""    Recombines several folders with many images in each folder so that
    the images order is maintained but the folders hold as many images
    as possible up to the maximum number of files specified.

"""


import argparse
import logging.config
import os
import sys

from frameoverframe.config import LOGGING_CONFIG

#   logging.config.dictConfig() and logging.getLogger()
#   must come after importing LOGGING_CONFIG
#   but before any other frameoverframe modules.

logging.config.dictConfig(LOGGING_CONFIG)

from frameoverframe.recombine import recombine

log = logging.getLogger("frameoverframe")


def dir_path(path):
    """for argparse directory type test.

    Args:
      path:

    Returns:

    """
    if os.path.isdir(path):
        return path
    else:
        raise argparse.ArgumentTypeError(f"readable_dir:{path} is not a valid path")


def collect_args():

    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        "src_dirs",
        nargs="+",
        type=dir_path,
        help="Source directories. ",
    )

    parser.add_argument(
        "-m",
        "--max_files",
        type=int,
        default=10000,
        help="Max number of files per directory. (default 10000)",
    )

    parser.add_argument(
        "-o",
        "--dst_dir",
        type=str,
        default=None,
        help="Destination directory",
    )

    parser.add_argument(
        "--copy_files",
        action="store_true",
        default=False,
        help="Copy files to a new direcotory otherwise they are moved. Default: False",
    )

    parser.add_argument(
        "-x",
        "--prefix",
        type=str,
        default=":folder",
        help="Prefix. (default no prefix). '' empty string will "
        "strip any existing prefix. The special word :folder will "
        "use the enclosing first folder's name as the prefix. default :folder",
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
    """Renumber Can be called from the commmandline."""

    args = collect_args()
    log.setLevel(args.loglevel)

    print('args=', args)

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
