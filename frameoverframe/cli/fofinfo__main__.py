#!/usr/bin/env python3
"""
    bracket - module docstring

"""

import argparse
import os
import sys

from PIL import Image
from PIL import ImageStat

import frameoverframe.info as info
import frameoverframe.utils as utils


def collect_args():
    """collect commandline arguments"""

    parser = argparse.ArgumentParser(description="frameoverframe - fps")

    parser.add_argument("input", nargs="*", default=None, help="folder(s)")
    parser.add_argument(
        "-a",
        "--alltags",
        action="store_true",
        default=False,
        dest="alltags",
        help="include all EXIF tags",
    )
    return parser


def main():
    """do the main thing"""

    parser = collect_args()
    args = parser.parse_args()

    # print('args==', args)

    for item in args.input:

        frames = len(os.listdir(item))

        info.print_exif_tags(utils.sorted_listdir(item)[0], alltags=args.alltags)

        im = Image.open(utils.sorted_listdir(item)[0])

        stat = ImageStat.Stat(im)
        print(" stat= ", stat)
        print("dir im = ", dir(im))
        print(" width= ", im.width)
        print(" size= ", im.size)
        print("Number of frames :", frames)

        info.fps_dir(item)

    return 0


if __name__ == "__main__":
    sys.exit(main())
