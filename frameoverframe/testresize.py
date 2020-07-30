#!/usr/bin/env python3

import os
import sys
import argparse
import time
import multiprocessing


import numpy
from moviepy.editor import VideoFileClip
from moviepy.editor import VideoClip
from moviepy.editor import ImageSequenceClip
from PIL import Image

import utils

from autotrace import autotrace



def tuptest(atuple, btuple, okay=False):

    print('type atuple=', type(atuple))

    print('atuple=',atuple)
    print('btuple=',btuple)

def main():
    ''' do the main thing '''

    infile='/Users/tbatters/BIG-STUFF/trace-fiddlehead/fiddlehead_small.eps'
    outfile='fiddlehead_out4k.eps'


    xy=(1920,1080)

    print('xy=',xy)
    tuptest( (12,13), (0,0) )
    tuptest( xy, (12,13))


    orig_size = utils.get_eps_size(infile)

    print('orig_size =',orig_size )


    four_k = (3840,2160)

    utils.calculate_scale_factor( orig_size, four_k )



    utils.resize_eps(infile, outfile, newsize=(3840, 2160))


if __name__ == "__main__":
    sys.exit(main())
