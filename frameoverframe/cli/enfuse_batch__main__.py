#!/usr/bin/env python3

"""
    enfuse_batch.py

    enfuse a folder of images:

    enfuse is part of hugin
    brew cask install hugin
"""

from subprocess import run, PIPE
import os
import argparse
import sys
import random
import shutil
from pathlib import Path
import multiprocessing

from PIL import Image


from frameoverframe.enfuse_batch import process_dir


def collect_args():
    """collect commandline arguments"""

    parser = argparse.ArgumentParser(
        description="Blend several images together from an image sequence to create another "
        "image sequence using enfuse by Hugin."
    )

    parser.add_argument(
        "method",
        type=str,
        help="Method of averaging: 'convert' : ImageMagick -average, 'enfuse' : Hugin's enfuse, 'pil', python Pillow library.",
    )

    parser.add_argument("num", type=int, help="Number of images to combine per frame.")

    parser.add_argument(
        "-b",
        "--skip-frames",
        type=int,
        default=1,
        help="Number of images to skip. Ususally for doing HDR set this to the number of images in each set.",
    )

    parser.add_argument(
        "--shuffle-frames",
        nargs="?",
        const=1000000,
        type=int,
        default=0,
        help="shuffle frames by XXX frames (default = 1000000) Large default to get a completely random shuffle.",
    )

    parser.add_argument(
        "-m",
        "--hard-mask",
        action="store_true",
        default=False,
        dest="hardmask",
        help="force hard blend masks and no averaging on finest scale;but leads to increased noise",
    )

    parser.add_argument("input_dir", help="Input directory of images.")

    parser.add_argument(
        "-o",
        "--output_dir",
        dest="output_dir",
        default=None,
        help="Output directory; will be created if necessary.",
    )

    return parser


def main():
    """enfuse_batch do the main thing"""

    parser = collect_args()
    args = parser.parse_args()

    if not args.output_dir:
        args.output_dir = args.input_dir + "-enfused"

    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    process_dir(
        args.num,
        args.hardmask,
        args.shuffle_frames,
        args.skip_frames,
        args.method,
        args.input_dir,
        args.output_dir,
    )
    print("DONE.")


if __name__ == "__main__":
    main()
