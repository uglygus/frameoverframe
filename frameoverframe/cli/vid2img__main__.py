#!/usr/bin/env python3
"""
    ffmpeg wrapper
    takes a video and creates a folder of images

"""


import argparse
import logging.config

#   logging.getLogger() must come after frameoverframe.config
#    but before any other frameoverframe modules.
from frameoverframe.config import LOGGING_CONFIG

logging.config.dictConfig(LOGGING_CONFIG)
log = logging.getLogger("frameoverframe")

from frameoverframe.vid2img import vid2img


def collect_args():
    """collect commandline arguments"""

    parser = argparse.ArgumentParser(
        description="Takes a video file and converts it to still images \
                    "
    )

    parser.add_argument("input_mov", help="video file...")
    group = parser.add_mutually_exclusive_group()
    parser.add_argument(
        "-o",
        "--output_folder",
        action="store",
        default=None,
        help="output folder, default is the name of name_of_input_video",
    )
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
    """commandline setup vid2img"""

    args = collect_args()
    log.setLevel(args.loglevel)

    log.debug(f"args= {args}")
    log.debug(f"{log.level=}")

    try:
        vid2img(args.input_mov, args.output_folder)
    except FileNotFoundError as e:
        print("FileNotFoundError: ", e)
        return 1

    log.info("DONE.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
