#!/usr/bin/env python3

"""
Renumbers image sequences by renaming them sequentially.
Can be used as a module or a called from the commandline.

For example: prodeng01.jpg prodeng11.png prodeng27.jpg
$renumber.py .
Would become: (split by sequence)
prodeng_00001.jpg prodeng_00002.jpg prodeng_00003.jpg

Includes options for adding padding, rename files in place or create new ones,
Includes options for adding padding, rename files in place or create new ones,
specify the start number of sequence etc. Please read through the renumber()
docstring for more.

"""
import logging
import os
import shutil
from datetime import datetime

import frameoverframe.utils as utils

log = logging.getLogger("frameoverframe")


def thin_shape():
    pass


# def keep_every_n()


def thin(src_dir, every, dst_dir=None, inplace=False):
    """
    thins files from a folder. Does not recurse into sum folders.
    keep 1 file; skip (every-1) files; keep 1 file ....

    src_dir[]: a list of source directories to be thinned

    every: keep every nth file. eg 2 = keep the first of every 2 files
           eg 16 = keep the first of every 16 files.

    dst_dir: destination directory
             If blank will create a new dir called input_dir_thinned_xxxxxx

    inplace: unimplemented
    """

    log.debug(f"thin() {src_dir=}, {dst_dir=}, {inplace=}")

    #    src_dirs.sort()

    #    for one_src_dir in src_dirs:
    utils.test_one_extension(src_dir)

    file_list = []

    # collect only the files we want - could check file type or extensions here
    # for one_src_dir in src_dirs:
    for f in os.listdir(src_dir):
        if f == ".DS_Store":
            continue
        if os.path.isfile(os.path.join(src_dir, f)):
            file_list.append(os.path.join(src_dir, f))

    file_list.sort()
    log.debug(f"SORTED:   {file_list=}")

    files_orig = len(file_list)

    # Create destination directory as required
    if dst_dir is None:

        if inplace:
            dst_dir = src_dir
        else:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            thinned_dir_name = "{0}_{1}_{2}".format(os.path.basename(src_dir), "thinned", timestamp)
            dst_dir = os.path.join(os.path.dirname(src_dir), thinned_dir_name)
            if not os.path.exists(dst_dir):
                os.makedirs(dst_dir)

    log.debug(f"BEFORE:   {file_list=}")

    file_list = file_list[::every]

    log.debug(f"AFTER:    {file_list=}")

    file_name, ext = os.path.splitext(file_list[0])
    name_part, num_part = utils.split_name_number(file_name)

    files_moved = 0
    for f in file_list:
        src_dir, src_name = os.path.split(f)

        dst_name = src_name

        src = os.path.join(src_dir, src_name)
        dst = os.path.join(dst_dir, dst_name)

        if inplace:
            log.debug(f"moving file: {src} -> {dst}")
            shutil.move(src, dst)
        else:
            log.debug(f"copying file: {src} -> {dst}")
            shutil.copy2(src, dst)
        files_moved += 1

    log.info(f"Original files: {files_orig}")
    log.info(f"Moved files: {files_moved}")
    log.info(f"Destination: {dst_dir}")
