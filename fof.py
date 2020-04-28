#!/usr/bin/env python3

import os
import sys
import argparse
from pathlib import Path
import inspect
from subprocess import PIPE, run
import time
import math

import multiprocessing
import numpy

from moviepy.editor import VideoFileClip
from moviepy.editor import VideoClip
from moviepy.editor import ImageSequenceClip

from PIL import Image

from which import which


#AUTOTRACE = '/Users/tbatters/Documents-Mirrored/code/autotrace/autotrace'
AUTOTRACE = 'autotrace'

SAVE_PNG = True  # wether autotrace should save PNG files after making EPS files
SAVE_OUTPUT_MOV = False

RESIZE_TO_SPEEDUP = True
RESIZE = (910, 540)
#RESIZE = (1920,1080)


def file_not_exist(fpath):
    return not os.path.isfile(fpath) or os.stat(fpath).st_size == 0


def open_eps(filename, width=None):
    original = [float(d) for d in Image.open(filename).size]
    scale = width / original[0]
    im = Image.open(filename)
    if width is not None:
        im.load(scale=math.ceil(scale))
    if scale != 1:
        im.thumbnail([int(scale * d) for d in original], Image.ANTIALIAS)
    return im


def autotrace(img, filename, framenumber, centerline):
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

    autotrace_bin = which(AUTOTRACE)

    filenameonly = Path(filename).stem
    # the inspect returns this functions name
    myname = inspect.currentframe().f_code.co_name

    indir = create_workdir(filename, myname + '-1-in')
    epsdir = create_workdir(filename, myname + '-2-eps')
    pngdir = create_workdir(filename, myname + '-3-png')

    infile = indir + '/{0:06d}'.format(framenumber) + ".tga"
    epsfile = epsdir + '/{0:06d}'.format(framenumber) + ".eps"
    pngfile = pngdir + '/{0:06d}'.format(framenumber) + ".png"

    if file_not_exist(infile):
        #print('file not exist writing:', infile)
        # can give any format you like base on extentions .tga
        img.save(infile)

    if file_not_exist(epsfile):
        call_list = [autotrace_bin,
                     infile,
                     '--output-file', epsfile,
                     '--despeckle-level', '20']

        if centerline:
            call_list.append('--centerline')

        print('calling: ', ' '.join(call_list))
        result = run(call_list, stdout=PIPE, stderr=PIPE,
                     universal_newlines=True)
        print('autotrace returncode={}, stdout={}, stderr={}'.format(
            result.returncode, result.stdout, result.stderr))

        if result.returncode:
            print('FAILED: ', myname)
            print('returncode = ', result.returncode)
            print('stdout = ', result.stderr)
            print('stderr = ', result.stderr)
            sys.exit(1)

    #
    # Premiere can read eps files directly so we do not need to save thi
    # frameoverframe needs to get an image back but I am going to skip
    # that to speed things up.
    #
    if file_not_exist(pngfile):
        if SAVE_PNG:
            im = open_eps(epsfile, 3840)
           # im = Image.open(epsfile, )
           # im = im.convert("RGB")
           # im = im.resize( (3840,2160), Image.BICUBIC)
            im.save(pngfile)

            sys.stdout.flush()
            return im

    sys.stdout.flush()
    return im




def create_workdir(filename, action):
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


def process_file(filename, args):
    ''' process individual files. '''

    outdir = create_workdir(filename)

    images_list = []

    clip = VideoFileClip(filename)
    outclip = VideoClip()
    framenumber = 0

    print('clip size=', clip.size)

    num_processes = multiprocessing.cpu_count()
    print('num_processes', num_processes)

    jobs = []
    max_jobs = 10

    for frame in clip.iter_frames():

        print('frame number ==', framenumber)
        print('frame.shape==', frame.shape)

        print('jobs active = ', len(jobs))

        waiting_to_place_job = True

        while waiting_to_place_job:

            if len(jobs) < max_jobs:

                img = Image.frombytes(
                    'RGB', (clip.size[0], clip.size[1]), frame)

                if RESIZE_TO_SPEEDUP:
                    img = img.resize(RESIZE, Image.BICUBIC)

                print('working size =', img.size[0], 'x', img.size[1])


                p = multiprocessing.Process(target=autotrace, args=(
                    img, filename, framenumber, args.centerline))
                jobs.append(p)
                p.start()

                #print('type.img=', img)

                framenumber += 1

                img_np = numpy.asarray(img)
                images_list.append(img_np)

                waiting_to_place_job = False

            else:
                print('all job slots are full sleeping...')
                time.sleep(1)

                for job in jobs:
                   # print ('job :', job.pid)

                    if not job.is_alive():
                        print('job {} finished removing'.format(job.pid))
                        jobs.remove(job)

    if SAVE_OUTPUT_MOV:
        outclip = ImageSequenceClip(images_list, fps=24)
        outclip.write_videofile("xxxmovie.mp4", fps=24)


def main():
    ''' do the main thing '''
    parser = argparse.ArgumentParser(
        description='process videos frame by frame')
    parser.add_argument("input",
                        default=None, nargs='*', help="video file, mov,mp4,m4a etc")
    parser.add_argument('-c', '--centerline', action='store_true', default=False,
                        dest='centerline', help='recurse into directories')
    args = parser.parse_args()

    if not args.input:
        parser.print_help()
        return 0

    print('args=', args)

    for single_input in args.input:
        print('single_input=', single_input)

        if os.path.isfile(single_input):
            process_file(single_input, args)

        if os.path.isdir(single_input):
            print('Cannot process directories. input must be a video file.')
            return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
