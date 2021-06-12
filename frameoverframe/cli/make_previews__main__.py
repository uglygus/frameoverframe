#!/usr/bin/env python3
"""
make_previews.py

given a folder check every subfolder and try to run img2vid on it.


"""

import argparse
import os
import sys

from colorama import Fore, Style, init

from frameoverframe.img2vid import img2vid
from frameoverframe.utils import ext_list, sorted_listdir


def collect_args():
    """collect commandline arguments"""

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "src_dir",
        help="Source directory. ",
    )

    return parser


def main():
    """
    Can be called from the commmandline:
    usage: renumber.py [-h] [-o DST_DIR] [-i] [-s START_AT] [-x PREFIX] [-p PADDING] src_dir

    """

    init()  # colorama

    parser = collect_args()
    args = parser.parse_args()

    for _dir in sorted_listdir(args.src_dir):

        # print("\n" + f"{_dir=}")

        if os.path.isdir(_dir):
            if os.path.isfile(_dir + ".mp4"):
                pass
                # print(f"Video file for {args.src_dir}/{_dir} already exists.")
            else:
                extensions = ext_list(_dir)
                print(f"'{_dir}' -- Needs video.")

                if extensions == [""]:
                    print(
                        f"'{_dir}' -- {Fore.RED}SKIPPING{Style.RESET_ALL} Folder contains only directories."
                    )
                    continue
                if ".ARW" in extensions:
                    print(
                        f"'{_dir}' -- {Fore.RED}SKIPPING{Style.RESET_ALL} Folder contains .ARW files. I only process .JPG files."
                    )
                    continue
                if ".CR2" in extensions:
                    print(
                        f"'{_dir}' -- {Fore.RED}SKIPPING{Style.RESET_ALL} Folder contains .CR2 files. I only process .JPG files."
                    )
                    continue
                img2vid(_dir, _dir + ".mp4")


if __name__ == "__main__":
    sys.exit(main())
