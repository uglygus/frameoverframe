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
import shutil
import argparse
import sys
import re

import  frameoverframe.utils as utils

def new_dirname(src_dir, ext):
    """ returns a new dirname based on ext of a file

        src_dir  the original dir
        ext      the extension of one of the files in src_dir

        eg. new_dirname(/path/to/final/, 'JPG')

        Returns(str):
            /path/to/final_JPG
    """

    return os.path.join(os.path.dirname(src_dir), os.path.basename(src_dir) + '_' + ext )


def unmix(src_dir):
    """
    unmix's images that are stored in the same folder. This helps with Canon folders
    which store the CR2 and JPG files in the same folder.

    Args:
        src_dir (str): Path to source directory containing the image sequences

    Returns():
        none

    """

    file_list = []

    if len(utils.ext_list(src_dir)) <= 1 :
        print('OK: Looks good folder is already unmixed.', src_dir)
        return

    ext_list = utils.ext_list(src_dir)

    for ext in ext_list:
        ext = ext.lstrip('.')
        try:
            os.mkdir( new_dirname(src_dir, ext) )
        except FileExistsError:
            print('ERROR: Directory already exists. ', new_dirname(src_dir, ext) )
            return


    for item in os.listdir(src_dir):
        if item == '.DS_Store':
            continue

        ext = os.path.splitext(os.path.split(item)[1])[1]
        ext = ext.lstrip('.')

        shutil.move(os.path.join(src_dir,item), new_dirname(src_dir, ext))

    shutil.rmtree(src_dir)
