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


def _make_previews(src_dir):
    init()  # colorama
    dirs_changed_need_to_recurse = False

    log.debug("make_previews : in_dir = %s" % (src_dir))

    for _dir in sorted_listdir(src_dir):
        skip_this_dir = False
        if os.path.isfile(_dir):
            log.debug(f"'{_dir}' -- {Fore.RED}SKIPPING{Style.RESET_ALL}not a directory.")
            continue

        if os.path.isfile(f"{_dir}.mp4") or os.path.isfile(f"{_dir}_preview.mp4"):
            log.debug(f"Restarting - Video file for {src_dir}/{_dir} already exists.")
            continue
        else:
            log.debug(" Continuing - There is no video for: {_dir}")
        extensions = ext_list(_dir)
        log.debug(f"{extensions=}")
        log.debug(f"'{_dir}' -- Needs video.")

        if extensions == [""]:
            log.info(
                f"'{_dir}' -- {Fore.RED}SKIPPING{Style.RESET_ALL} Folder contains only directories."
            )
            continue

        log.debug("Checking folder for RAW extensions.")
        log.debug("extensions = %s" % (extensions))
        for ext, raw_ext in product(extensions, RAW_EXTENSIONS):
            if re.search(rf"{ext}$", raw_ext, re.IGNORECASE):
                log.debug("RAW Extension found, %s needs unmix." % (raw_ext))

                result = unmix(_dir)
                if result:
                    dirs_changed_need_to_recurse = True

                skip_this_dir = True
                break
            else:
                log.debug("NO-MATCH")

        if skip_this_dir:
            log.debug("continuing because skip_this_dir = True")
            continue

            # , {_dir}.mp4)
        log.info(f"calling image2vid({_dir}")
        img2vid(_dir)  # , _dir + ".mp4"

    return dirs_changed_need_to_recurse


def make_previews(src_dir):
    """Repeat until _make_previews() runs without needing to unmix()"""

    while True:
        result = _make_previews(src_dir)
        if result:
            log.debug("make_previews() : running again, result = %s", result)
        else:
            break
