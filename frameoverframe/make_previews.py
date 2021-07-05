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
from frameoverframe.utils import ext_list, folder_contains_ext, sorted_listdir

log = logging.getLogger("frameoverframe")


def _make_previews(src_dir):
    init()  # colorama

    log.debug("make_previews : in_dir = %s" % (src_dir))

    was_the_list_of_dirs_modified = False
    for item in sorted_listdir(src_dir):
        contains_raw_ext = False

        if os.path.isfile(item):
            log.info(f"'{item}' -- {Fore.RED}SKIPPING{Style.RESET_ALL} Not a directory.")
            continue

        if os.path.isfile(f"{item}.mp4") or os.path.isfile(f"{item}_preview.mp4"):
            log.info(f"{item}' -- {Fore.GREEN}SKIPPING{Style.RESET_ALL} Video file alread exists.")
            continue

        extensions = ext_list(item)
        if extensions == [""]:
            log.info(
                f"'{item}' -- {Fore.YELLOW}SKIPPING{Style.RESET_ALL} directory contains only directories."
            )
            continue

        if len(extensions) > 2:
            log.info(
                f"'{item}' -- {Fore.RED}SKIPPING{Style.RESET_ALL} Contains more than two filetypes. {extensions}"
            )
            continue

        if folder_contains_ext(item, RAW_EXTENSIONS) and folder_contains_ext(item, "JPG"):
            log.debug(f"unmixing {item}")
            if unmix(item):
                log.debug(f"{item} just got unmixed I will need double check all this.")
                was_the_list_of_dirs_modified = True
                continue
            log.debug("unmix failed item=%s'" % (item))
            contains_raw_ext = True

        if not folder_contains_ext(item, "JPG"):
            log.info(
                f"'{item}' -- {Fore.YELLOW}SKIPPING{Style.RESET_ALL} Folder doesn't have any JPGs extensions={extensions}"
            )
            continue
        #
        # if folder_contains_ext(item, RAW_EXTENSIONS):
        #     if unmix(item):
        #         log.info(f"{item} just got unmixed I will need double check all this.")
        #         was_the_list_of_dirs_modified = True
        #         continue
        #     log.debug("unmix failed itemr=%s'" % (item))
        #     contains_raw_ext = True

        if not was_the_list_of_dirs_modified:
            # log.info(f"Making video for '{item}'")
            img2vid(item)
            log.info(
                f"'{item}' -- {Fore.GREEN}SUCCESS{Style.RESET_ALL} Video for {item} succesfully made."
            )
    return was_the_list_of_dirs_modified


def make_previews(src_dir):
    """Repeat until _make_previews() runs without needing to unmix()"""

    while True:
        result = _make_previews(src_dir)
        if result:
            log.debug("make_previews() : running again, result = %s", result)
        else:
            break
