#!/usr/bin/env python3
"""
    This is an example of a frameoverframe module. It is a wrapper for the
    autotrace C program to do the actual tracing.

    modules take a PIL Image and return a PIL Image
    If they need to work with a file like autotrace does then they save the file
    process it and optionally keep the file for future runs.

    autotrace hi-mom-8bit.tga -output-file hi-mom.eps --despec kle-level 20

"""

import inspect
import os
import shutil
import sys
from pathlib import Path
from subprocess import PIPE, run

import quotelib

from .utils import *


def autotrace(img, filename, framenumber, centerline, save_png=False):
    """This is an example of a frameoverframe module
        modules take a PIL Image and return a PIL Image
        If they need to work with a file like autotrace does then they save the file
        process it and optionally keep the file for future runs.

       img :        a PIL image
       filename :   name of file the image is from ie. the video file
       framenumber :integer framenumber   in the video file

       returns: a PIL image or None

    Args:
      img: a PIL image
      filename (int): name of file the image is from ie. the video file
      framenumber (int): framenumber   in the video file
      centerline (bool): whether to used centerline only or outlines
      save_png (bool): wether to save a png version or not. (Default value = False)

    Returns:
        PIL Image or None
    """


    autotrace_bin = shutil.which('autotrace')
    if not autotrace_bin:
        print('ERROR: The autotrace binary is not in your PATH')
        sys.exit(1)


    filenameonly = Path(filename).stem
    # the inspect returns this functions name
    myname = inspect.currentframe().f_code.co_name

    indir = create_workdir(filename, myname + '-1-in')
    epsdir = create_workdir(filename, myname + '-2-eps')
    epsdir_big = create_workdir(filename, myname + '-4-eps_big')
    pngdir = create_workdir(filename, myname + '-3-png')

    infile = indir + '/' + filenameonly + '_{0:06d}'.format(framenumber) + ".tga"
    epsfile = epsdir + '/' + filenameonly + '_{0:06d}'.format(framenumber) + ".eps"
    epsfile_big = epsdir_big + '/' + filenameonly + '_{0:06d}'.format(framenumber) + ".eps"
    pngfile = pngdir + '/' + filenameonly + '_{0:06d}'.format(framenumber) + ".png"

    if file_not_exist(infile):
        #print('file not exist writing:', infile)
        # can give any format you like base on extentions .tga
        img.save(infile)

    if file_not_exist(epsfile):
        call_list = [ autotrace_bin,
                      infile,
                      '--output-file', epsfile,
                      '--despeckle-level', '20'
                    ]

        if centerline:
            call_list.append('--centerline')

        print('calling : ', ' '.join( quotelib.quote(call_list)))
     #   input('xxx abcd ...')
        result = run(call_list, stdout=PIPE, stderr=PIPE, universal_newlines=True)
        print('autotrace returncode={}, stdout={}, stderr={}'.format(result.returncode, result.stdout, result.stderr))

        if result.returncode:
            print('FAILED: ', myname)
            print('returncode = ', result.returncode)
            print('stdout = ', result.stderr)
            print('stderr = ', result.stderr)
            sys.exit(1)
    #
    # Premiere can read eps files directly so we do not need to save these
    # frameoverframe needs to get an image back but I am going to skip
    # that to speed things up.
    #
    im = None

    if file_not_exist(pngfile):
        if save_png:
            im = open_eps(epsfile, 3840)
            im.save(pngfile)

    print('about to consider upressing eps', epsfile_big)
    if file_not_exist(epsfile_big):
        print('upressing eps')
        resize_eps(epsfile, epsfile_big)
    else:
        print('upressed eps already exists!')

    return im or None
