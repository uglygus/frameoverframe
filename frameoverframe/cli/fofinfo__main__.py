#!/usr/bin/env python3
"""
    fofinfo
    Get technical details about an image sequence.

"""

import argparse
import logging.config
import os
import sys

from PIL import Image, ImageStat

#   logging.config.dictConfig() and logging.getLogger()
#   must come after importing LOGGING_CONFIG
#   but before any other frameoverframe modules.
from frameoverframe.config import LOGGING_CONFIG

logging.config.dictConfig(LOGGING_CONFIG)
log = logging.getLogger("frameoverframe")

import frameoverframe.info as info
import frameoverframe.utils as utils

parser = argparse.ArgumentParser(
    description="Provides information such as length, exif tags, frames per second."
)


def collect_args():
    """collect commandline arguments"""

    parser = argparse.ArgumentParser(
        description="Provides information such as length, exif tags, frames per second."
    )

    parser.add_argument("arguments", nargs="*", default=None, help="folder(s)")
    parser.add_argument(
        "-f",
        "--fps",
        action="store_const",
        const="fps",
        dest="command",
        help="Report the speed of shooting with a graph.",
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
    """do the main thing"""

    args = collect_args()
    log.setLevel(args.loglevel)

    print("args=", args)

    print("TYPE INPUT=", type(args.arguments))

    print("args.argumebnts=", args.arguments)

    print("args.command=", args.command)

    if len(args.arguments) == 0:
        parser.print_help()
        print("asdf")
        return 0

    for dirfile in args.arguments:

        sample_file = os.path.join(dirfile, os.listdir(dirfile)[0])
        print(f"{dirfile=}")
        dirfile = os.path.abspath(dirfile)
        print(f"{dirfile=}")
        if os.path.isdir(dirfile):
            info.fps_dir(dirfile)
            info.print_exif_tags(sample_file)
            info.num_frames(dirfile)
        else:
            log.info("Not a directory: ", dirfile)

            # ["fps", "a", "alltags", "input"]:

    ###########
    ########### These need to be implemented. do not delete!
    ###########
    # frames = len(os.listdir(item))
    #
    # info.print_exif_tags(utils.sorted_listdir(item)[0], alltags=args.alltags)
    #
    # im = Image.open(utils.sorted_listdir(item)[0])
    #
    # stat = ImageStat.Stat(im)
    # print(" stat= ", stat)
    # print("dir im = ", dir(im))
    # print(" width= ", im.width)
    # print(" size= ", im.size)
    # print("Number of frames :", frames)

    return 0


if __name__ == "__main__":
    sys.exit(main())
