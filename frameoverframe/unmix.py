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
import os
import re
import shutil

import frameoverframe.utils as utils


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
    ext_list.sort()

    if len(ext_list) <= 1:
        print("unmix: Looks good folder is already unmixed.", src_dir)
        return

    new_dirs = []

    for ext in ext_list:
        ext = ext.lstrip(".")

        new_dir = new_dirname(src_dir, ext)
        try:
            os.mkdir(new_dir)
        except FileExistsError:
            print("ERROR: Directory already exists. ", new_dir)
            return
        new_dirs.append(new_dir)

    for item in os.listdir(src_dir):
        if item == ".DS_Store":
            continue

        ext = os.path.splitext(os.path.split(item)[1])[1]
        ext = ext.lstrip(".")

        shutil.move(os.path.join(src_dir, item), new_dirname(src_dir, ext))

    shutil.rmtree(src_dir)

    return new_dirs
