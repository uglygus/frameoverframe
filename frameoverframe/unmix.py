#!/usr/bin/env python3

"""
unmix

unmix's images that are stored in the same folder. This helps with Canon folders
which store the CR2 and JPG files in the same folder.

For example:
/fireants/000001.CR2
/fireants/000001.JPG
/fireants/000002.CR2
/fireants/000002.JPG

becomes:
/fireants_CR2/000001.CR2
/fireants_CR2/000002.CR2
/fireants_JPG/000001.JPG
/fireants_JPG/000002.JPG

ignores .DS_Store files

"""

import logging
import os
import re
import shutil
import sys

import frameoverframe.utils as utils

log = logging.getLogger("frameoverframe")


def new_dirname(src_dir, ext):
    """returns a new dirname based on ext of a file
    takes into account any trailing digits and keeps them trailing

    src_dir  the original dir
    ext      the extension of one of the files in src_dir

    eg: new_dirname(/path/to/final_01, 'JPG')

    Returns(str):
        /path/to/final_JPG_01
    """

    # does it end in numbers _01 ? If so keep the numbers at the end.

    m = re.search("_[0-9]+$", os.path.basename(src_dir))

    if m:
        stripped = re.sub("_[0-9]+$", "", os.path.basename(src_dir))
        newdir = stripped + "_" + ext + m[0]
    else:
        newdir = os.path.basename(src_dir) + "_" + ext
    return os.path.join(os.path.dirname(src_dir), newdir)


def unmix(src_dir):
    """
    unmix's images that are stored in the same folder.
    Canon puts CR2 and JPG together. Sony puts ARW and JPG together.

    Args:
        src_dir (str): Path to source directory containing the image sequences

    Returns():
        new_dirs (list): newly created directories (in alphabetical order)

    """

    ext_list = utils.ext_list(src_dir)

    if ext_list == [""]:
        log.warn("Directory has no files with extensions. Stopping.")
        return None

    ext_list.sort()

    if len(ext_list) == 1:
        log.info(f"unmix: Looks good folder is already unmixed. {src_dir}")
        log.debug(f"{ext_list[0]=}")
        ext = ext_list[0].lstrip(".")
        src_dir_EXT = src_dir + "_" + ext
        log.debug("Renaming {src_dir} to {src_dir_EXT}")
        os.rename(src_dir, src_dir_EXT)
        return [""]

    if len(ext_list) == 0:
        log.warn(f"unmix: Not sure if we can even get here? Extension list is empty. {src_dir}")
        return [""]

    if len(ext_list) > 2:
        log.warn(f"unmix: This folder has more than two extensions. Stopping. {src_dir}")
        log.warn(f"{ext_list=}")
        return [""]

    for d in ext_list:
        if d == "":
            log.warn(f"unmix: This folder has other folders in it. Stopping. {src_dir}")
            return [""]

    new_dirs = []

    for ext in ext_list:
        ext = ext.lstrip(".")

        new_dir = new_dirname(src_dir, ext)
        try:
            os.mkdir(new_dir)
        except FileExistsError:
            log.warn(f"ERROR: Directory already exists. {new_dir}")
            raise

        new_dirs.append(new_dir)

    for item in os.listdir(src_dir):
        if item == ".DS_Store":
            continue

        ext = os.path.splitext(os.path.split(item)[1])[1]
        ext = ext.lstrip(".")
        orig_item = os.path.join(src_dir, item)
        new_item = new_dirname(src_dir, ext)
        try:
            log.debug(f"renaming {orig_item} -> {new_item}")
            shutil.move(orig_item, new_item)
        except FileNotFoundError as e:
            log.warn(f"renaming {orig_item} -> {new_item}")
            raise

    shutil.rmtree(src_dir)

    # new dirs is in alphabetical order so for both
    # Canon and Sony cameras the JPG folder is second.
    # Sony ['indir_ARW', 'indir_JPG']
    # Canon ['indir_CR2, 'indir_JPG']
    return new_dirs
