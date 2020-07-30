#!/usr/bin/env python3

import os
from pathlib import Path
from subprocess import PIPE, run
import sys
import re

from which import which

import quotelib


def file_not_exist(fpath):
    ''' returns True if:
            file doesn't exist OR file size is zero
    '''
    return not os.path.isfile(fpath) or os.stat(fpath).st_size == 0


def create_workdir(filename, action=''):
    '''
    creates and returns the workingdir for a given video file and module
    eg: filename = /test/out.mp4  action = autotrace
        returns: /test/out/autotrace
    '''

    directory = os.path.split(filename)[0]
    filenameonly = Path(filename).stem

    outdir = directory + '/' + filenameonly + '/' + action
    #print('making outdir - ', outdir)
    try:
        os.makedirs(outdir, exist_ok=True)
    except OSError as e:
        print('ERROR: creating folder {} \n {} '.format(filename, e) )
        sys.exit()

    return outdir


def open_eps(filename, width=None):
    ''' takes a filename and returns a scaled PIL Image
        scaling is done AFTER the image has been rasterized
        so this is not really that useful for scaling.
        use resize_eps() to scale epss without losing quality.
    '''

    print('width=', width)
    original = [float(d) for d in Image.open(filename).size]
    print('original=', original)
    scale = width / original[0]
    print('scale=', scale)
    im = Image.open(filename)

    print('new im size = ', im.size)

    if width is not None:
        print('scaling-loading')
        im.load(scale=math.ceil(scale))
        print('new im size after scaling = ', im.size)
    if scale != 1:
        print('scaling-thumbnail')
        im.thumbnail([int(scale * d) for d in original], Image.ANTIALIAS)
        print('new im size after thumbnail = ', im.size)

    print('sleeping 60...')
    time.sleep(60)
    return im

def get_eps_size(epsfile):

    width=None
    height=None

    pattern = re.compile("%%BoundingBox: (\d*) (\d*) (\d+) (\d+)")

    for i, line in enumerate(open(epsfile, 'r')):
        m = re.search(pattern, line)

        if m:
            width=int(m.groups()[2]) - int(m.groups()[0])
            height=int(m.groups()[3]) - int(m.groups()[1])
            break

   # print('get_eps_size({}) returning: ({}x{})'.format(epsfile,width,height))
    return (width,height)


def calculate_scale_factor( orig_tup, new_tup, allow_crop=False):

    '''
        Calculate the scale factor to apply to make one rect fit another rect.
        Will not stretch. Returns a float to be applied to both dimensions.

        orig_tup (tuple) : original dimensions (width,height) eg (1920,1080)
        new_tup (tuple) : new dimensions (width,height) eg (3840,2160)
        allow_crop (boolean) : True = make dimensions fill screen and crop excess
                               False = make dimensions fit within the new box leaving black bars

        returns float : the scale factor.
    '''

    # +1 so that we are always erring oversize
    x_ratio = round( new_tup[0] / orig_tup[0], 1 )
    y_ratio = round( new_tup[1] / orig_tup[1], 1 )

    print('x_ratio=', x_ratio)
    print('y_ratio=', x_ratio)

    if allow_crop:
        return min(x_ratio, y_ratio)
    else:
        return max(x_ratio, y_ratio)



def resize_eps(infile, outfile, newsize=(3840, 2160)):
    '''
        This needs to calculate the right scale based on the size of the input file
        requires ghostscript
        brew install gs
    '''

    print('resize_eps(', 'infile=', infile, ', outfile=', outfile, ', newsize=', newsize, ')')

    print('orig_sizze=', get_eps_size(infile))
    print('newsize=', newsize)
    scale =  calculate_scale_factor( get_eps_size(infile), newsize)
    print('scale=', scale)

    gs_bin = which('gs')

    print('hi mom')
    call_list = [gs_bin,
                 '-q',      # quiet
                 '-dBATCH',  # exit after last file
                 '-o', outfile, #   quotelib.quote(outfile),
                 '-sDEVICE=eps2write',
                 '-dDEVICEWIDTHPOINTS={}'.format(newsize[0]), '-dDEVICEHEIGHTPOINTS={}'.format(newsize[1]),
                 '-c', '\"<</Install {{ {:4.2f} {:4.2f} scale }}>> setpagedevice\"'.format(scale, scale),
                 '-f', infile, #//quotelib.quote(infile)
                 ]

    print('before')
    print('calling : ', ' '.join( quotelib.quote(call_list)))
    print('after')

    result = run(call_list, stdout=PIPE, stderr=PIPE, universal_newlines=True)
    print('gs returncode={}, stdout={}, stderr={}'.format(
        result.returncode, result.stdout, result.stderr))

    if result.returncode:
        print('FAILED: ', gs_bin)
        print('returncode = ', result.returncode)
        print('stdout = ', result.stderr)
        print('stderr = ', result.stderr)
        sys.exit(1)

    sys.exit()
