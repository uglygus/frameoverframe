#!/usr/bin/env python3

import argparse
import os
import sys

import frameoverframe.autotrace
import frameoverframe.autotrace_sequence


def collect_args():
    parser = argparse.ArgumentParser(description="process videos frame by frame.")
    parser.add_argument("input", default=None, nargs="*", help="video file, mov,mp4,m4a etc")
    parser.add_argument(
        "-c",
        "--centerline",
        action="store_true",
        default=False,
        dest="centerline",
        help="Trace the centerline of blobs. Produces lines only. ",
    )
    parser.add_argument(
        "-s",
        "--scalefactor",
        type=int,
        default=50,
        help="resize the image size before autotracing. \
                        Scale is a percentage. 50=half size, defalut = 50. \
                        4k images must be scaled down or autotrace will crash.",
    )
    parser.add_argument(
        "-j",
        "--jobs",
        default="0",
        type=int,
        help="Number of parallel prcesseses to spawn. default=0 (same as cpu count)",
    )
    return parser


def main():
    """do the main thing"""

    parser = collect_args()

    args = parser.parse_args()

    if not args.input:
        parser.print_help()
        return 0

    for single_input in args.input:

        #  print('single_input=', single_input)

        single_input = os.path.abspath(single_input)

        if os.path.isfile(single_input):
            frameoverframe.autotrace_sequence.process_file(single_input, args)

        if os.path.isdir(single_input):
            print("Cannot process directories. input must be a video file.")
            return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
