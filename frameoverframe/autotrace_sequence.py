#!/usr/bin/env python3

import multiprocessing
import time

import numpy
from moviepy.editor import ImageSequenceClip, VideoClip, VideoFileClip
from PIL import Image

from .autotrace import autotrace

SAVE_OUTPUT_MOV = False

# MAX_JOBS = 10  # number of concurrent threads. MacBook Pro has 12 cores.


def process_file(filename, args):
    """process individual video files."""

    # outdir = create_workdir(filename)

    images_list = []

    clip = VideoFileClip(filename)
    outclip = VideoClip()
    framenumber = 0

    print("clip size=", clip.size)

    jobs = []

    if args.jobs == 0:
        #   max_jobs = multiprocessing.cpu_count() - 1   # leave one core free
        max_jobs = multiprocessing.cpu_count() - 1
    else:
        max_jobs = min(multiprocessing.cpu_count() - 1, args.jobs)

    print("max_jobs=", max_jobs)

    print("Using {} of {} cores.".format(max_jobs, multiprocessing.cpu_count()))
    dots = 2  # number of dots to print on the waiting to start job line

    for frame in clip.iter_frames():

        print("frame number ==", framenumber)

        print("jobs active = ", len(jobs))

        waiting_to_place_job = True

        while waiting_to_place_job:

            if len(jobs) < max_jobs:

                # print('original movie Clip.size =', clip.size[0], 'x', clip.size[1]  )

                img = Image.frombytes("RGB", (clip.size[0], clip.size[1]), frame)

                #                 print('orig width=', img.size[0])
                #                 print('args.scalefactor=', args.scalefactor)
                #                 print('new width=', int(img.size[0]*args.scalefactor / 100))

                resize = (
                    int(img.size[0] * args.scalefactor / 100),
                    int(img.size[1] * args.scalefactor / 100),
                )

                img = img.resize(resize, Image.LANCZOS)

                print(
                    "original size: ",
                    frame.shape[1],
                    "x",
                    frame.shape[0],
                    ", tracing size:",
                    img.size[0],
                    "x",
                    img.size[1],
                )

                p = multiprocessing.Process(
                    target=autotrace, args=(img, filename, framenumber, args.centerline)
                )
                jobs.append(p)
                p.start()

                framenumber += 1

                img_np = numpy.asarray(img)
                images_list.append(img_np)

                waiting_to_place_job = False

            else:
                dots += 1
                print("all job slots are full sleeping...", str(dots), "seconds", end="\r", flush=True)
                time.sleep(1)

                for job in jobs:
                    # print ('job :', job.pid)

                    if not job.is_alive():
                        print("\njob {} finished removing".format(job.pid))
                        jobs.remove(job)
                        dots = 2

    if SAVE_OUTPUT_MOV:
        outclip = ImageSequenceClip(images_list, fps=24)
        outclip.write_videofile(basename(filename) + .mp4, fps=24)
