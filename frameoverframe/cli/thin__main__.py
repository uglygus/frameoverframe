#!/usr/bin/env python3
"""
thin

copies file like cp but skips files. Copy every other file, or every 10th file, etc
Used to thin timelapses that have too many frames for their movement.
Timelapses we end up using at 10x or 20x speed should be thinned.

"""

import argparse
import logging.config
import sys

#   logging.config.dictConfig() and logging.getLogger()
#   must come after importing LOGGING_CONFIG
#   but before any other frameoverframe modules.
from frameoverframe.config import LOGGING_CONFIG

logging.config.dictConfig(LOGGING_CONFIG)
log = logging.getLogger("frameoverframe")

from frameoverframe.thin import thin


def collect_args():
    """collect commandline arguments"""

    parser = argparse.ArgumentParser()

    parser.add_argument("src_dirs", nargs="+", help="Source directory. ")

    parser.add_argument(
        "-e", "--every", type=int, required=True, help="copy every nth file. Discard the rest."
    )

    parser.add_argument("-o", "--dst_dir", type=str, default=None, help="Destination directory")

    parser.add_argument(
        "--inplace",
        action="store_false",
        default=False,
        help="Copy files to a new direcotory otherwise they are renamed inplace. (default False)",
    )

    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--quiet",
        "-q",
        action="store_const",
        const=logging.WARN,
        dest="loglevel",
        help="Only output when necessary.",
    )
    group.add_argument(
        "--verbose",
        "-v",
        action="store_const",
        const=logging.DEBUG,
        dest="loglevel",
        help="Increase output verbosity.",
    )

    parser.set_defaults(loglevel=logging.INFO)
    args = parser.parse_args()
    log.setLevel(args.loglevel)

    return args


def main():
    """
    Can be called from the commmandline:
    usage: renumber.py [-h] [-o DST_DIR] [-i] [-s START_AT] [-x PREFIX] [-p PADDING] src_dir

    """

    args = collect_args()
    log.setLevel(args.loglevel)

    log.debug(f"{args=}")

    args.src_dirs.sort()

    for single_dir in args.src_dirs:
        thin(
            single_dir,
            args.every,
            dst_dir=args.dst_dir,
            inplace=args.inplace,
        )


if __name__ == "__main__":

    result = main()
    print("result=", result)
    sys.exit(main())
