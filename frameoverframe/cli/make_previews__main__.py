#!/usr/bin/env python3
"""
make_previews.py

given a folder check every subfolder and try to run img2vid on it.

"""

import argparse
import logging.config
import os
import re
import sys

from colorama import Fore, Style, init

from frameoverframe.config import LOGGING_CONFIG, RAW_EXTENSIONS
from frameoverframe.img2vid import img2vid
from frameoverframe.utils import ext_list, sorted_listdir


def collect_args():
    """collect commandline arguments"""

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "src_dir",
        help="Source directory. ",
    )

    parser.add_argument("--quiet", action="store_true", help="Only output when necessary.")
    parser.add_argument("--verbose", "-v", action="store_true", help="increase output verbosity")
    parser.add_argument("--debug", action="store_true", help="Print debugging information.")

    return parser


def main():
    """
    Can be called from the commmandline:
    usage: renumber.py [-h] [-o DST_DIR] [-i] [-s START_AT] [-x PREFIX] [-p PADDING] src_dir

    """

    parser = collect_args()
    args = parser.parse_args()

    logging.config.dictConfig(LOGGING_CONFIG)
    log = logging.getLogger("frameoverframe")

    log.setLevel(logging.WARN) if args.quiet else None
    log.setLevel(logging.INFO) if args.verbose else None
    log.setLevel(logging.DEBUG) if args.debug else None

    init()  # colorama

    from itertools import product

    # input("...stopee....")

    for _dir in sorted_listdir(args.src_dir):
        # inpu("...waiting..top of for....")
        skip_this_dir = False
        log.info(f"{_dir}")

        if os.path.isfile(_dir):
            continue

        if os.path.isfile(f"{_dir}.mp4") or os.path.isfile(f"{_dir}_preview.mp4"):
            pass
            log.info(f"Video file for {args.src_dir}/{_dir} already exists.")
            continue

        extensions = ext_list(_dir)
        log.debug(f"{extensions=}")
        #    print(f"'{_dir}' -- Needs video.")

        if extensions == [""]:
            log.info(
                f"'{_dir}' -- {Fore.RED}SKIPPING{Style.RESET_ALL} Folder contains only directories."
            )
            continue

        #        for ext in extensions:

        for ext, raw_ext in product(extensions, RAW_EXTENSIONS):
            # print(f"{ext=}, {raw_ext=}")
            if re.search(rf"{ext}$", raw_ext, re.IGNORECASE):
                log.debug(" MATCH contains ext", ext)
                skip_this_dir = True
                break
            else:
                log.debug("NO-MATCH")

        # print("....done for loop...")
        # input("...")

        if skip_this_dir:
            continue

        log.info(f"calling image2vid({_dir}, {_dir}.mp4)")
        img2vid(_dir, _dir + ".mp4")


if __name__ == "__main__":
    sys.exit(main())
