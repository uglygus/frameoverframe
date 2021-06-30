#!/usr/bin/env python3
"""
    check_images
    Tests files one by one from many directories. Reports bad images to stdout.
    Uses imagemagick's `identify` to do the actual testing
"""

import argparse
import logging.config

from frameoverframe.config import LOGGING_CONFIG

#   logging.config.dictConfig() and logging.getLogger()
#   must come after importing LOGGING_CONFIG
#   but before any other frameoverframe modules.

logging.config.dictConfig(LOGGING_CONFIG)
log = logging.getLogger("frameoverframe")

from frameoverframe.check_images import check_images


def collect_args():
    """collect commandline arguments"""

    parser = argparse.ArgumentParser(
        description="Takes one or more folders of images and tests each image "
        "using ffmpeg's identify. Reports bad images to stdout."
    )

    parser.add_argument("input_dirs", nargs="+", help="directory(s) of images...")
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

    #   parser.add_argument( "-r", "--recursive", action="store_true", default=False,
    #       help="Descend into sub directories?. (default False)",
    #   )

    parser.set_defaults(loglevel=logging.INFO)
    args = parser.parse_args()
    log.setLevel(args.loglevel)

    return args


def main():
    """commandline setup"""

    # logging.info("Hello, log called from __main__")
    # log.info("called LOG from __main__")
    #

    args = collect_args()
    log.setLevel(args.loglevel)

    log.debug(f"args= {args}\n{log.level=}")

    check_images(args.input_dirs)  # , args.recursive)


if __name__ == "__main__":
    main()
