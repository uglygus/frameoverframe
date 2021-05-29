#!/usr/bin/env python3
"""
    test_image

    Tests files one by one from many directories. Reports bad images to stdout.

"""

import argparse

from frameoverframe.test_images import test_images

def collect_args():
    """ collect commandline arguments """

    parser = argparse.ArgumentParser(
        description="Takes one or more folders of images and test each image"
                    "using ffmpeg's identify. Reports bad images to stdout.")


    parser.add_argument('input_dirs', nargs='+', help='directory(s) of images...')

 #   parser.add_argument( "-r", "--recursive", action="store_true", default=False,
 #       help="Descend into sub directories?. (default False)",
 #   )
    
    return parser

def main():
    """ commandline setup """

    parser = collect_args()
    args = parser.parse_args()

    print(f'{args=}')

    test_images(args.input_dirs) #, args.recursive)

if __name__ == '__main__':
    main()
