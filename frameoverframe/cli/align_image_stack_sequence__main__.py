#!/usr/bin/env python3
"""
    fof module align_image_stack_sequence

"""

import os
import sys
import argparse

from frameoverframe.align_image_stack_sequence import align_image_stack_sequence


def collect_args():
    """collect commandline arguments"""

    parser = argparse.ArgumentParser(
        description='wrapper for align_image_stack to be used on image sequences')
    parser.add_argument('-b', '--brackets', required=True, type=int,
                        dest='brackets', help='number of brackets')

    parser.add_argument("input", nargs='*', default=None, help="folder(s)")
    return parser


def main():
    """align a sequence of images that are bracketed images
        img0001.jpg - exposure A
        img0002.jpg - exposure B
        img0003.jpg - exposure C
        img0004.jpg - exposure A
        img0005.jpg - exposure B
        img0006.jpg - exposure C
    
        img001.jpg - img003.jpg will be aligned to img0001.jpg
        img004.jpg - img006.jpg will be aligned to img0004.jpg
    
        produces:
    
        img0001.tif ... img0006.tif

    Args:

    Returns:
      int: Exit code, 0 on success, 1 on failure.

    """

    parser = collect_args()
    args = parser.parse_args()

    if not args.input:
        parser.print_help()
        return 0

    for single_input in args.input:

        if os.path.isdir(single_input):
            image_list = []
            for item in os.listdir(single_input):
                if item.startswith('.') or not os.path.isfile(os.path.join(single_input, item)):
                    continue
                image_list.append(os.path.join(single_input, item))
                image_list.sort()
            align_image_stack_sequence(image_list, args.brackets)

        else:
            print('Cannot process files. input must be a direcotry of images')
            return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
