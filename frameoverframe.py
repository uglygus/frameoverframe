#!/usr/bin/env python3

import os
import sys
import argparse
from pathlib import Path
import inspect
from subprocess import PIPE, run, call

import numpy

import cv2
from moviepy.editor import VideoFileClip
from moviepy.editor import VideoClip
from moviepy.editor import ImageSequenceClip

from PIL import Image

from which import which


AUTOTRACE = '/Users/tbatters/Documents-Mirrored/code/autotrace/autotrace'

SAVE_PNG = False #wether autotrace should save PNG files

import os
def file_not_exist(fpath):  
    return not os.path.isfile(fpath) or os.stat(fpath).st_size == 0
    
    

def autotrace(img, filename, framenumber):
    '''
        This is an example of a frameoverframe module
        modules take a PIL Image and return a PIL Image
        If they need to work with a file like autotrace does then they save the file 
        process it and optionally keep the file for future runs.
       
       img :        a PIL image 
       filename :   name of file the image is from ie. the video file
       framenumber :integer framenumber   in the video file
        
        autotrace hi-mom-8bit.tga -output-file hi-mom.eps --despeckle-level 20
    '''


    filenameonly = Path(filename).stem
    myname=inspect.currentframe().f_code.co_name    # the inspect returns this functions name

    indir = create_workdir(filename, myname + '-1-in')
    epsdir = create_workdir(filename, myname + '-2-eps')
    pngdir = create_workdir(filename, myname + '-3-png')

    autotrace_bin = which(AUTOTRACE)

    infile = indir + '/{0:06d}'.format(framenumber) + ".tga"
    epsfile = epsdir + '/{0:06d}'.format(framenumber) + ".eps"
    pngfile = pngdir + '/{0:06d}'.format(framenumber) + ".png"

    if file_not_exist(infile):
        print('file not exist writing:', infile)
        img.save(infile)  # can give any format you like base on extentions .tga 


    if file_not_exist(epsfile) :
        call_list = [autotrace_bin,
                     infile,
                     '--output-file', epsfile,
                     '--despeckle-level', '20',
                     '-centerline'
                    ]
        print('calling: ', ' '.join(call_list))
        result = run(call_list, stdout=PIPE, stderr=PIPE, universal_newlines=True)
        print(result.returncode, result.stdout, result.stderr)

        if result.returncode:
            print('FAILED: ', myname)
            print( result.stderr)
            raise


    #
    # Premiere can read eps files directly so we do not need to save thi
    # frameoverframe needs to get an image back but I am going to skip 
    # that to speed things up.
    # 
    if file_not_exist(pngfile) :
        if (SAVE_PNG):
            im = Image.open(epsfile)    
            im = im.convert("RGB")
            im = im.resize( (3840,2160), Image.BICUBIC) 
            im.save(pngfile)

            return(im)
    return 

def create_workdir(filename, action=''):
    '''
    creates and returns the workingdir for a given video file and module
    eg: filename = /test/out.mp4  action = autotrace
        returns: /test/out/autotrace
    '''

    directory = os.path.split(filename)[0]
    filenameonly = Path(filename).stem

    outdir = directory + '/' + filenameonly + '/' + action
    os.makedirs(outdir, exist_ok=True)
    return outdir


def process_file(filename):
    ''' process individual files. '''

    outdir = create_workdir(filename)
    filenameonly = Path(filename).stem

    print('outdir okay =', outdir)

    images_list=[]

    clip = VideoFileClip(filename)
    
    
    
    print('clip size=',clip.size)
    
    outclip = VideoClip()
    framenumber = 0
    for frame in clip.iter_frames():


      #  print('frames==',frame,'|||||||')
        print('frame.shape==', frame.shape)
        
       # input('aksdjgf')
       # print('type(frames)==',type(frame.shape))
       # print('type(frames.shape)==',type(frame.shape))

       # rawData = open("foo.raw", 'rb').read()
        #img_size = (1920,1080)# the image size
        img = Image.frombytes('RGB', (clip.size[0], clip.size[1]), frame)
        img = autotrace(img, filename, framenumber)

        print('type.img=', img)

        framenumber+=1

        img_np = I = numpy.asarray(img)
        images_list.append(img_np)


    outclip = ImageSequenceClip(images_list, fps=24)
    outclip.write_videofile("xxxmovie.mp4",fps=24)


    print(framenumber)

def main():
    ''' do the main thing '''
    parser = argparse.ArgumentParser(
        description='process videos frame by frame')
    parser.add_argument("input",
                        default=None, nargs='*', help="video file, mov,mp4,m4a etc")

    args = parser.parse_args()

    if not args.input:
        parser.print_help()
        return 0

    print('args=',args)


    for single_input in args.input:
        print('single_input=', single_input)

        if os.path.isfile(single_input):
            process_file(single_input)

        if os.path.isdir(single_input):
            print('Cannot process directories. input must be a video file.')
            return 1

    return 0

if __name__ == "__main__":
    sys.exit(main())
