#!/usr/bin/env python3
"""
make_previews.py

given a folder check every subfolder and try to run img2vid on it.

"""

import argparse
import logging.config
import os
import sys

from frameoverframe.config import LOGGING_CONFIG

logging.config.dictConfig(LOGGING_CONFIG)
log = logging.getLogger("frameoverframe")

from frameoverframe.make_previews import make_previews


def collect_args():
    """collect commandline arguments"""

    parser = argparse.ArgumentParser(
        description="Look for directories of pegs and make a previes for each one."
    )

    parser.add_argument(
        "src_dir",
        nargs="+",
        help="Source directory. ",
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
    verbosity.set_defaults(loglevel=logging.INFO)
    args = parser.parse_args()
    log.setLevel(args.loglevel)

    return args


def main():
    """
    Can be called from the commmandline:
    usage: make_previews [-h] src_dir...

    """

    args = collect_args()
    log.setLevel(args.loglevel)
    #    log.critical("logging level : %s", logging.getLevelName(log.getEffectiveLevel()))

    for single_input in args.src_dir:
        if not os.path.isdir(single_input):
            print("ERROR: input is not a directory: " + single_input)
            return 1

        try:
            make_previews(single_input)
        except FileNotFoundError as e:
            log.warning("File not Found: %s", e)

    return 0


if __name__ == "__main__":
    sys.exit(main())
