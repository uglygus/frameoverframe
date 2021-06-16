#!/usr/bin/env python3
"""
    ffmpeg wrapper
    takes a video and creates a folder of images

"""


import argparse
import logging.config

#   logging.getLogger() has to come before importing any frameoverframe modules
#   except frameoverframe.config that must come before (careful isort might move imports)
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
    parser.add_argument(
        "-o",
        "--output_folder",
        action="store",
        default=None,
        help="output folder, default is the name of name_of_input_video",
    )

    args = parser.parse_args()

    return args


def main():
    """commandline setup vid2img"""

    args = collect_args()
    log.setLevel(logging.INFO)

    log.debug(f"args= {args}")

    vid2img(args.input_mov, args.output_folder)

    print("DONE.")


if __name__ == "__main__":
    main()
