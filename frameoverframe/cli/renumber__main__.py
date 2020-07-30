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
import os
import shutil
import uuid
import argparse
import sys
import re

from frameoverframe.renumber import renumber


def main():
    '''
        Can be called from the commmandline:
    usage: renumber.py [-h] [-o DST_DIR] [-i] [-s START_AT] [-x PREFIX] [-p PADDING] src_dir

    '''
    parser = argparse.ArgumentParser()

    parser.add_argument('src_dir',
        help="Source directory. ",
    )

    parser.add_argument( "-o", "--dst_dir", type=str, default=None,
        help="Destination directory",
    )

    parser.add_argument( "--safe", action="store_true", default=False,
        help="Copy files to a new direcotory otherwise they are renamed inplace. (default False)",
    )

    parser.add_argument( "-s", "--start_at", type=int, default=0,
        help="Start number for renaming sequence. (default 0)",
    )

    parser.add_argument( "-x", "--prefix", type=str, default=None,
        help="Prefix. (default no prefix). '' empty string will strip any existing prefix. The special word :folder will use the enclosing folder's name as the prefix.",
    )

    parser.add_argument( "-p", "--padding", type=int, default=5,
        help="How many digits for number. (default 5) eg. 00001.jpg",
    )

    args = parser.parse_args()

    print('args=', args)


    if args.prefix == ':folder':
        print(' him om')
        print('dirname=', os.path.dirname(args.src_dir) )
        print('basename=', os.path.basename(args.src_dir) )

        print('normbasename=', os.path.basename( os.path.normpath(args.src_dir)) )
        prefix = os.path.basename( os.path.normpath(args.src_dir))

        print('prefix=', prefix)

        args.prefix = prefix


    renumber(
        args.src_dir,
        dst_dir = args.dst_dir,
        inplace = not args.safe,
        start_at = args.start_at,
        prefix = args.prefix,
        padding = args.padding,
    )

if __name__ == "__main__":
    sys.exit(main())
