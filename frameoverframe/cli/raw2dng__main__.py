#!/usr/bin/env python3
"""
    ffmpeg wrapper
    takes a folder of images creates a video

"""


import argparse
import logging.config
import sys

from frameoverframe.config import LOGGING_CONFIG

#   logging.config.dictConfig() and logging.getLogger()
#   must come after importing LOGGING_CONFIG
#   but before any other frameoverframe modules.

logging.config.dictConfig(LOGGING_CONFIG)
log = logging.getLogger("frameoverframe")

from frameoverframe.raw2dng import raw2dng


def collect_args():
    """collect commandline arguments"""

    parser = argparse.ArgumentParser(
        description='Wrapper for "Adobe DNG Converter" \
                     Accepts a directories instead of individual files.'
    )

    parser.add_argument("input_dirs", nargs="+", help="directory of images...")
    parser.add_argument(
        "-o", "--output_dir", action="store", default=None, help="outputdirectory for the DNG files"
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
    log.debug("args.loglevel = {}".format(args.loglevel))
    return args


def main():
    """Use Adobe DNG Converter to convert RAW files to DNG
    Requires Adobe DNG Converter to be installed.
    """

    args = collect_args()
    log.setLevel(args.loglevel)

    try:
        raw2dng(args.input_dirs, args.output_dir)
    except FileNotFoundError as e:
        print("FileNotFoundError: ", e)
        return 1

    log.info("DONE.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
