#!/usr/bin/env python3

"""
    enfuse_batch.py

    enfuse a folder of images:

    enfuse is part of hugin
    brew cask install hugin
"""

from subprocess import run, PIPE
import os
import argparse
import sys
import random
import shutil
from pathlib import Path
import multiprocessing

from PIL import Image


def enfuse(infiles, output_file, counter, hardmask=False):

    #  output_file = os.path.abspath(output_file)
    outname = os.path.basename(os.path.dirname(os.path.abspath(output_file)))

    output_dir = os.path.dirname(os.path.dirname(output_file))

    print("output_dir=", output_dir)
    print("outname=", outname)

    enfuse_bin = shutil.which("enfuse")

    weight = dict(
        [
            ("exposure", 0.2),  # default 1
            ("saturation", 0.6),  # default 0.2
            ("contrast", 0.4),  # default 0
            ("entropy", 0.4),  # default 0
            ("hard-mask", hardmask),
        ]
    )

    file = open(output_dir + "/" + outname + "-settings.txt", "w")
    file.write(str(weight))
    file.close()

    sys_call = [
        enfuse_bin,
        "--exposure-weight=" + str(weight["exposure"]),
        "--saturation-weight=" + str(weight["saturation"]),
        "--contrast-weight=" + str(weight["contrast"]),
        "--entropy-weight=" + str(weight["entropy"]),
    ]

    if weight["hard-mask"]:
        print("hard masked!")
        sys_call.append("--hard-mask")

    sys_call.append("--output=" + output_file)

    for item in infiles:
        sys_call.append(item)

    print("calling :" + " ".join(sys_call))
    result = run(sys_call, stdout=PIPE, stderr=PIPE, universal_newlines=True, check=False)

    print(("returncode=", result.returncode))

    if result.returncode == -11:
        times = 1
        while returncode != 0:
            print(("enfuse FAILED!!!=", returncode, times, " times"))
            print("!!-->" + " ".join(sys_call))
            result = run(sys_call, stdout=PIPE, stderr=PIPE, universal_newlines=True, check=False)
            times += 1


def convert(image_path, output_file, counter):
    """constructs and calls  a system call to 'convert' the imagemagick command
    image_path (list) : a list of image paths to merge
    output_file (str) : the output file
    counter (int) : the counter of the current image (used to name output file)
    """

    convert_bin = shutil.which("convert")

    sys_call = [
        convert_bin,
    ]

    print("counter=", counter)
    print("image_path=", image_path)

    for item in image_path:
        sys_call.append(item)
    sys_call.append("-average")
    sys_call.append(output_file)

    print("calling : " + " ".join(sys_call))
    returncode = subprocess.call(sys_call)
    print(("returncode=", returncode))


def pil(image_path, output_file, counter):

    print("counter=", counter)
    print("image_path=", image_path)

    images = []

    count = 0

    img_master = Image.open(image_path[0])

    for image in image_path:

        alpha = len(image_path) * count / 2 / 100

        print("image=", image)
        print("alpha=", alpha)

        image_as_pill = Image.open(image)
        img_master = Image.blend(img_master, image_as_pill, alpha)
        #  img_master.save( 'out_img_master' + '{}'.format(count) +'__a='+ str(alpha) + '.png')
        count += 1

    img_master.save(output_file)


def shuffle_distance(list, max_distance):
    """
    shuffle a list by moving elements at most max_distance from their starting point
    distribution is a little counter intuitive: Given a list of 100 elements and a
    distance of 100 shuffle_distance(100,100) will still result in early elements being clustered at
    the front and later elements being clustered in the rear. since 100 will be the MAX distance
    and the distribution is center weighted. To get an even more random distribution
    use a distance several orders of magnitude larger than the list length. Like 10000
    for a 100 element list.
    https://stackoverflow.com/questions/30747690/controlling-distance-of-shuffling
    """
    return [
        x
        for i, x in sorted(
            enumerate(list), key=lambda i_x: i_x[0] + (max_distance + 1) * random.random()
        )
    ]


def process_dir(num, hardmask, shuffle_frames, skip_frames, method, input_dir, output_dir):
    """
    num : int, number of images to merge
    hardmask : bool, hardmask flag for enfuse
    shuffle_frames : int how far apart frames are allowed to be from their original locations
    skip_frames : number of frames to skip -- when working with brackets num and skipframes should be the same
    method : str, 'enfuse', 'convert', maybe more.
    input_dir :
    output_dir :
    """

    images = []

    # generate a list of all files : images[]
    for file in os.listdir(input_dir):
        if file.startswith(".") or not os.path.isfile(os.path.join(input_dir, file)):
            continue
        images.append(file)

    if shuffle_frames:
        images = shuffle_distance(images, shuffle_frames)
        print("shuffled within {} frames ".format(shuffle_frames))
    else:
        images.sort()
        print("sorted images")

    # print 'images=', images

    # align images with align_image_stack
    #     for counter in range(0, len(images) - num + 1, num):
    #
    #         image_path_list = []
    #         for n in range(num):
    #             image_path_list.append(
    #                 os.path.join(input_dir, images[counter + n]))
    #
    #         output_file = output_dir + "/out-" + str(counter).zfill(5) + ".png"
    #
    #         align_image_stack_sequence(image_path_list, skip_frames)
    #

    #  input('hi mom')

    jobs = []
    max_jobs = multiprocessing.cpu_count() - 2  # leave two cores free
    print("Using {} or {} cores.".format(max_jobs, multiprocessing.cpu_count()))

    print("jobs active = ", len(jobs))

    waiting_to_place_job = True

    # call enfuse/convert/pil on the stack
    for counter in range(0, len(images) - num + 1, skip_frames):

        print("counter ==", counter)
        print("jobs active = ", len(jobs))

        ##        input('going...')

        image_path = []
        for n in range(num):
            image_path.append(os.path.join(input_dir, images[counter + n]))

        print(("method=", method))
        output_file = output_dir + "/out-" + str(counter).zfill(5) + ".png"

        if os.path.isfile(output_file):
            print(("file already exists. Skipping = ", output_file))
            continue

        #         input('before while...')
        #         while waiting_to_place_job:

        #             print('top of while waiting_to place jobs, len(jobs=) ', len(jobs))
        #             print('counter ==', counter)
        #             print('jobs active = ', len(jobs))
        #             input('looking for job...')

        if len(jobs) < max_jobs:

            if method == "enfuse":
                enfuse(image_path, output_file, counter, hardmask)
            #                     p = multiprocessing.Process(target=enfuse, args=(image_path, output_file, counter, hardmask))
            #                     input('a...')
            #                     jobs.append(p)
            #                     input('b...')
            #                     p.start()
            #                     input('c...')

            elif method == "convert":
                convert(image_path, output_file, counter)
            #                     p = multiprocessing.Process(target=convert, args=(image_path, output_file, counter))
            #                     jobs.append(p)
            #                     p.start()

            elif method == "pil":
                pil(image_path, output_file, counter)
            #                     p = multiprocessing.Process(target=pil, args=(image_path, output_file, counter))
            #                     jobs.append(p)
            #                     p.start()

            else:
                print("unknown method")
                sys.exit()


#                 waiting_to_place_job = False

#             else:
#                 dots+=1
#                # print('all job slots are full sleeping...',str(dots), 'seconds', end='\r', flush=True)
#                 print('all job slots are full sleeping...')
#                 time.sleep(10)
#
#                 for job in jobs:
#                     if not job.is_alive():
#                         print('\njob {} finished removing'.format(job.pid) )
#                         jobs.remove(job)
#                         dots=2
