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

import logging.config

from frameoverframe.config import LOGGING_CONFIG

logging.config.dictConfig(LOGGING_CONFIG)
log = logging.getLogger("frameoverframe")

from frameoverframe.config import LOGGING_CONFIG, RAW_EXTENSIONS
from frameoverframe.img2vid import img2vid
from frameoverframe.utils import ext_list, sorted_listdir


def collect_args():
    """collect commandline arguments"""

    parser = argparse.ArgumentParser(description="Look for directories of pegs and make a previes for each one.")

    parser.add_argument(
        "src_dir",
        help="Source directory. ",
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
    verbosity.set_defaults(loglevel=logging.INFO)
    args = parser.parse_args()
    log.setLevel(args.loglevel)

    return args



def main():
    """
    Can be called from the commmandline:
    usage: renumber.py [-h] [-o DST_DIR] [-i] [-s START_AT] [-x PREFIX] [-p PADDING] src_dir

    """

    args = collect_args()

    logging.config.dictConfig(LOGGING_CONFIG)
    log = logging.getLogger("frameoverframe")

    init()  # colorama

    from itertools import product



    for _dir in sorted_listdir(args.src_dir):
        # inpu("...waiting..top of for....")
        skip_this_dir = False

        log.info(f"{_dir}")

        if os.path.isfile(_dir):
            log.debug(
                f"'{_dir}' -- {Fore.RED}SKIPPING{Style.RESET_ALL}not a directory."
            )
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

        log.debug("....done for loop...")
        input("...")

        if skip_this_dir:
            continue

        log.info(f"calling image2vid({_dir}, {_dir}.mp4)")
        img2vid(_dir, _dir + ".mp4")


if __name__ == "__main__":

    args = collect_args()
    log.setLevel(args.loglevel)

    log.debug(f"args= {args}")
    log.debug(f"{log.level=}")

    input('... maiin...')
    #sys.exit(main())
