#!/usr/bin/env python3

"""
make_previews()

A high level function that given a folder check every
subfolder and unmix if necessary also if there is a folder
of JPGs run img2vid on it.

returns a list of the folders that have been unmixed.
If the returned list is not empty - run it again like this:
    while(make_previews('some/folder')):
        pass

"""

import logging
import os
import re
import sys
from itertools import product

from colorama import Fore, Style, init

from frameoverframe.config import RAW_EXTENSIONS
from frameoverframe.img2vid import img2vid
from frameoverframe.unmix import unmix
from frameoverframe.utils import ext_list, sorted_listdir

log = logging.getLogger("frameoverframe")


def check_folder_for_RAW_extensions(src_dir):

    contains_raw_ext = False
    was_the_list_of_dirs_modified = False

    extensions = ext_list(src_dir)
    log.debug("Checking folder for RAW extensions.")
    for ext, raw_ext in product(extensions, RAW_EXTENSIONS):
        if re.search(rf"{ext}$", raw_ext, re.IGNORECASE):
            if unmix(src_dir):
                log.info(f"{src_dir} was unmixed I will need double check all this.")
                was_the_list_of_dirs_modified = True
            log.debug("RAW Extension found, skipping '%s'" % (raw_ext))
            contains_raw_ext = True
    print("check_for... returning (%s, %s)", (contains_raw_ext, was_the_list_of_dirs_modified))

    input(";;;")
    return (contains_raw_ext, was_the_list_of_dirs_modified)


def _make_previews(src_dir):
    init()  # colorama

    log.debug("make_previews : in_dir = %s" % (src_dir))

    for item in sorted_listdir(src_dir):
        contains_raw_ext = False

        if os.path.isfile(item):
            log.debug(f"'{item}' -- {Fore.RED}SKIPPING{Style.RESET_ALL}not a directory.")
            continue

        if os.path.isfile(f"{item}.mp4") or os.path.isfile(f"{item}_preview.mp4"):
            log.info(f"Video file for '{item}' already exists.")
            continue

        #        log.info(f"There is no video for: '{item}'")

        extensions = ext_list(item)
        if extensions == [""]:
            log.info(
                f"'{item}' -- {Fore.RED}SKIPPING{Style.RESET_ALL} directory contains only directories."
            )
            continue

        (contains_raw_ext, was_this_list_of_dirs_modified) = check_folder_for_RAW_extensions(item)
        if was_this_list_of_dirs_modified:
            was_the_list_of_dirs_modified = True

        if contains_raw_ext:
            log.debug("Why and how did we get here?")
            log.debug(
                f"'{item}' contains RAW images but was not correctly unmixed. Do not make a video."
            )
            continue

        log.info(f"Making video for '{item}'")
        img2vid(item)

    return was_the_list_of_dirs_modified


def make_previews(src_dir):
    """Repeat until _make_previews() runs without needing to unmix()"""

    while True:
        result = _make_previews(src_dir)
        if result:
            log.debug("make_previews() : running again, result = %s", result)
        else:
            break
