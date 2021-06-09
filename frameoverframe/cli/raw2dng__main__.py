#!/usr/bin/env python3
"""
    ffmpeg wrapper
    takes a folder of images creates a video

"""


import argparse

from frameoverframe.raw2dng import raw2dng


def collect_args():
    """collect commandline arguments"""

    parser = argparse.ArgumentParser(
        description='Wrapper for "Adobe DNG Converter" \
                     Accepts a directory instead of individual files.'
    )

    parser.add_argument("input_dirs", nargs="+", help="directory of images...")
    parser.add_argument(
        "-o", "--output_dir", action="store", default=None, help="outputdirectory for the DNG files"
    )

    return parser


def main():
    """commandline setup img2vid"""

    parser = collect_args()
    args = parser.parse_args()

    raw2dng(args.input_dirs, args.output_dir)

    print("DONE.")


if __name__ == "__main__":
    main()
