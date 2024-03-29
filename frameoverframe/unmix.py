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

import frameoverframe.config as config
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

    log.debug("new_dirname({}, {})".format(src_dir, ext))

    ext = ext.upper()

    # does it end in numbers _01 ? If so keep the numbers at the end.
    m = re.search("_[0-9]+$", os.path.basename(src_dir))

    if m:
        stripped = re.sub("_[0-9]+$", "", os.path.basename(src_dir))
        newdir = stripped + "_" + ext + m[0]
    else:
        if not src_dir.endswith("_" + ext.lstrip(".")):
            src_dir_EXT = src_dir + "_" + ext
            newdir = os.path.basename(src_dir) + "_" + ext
        else:
            newdir = src_dir
    log.debug("new_dirname() returning: {}".format(os.path.join(os.path.dirname(src_dir), newdir)))
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

    new_dirs = []

    utils.rm_trash_files(src_dir)

    ext_list = utils.ext_list(src_dir)

    if ext_list == [""]:
        log.warning("Directory has no files with extensions. Stopping.")
        return new_dirs

    ext_list.sort()
    log.debug(f"{ext_list=}")

    if len(ext_list) == 1:
        log.info(f"unmix: Looks good folder is already unmixed. {src_dir}")

        ext = ext_list[0].lstrip(".").upper()
        if not src_dir.endswith("_" + ext.lstrip(".")):
            src_dir_EXT = src_dir + "_" + ext
            log.debug("Renaming {src_dir} to {src_dir_EXT}")
            os.rename(src_dir, src_dir_EXT)
        else:
            log.debug("src_dir already ends with %s" % ext)
        return new_dirs

    if len(ext_list) == 0:
        log.warning(f"unmix: Not sure if we can even get here? Extension list is empty. {src_dir}")
        return new_dirs

    # if len(ext_list) > 2:
    #     log.warning(f"unmix: This folder has more than two extensions. Stopping. {src_dir}")
    #     log.warning(f"{ext_list=}")
    #     return new_dirs

    for d in ext_list:
        if d == "":
            log.warning(f"unmix: This folder has other folders in it. Stopping. {src_dir}")
            return new_dirs

    for ext in ext_list:
        ext = ext.lstrip(".")

        new_dir = new_dirname(src_dir, ext)
        try:
            os.mkdir(new_dir)
        except FileExistsError:
            if new_dir == src_dir:
                continue
            else:
                log.warning(f"ERROR: Directory already exists. {new_dir}")
                sys.exit(1)

        new_dirs.append(new_dir)

    keep_source_folder = False

    for item in os.listdir(src_dir):
        if item in config.TRASH_FILES:
            continue

        ext = os.path.splitext(os.path.split(item)[1])[1]
        ext = ext.lstrip(".")
        orig_item = os.path.join(src_dir, item)
        new_item = new_dirname(src_dir, ext)
        using_same_source_folder = False

        if new_item == os.path.split(orig_item)[0]:
            using_same_source_folder = True
            keep_source_folder = True

        if not using_same_source_folder:
            try:
                log.debug(f"moving {orig_item} -> {new_item}")
                shutil.move(orig_item, new_item)
            except FileNotFoundError as e:
                log.warning(f"renaming {orig_item} -> {new_item}")
                raise

    if not keep_source_folder:
        shutil.rmtree(src_dir)

    # new dirs is in alphabetical order so for both
    # Canon and Sony cameras the JPG folder is second.
    # Sony ['indir_ARW', 'indir_JPG']
    # Canon ['indir_CR2, 'indir_JPG']

    return new_dirs
