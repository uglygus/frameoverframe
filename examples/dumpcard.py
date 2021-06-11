#!/usr/bin/env python3
""" Prepare an SD card of images.

1. rename folder on card (Manually)
2. copy images off card to destination directory
3. unmix images
4. recombine ARW images ( if previous ones exist )
5. recombine JPG images ( if previous ones exist )
6. make preview movie from JPG images.

"""

import argparse
import sys
import os
import shutil
import re

from itertools import takewhile
from functools import reduce

from frameoverframe.unmix import unmix
from frameoverframe.recombine import recombine
from frameoverframe.img2vid import img2vid
from frameoverframe.utils import sorted_listdir, split_name_number
from frameoverframe.config import extensions


def dumpcard(directory, dst_dir):
    """Prepare images from card to preview.

    1. rename folder on card (Manually)
    2. copy images off card to destination directory
    3. unmix images
    4. recombine ARW images ( if previous ones exist )
    5. recombine JPG images ( if previous ones exist )
    6. make preview movie from JPG images.

    """
    print(f"Copying images...")
    # print(f"{dst_dir=}")
    dst_dir = os.path.join(dst_dir, os.path.basename(directory))
    # print(f"{dst_dir=}")
    #
    # print("directory=", directory)
    #
    # input("should I start copy.....")
    shutil.copytree(directory, dst_dir, dirs_exist_ok=True)

    # input(".done copy.....")

    #
    # Unmix
    #

    try:
        print("Unmixing...")
        result = unmix(dst_dir)
        #    print(f"{result=}")
        sys.stdout.flush()
    except FileNotFoundError as error:
        print("ERROR:", error)
        sys.exit()
    except FileExistsError as error:
        print("ERROR: ", error)
        sys.exit()

    #    print("splitname = ", split_name_number(os.path.basename(dst_dir)))
    shotname = split_name_number(os.path.basename(dst_dir))[0]
    shotname = shotname.rstrip(" -")

    #    print("shot_name=", shotname)

    #    input("unmix finished")

    #
    # recombine
    #
    # unmix is done now look through all the folders and try to find ones we can to_recombine
    # search by extensions
    # look for shotname[-number].extension
    # recombine those

    print("Recombining images...")
    for ext in extensions:
        to_recombine = []
        for item in sorted_listdir(os.path.dirname(dst_dir)):
            # print("\nitem=", item)
            # print("os.path.basename(dst_dir)=", os.path.basename(dst_dir))
            item_shotname = os.path.basename(item)

            regex = rf"^{shotname}(.*?)_{ext}$"
            if re.match(regex, item_shotname):
                to_recombine.append(item)

        #        print("to_recombine=", to_recombine)
        dest_dirs = recombine(to_recombine)
        if ext == "JPG":
            jpg_dirs = dest_dirs

    #    print(" recombine returned dest_dirs", dest_dirs)

    # recombine is done so now we make a preview
    # img2vid()

    # alldirs = sorted_listdir(dests)

    if jpg_dirs is None:
        print(" dest_dirs =None quitting dumpcard()")
        return

    print("Making preview movie...")
    img2vid(jpg_dirs)

    return


def collect_args():
    """collect commandline arguments"""

    parser = argparse.ArgumentParser(description="Unmix - recombine - img2vid")

    parser.add_argument("src_dir", help="Source directory. ")
    parser.add_argument(
        "dst_dir",
        nargs="?",
        default=None,
        help="Destination directory. default None (parent dir of source)",
    )

    return parser


def main():
    """
    Can be called from the commmandline:
    usage: imgprep.py [-h] src_dir [src_dir...]

    """

    parser = collect_args()
    args = parser.parse_args()

    print(f"{args=}")
    #
    # for directory in args.src_dirs:
    if args.dst_dir is None:
        dst_dir = os.path.dirname(args.src_dir)
    else:
        dst_dir = args.dst_dir

    dumpcard(args.src_dir, dst_dir)


if __name__ == "__main__":
    sys.exit(main())
