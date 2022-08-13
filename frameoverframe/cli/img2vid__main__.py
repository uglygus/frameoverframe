#!/usr/bin/env python
"""
    ffmpeg wrapper
    takes a folder of images creates a video

    Takes one or more folders of images and creates a video. \
    This video is just a preview not meant for editing it is highly compressed. \
    Framerate 24fps. \
    By default video dimensions are the same as the original images \
    the --preview option will make the dimensions 1080p or smaller."
)

"""

import argparse
import logging.config
import sys

from colorama import Fore, Style, init
from PIL import Image

from frameoverframe.config import LOGGING_CONFIG

#   logging.config.dictConfig() and logging.getLogger()
#   must come after importing LOGGING_CONFIG
#   but before any other frameoverframe modules.

logging.config.dictConfig(LOGGING_CONFIG)

from frameoverframe.config import RAW_EXTENSIONS
from frameoverframe.utils import sorted_listdir

log = logging.getLogger("frameoverframe")

# Image.MAX_IMAGE_PIXELS = 244022272  # otherwise PIL bails on large images

from frameoverframe.img2vid import img2vid


def collect_args():
    """collect commandline arguments"""

    parser = argparse.ArgumentParser(
        description="Takes one or more folders of images and creates a video. \
                     This video is just a preview not meant for editing it is highly compressed. \
                     Framerate 24fps. \
                     By default video dimensions are the same as the original images \
                     the --preview option will make the dimensions 1080p or smaller."
    )

    parser.add_argument("input_dirs", nargs="+", help="directory of images...")
    parser.add_argument(
        "-o",
        "--output_filename",
        action="store",
        default=None,
        help="output filename, default is the name of name_of_input_directory.srt",
    )
    parser.add_argument(
        "-p",
        "--profile",
        action="store",
        default="preview",
        choices={"tiny", "preview", "uhd", "prores"},
        help="preview is 1080p/h264; uhd is 2160p/h264; prores is prores_sd/fullsize.",
    )
    parser.add_argument(
        "-f",
        "--framenumber",
        dest="framenumber",
        default=False,
        action="store_true",
        help="Burn in framenumbers. default:False",
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
    """commandline setup img2vid"""

    args = collect_args()
    log.setLevel(args.loglevel)

    log.debug(f"{args=}")

    try:
        img2vid(
            args.input_dirs,
            args.output_filename,
            args.profile,
            framenumber=args.framenumber,
        )
    except NotADirectoryError as e:
        log.warning(e)
        sys.exit(1)

    log.info("DONE.")


if __name__ == "__main__":
    sys.exit(main())
