#!/usr/bin/env python3
"""
make_previews.py

given a folder check every subfolder and try to run img2vid on it.


"""

import os
import shutil
import argparse
import sys
import re

from frameoverframe.utils import sorted_listdir
from frameoverframe.img2vid import img2vid

def collect_args():
    """ collect commandline arguments """

    parser = argparse.ArgumentParser()

    parser.add_argument('src_dir',
        help="Source directory. ",
    )

    return parser

def main():
    """
    Can be called from the commmandline:
    usage: renumber.py [-h] [-o DST_DIR] [-i] [-s START_AT] [-x PREFIX] [-p PADDING] src_dir

    """

    parser = collect_args()
    args = parser.parse_args()

    for _dir in sorted_listdir(args.src_dir):

        print('\n' + f'{_dir=}')

        if os.path.isdir(_dir):
            if os.path.isfile(_dir + '.mp4'):
                print(f'Video file for {args.src_dir}/{_dir} already exists.')
            else:
                print(f'Need to make video for {_dir}.')
                img2vid(_dir, _dir + '.mp4')


if __name__ == "__main__":
    sys.exit(main())
