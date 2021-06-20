#!/usr/bin/env python3
"""
unmix

unmix's images that are stored in the same folder. This helps with Canon folders
which store the CR2 and JPG files in the same folder.

For example:
/fireants/000001.CR2
/fireants/000001.JPG
/fireants/000002.CR2
/fireants/000002.JPG

becomes:
/fireants_CR2/000001.CR2
/fireants_CR2/000002.CR2
/fireants_JPG/000001.JPG
/fireants_JPG/000002.JPG

ignores .DS_Store files

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


from frameoverframe.unmix import unmix


def collect_args():
    """collect commandline arguments"""

    parser = argparse.ArgumentParser(
        description="Unmix's images that are stored in the same folder."
        "This helps with Canon folders which store the CR2 and JPG files in the same folder."
    )

    parser.add_argument(
        "src_dirs",
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
        log.info(f"unmixing {directory} ...")
        try:
            unmix(directory)
        except FileNotFoundError as e:
            log.warn(e)
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
