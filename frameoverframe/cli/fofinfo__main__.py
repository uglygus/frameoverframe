#!/usr/bin/env python3
"""
    bracket - module docstring

"""

import argparse
import os
import sys

from PIL import Image, ImageStat

import frameoverframe.info as info
import frameoverframe.utils as utils


def collect_args():
    """collect commandline arguments"""


    parser = argparse.ArgumentParser( \
        description="Provides information such as length, exif tags, frames per second."
    )

    parser.add_argument("arguments", nargs="*", default=None, help="folder(s)")
    parser.add_argument("-f", "--fps",action="store_const", const="fps", dest="command", help="Report the speed of shooting with a graph.")
    # parser.add_argument(
    #     "-a",
    #     "--alltags",
    #     action="store_true",
    #     default=False,
    #     help="include all EXIF tags",
    # )
    args = parser.parse_args()

    return args


def main():
    """do the main thing"""

    args = collect_args()

    print('args=', args)


    print('TYPE INPUT=', type(args.arguments))

    print('args.argumebnts=', args.arguments)

    if args.command == "fps":
        for dirfile in args.arguments:
            print(f"{dirfile=}")
            dirfile=os.path.abspath(dirfile)
            print(f"{dirfile=}")
            if os.path.isdir(dirfile):
                info.fps_dir(dirfile)
                return 0

            if os.path.isfile(dirfile):
                print("Calling fps_single() dirpath=", dirpath, "==")
                info.fps_single(dirfile)
                return 0
            else:
                print("No path provided. eg: $ fofinfo --fps ./somedir/")
                return 1


            # ["fps", "a", "alltags", "input"]:


            ### hese need to be implemented. do not delete
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
