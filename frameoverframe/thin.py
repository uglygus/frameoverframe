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
import logging
import math
import os
import shutil
from datetime import datetime

import frameoverframe.utils as utils
from frameoverframe.config import FILES_TO_IGNORE, RAW_EXTENSIONS

log = logging.getLogger("frameoverframe")


def thin_shape(file_list):
    # importing the required modules
    import matplotlib.pyplot as plt
    import numpy as np

    # setting the x - coordinates
    #    x = np.arange(0, 2 * (np.pi), 0.1)
    # x = np.arange(0, len(file_list) * 100, 1)
    # setting the corresponding y - coordinates
    x = np.linspace(-1 * (len(file_list) / 2), (len(file_list) / 2), len(file_list))
    y = x ** 2
    print(f"{x=}")
    print(f"{y=}")
    # potting the points
    # plt.plot(x, y)

    # function to show the plot
    # plt.show()

    input(" plot2...")
    # fmt: off
    #x=[0,0,0,1,1,0,1,0,1,0,0,0,0,1,0,1,1,1,1,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,0]
    x1=[]
    y1=[]
    x2=[]
    y2=[]
    count=1
    print('len(file_list=)', len(file_list))


    skip=False
    scount=0
    prev_calc=1
    prev_diff=1
    print(f"{prev_calc=}")
    for i in range(1, len(file_list)):
        print("len(file_list)/i == ", len(file_list)/i)
        print(f"{prev_calc=}")
        calc=prev_calc**2

        print(f"{calc=}")
        print(f"{prev_calc=}")
        diff = calc-prev_calc
        print(f"{diff=}")

        result=diff-prev_diff
        print(f"{result=}")
        prev_calc=calc**2+1
        result2=result/abs(prev_calc)
        print(f"{result2=}")
        result3=abs(result2)*result2
        print(f"{result3=}")
        result4=(result3 / result3+diff)
        print(f"{result4=}")

        if (result3 / abs(result2)) == 0:
            skip=True
        else:
            skip=False
        if not skip :
            print(f"{i} = 1")
            x1.append(1)
        else:
            print(f"{i} = 0")
            x1.append(0)


        if (result3 % 3) == 0:
            skip=True
        else:
            skip=False
        if not skip :
            print(f"{i} = 1")
            x2.append(1)
        else:
            print(f"{i} = 0")
            x2.append(0)
        count=count+1
        prev_diff=diff
    # x.append((i%(len(file_list)/2-i)**2)%2)
    # input('iii')
    # fmt: on
    y1 = range(0, len(x1))
    y2 = range(0, len(x2))

    # plt.bar(x, y, color="maroon", width=0.4)
    plt.style.use("seaborn-whitegrid")
    plt.plot(y1, x1, "o", color="red")
    plt.plot(y2, x2, "o", color="black")
    plt.show()

    # for i in x:
    #     print(i)
    # for item in file_list:
    #     print(item)
    #
    # print("len(x)=", len(x))
    #
    # new_file_list = []
    # count = 0
    # for item in file_list:
    #     print(item)
    #     print("keeping 1 in count")
    #     count + 1
    # input(",.....)")
    # pass


def thin_simple(file_list, every):
    # file_list = file_list[::every]
    return file_list[::every]
    # pass


def thin(src_dir, every, dst_dir=None, inplace=False):
    """
    thins files from a folder. Does not recurse into sum folders.
    keep 1 file; skip (every-1) files; keep 1 file ....

    src_dir[]: a list of source directories to be thinned

    every: keep every nth file. eg 2 = keep the first of every 2 files
           eg 16 = keep the first of every 16 files.

    dst_dir: destination directory
             If blank will create a new dir called input_dir_thinned_xxxxxx

    inplace: unimplemented
    """

    log.debug(f"thin() {src_dir=}, {every=}, {dst_dir=}, {inplace=}")

    #    src_dirs.sort()

    #    for one_src_dir in src_dirs:
    utils.test_one_extension(src_dir)

    file_list = []

    # collect only the files we want - could check file type or extensions here
    # for one_src_dir in src_dirs:
    for f in os.listdir(src_dir):
        if f in FILES_TO_IGNORE:
            continue
        if os.path.isfile(os.path.join(src_dir, f)):
            file_list.append(os.path.join(src_dir, f))

    file_list.sort()
    log.debug(f"SORTED:   {file_list=}")

    file_list = range(0, 200)

    files_orig = len(file_list)

    # Create destination directory as required
    if dst_dir is None:

        if inplace:
            dst_dir = src_dir
        else:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            thinned_dir_name = "{0}_{1}_{2}".format(os.path.basename(src_dir), "thinned", timestamp)
            dst_dir = os.path.join(os.path.dirname(src_dir), thinned_dir_name)
            if not os.path.exists(dst_dir):
                os.makedirs(dst_dir)

    log.debug(f"BEFORE:   {file_list=}")

    # choose which files to keep
    file_list = thin_simple(file_list, every)
    file_list = thin_shape(file_list)

    log.debug(f"AFTER:    {file_list=}")

    file_name, ext = os.path.splitext(file_list[0])
    name_part, num_part = utils.split_name_number(file_name)

    files_moved = 0
    for f in file_list:
        src_dir, src_name = os.path.split(f)

        dst_name = src_name

        src = os.path.join(src_dir, src_name)
        dst = os.path.join(dst_dir, dst_name)

        if inplace:
            log.debug(f"moving file: {src} -> {dst}")
            shutil.move(src, dst)
        else:
            log.debug(f"copying file: {src} -> {dst}")
            shutil.copy2(src, dst)
        files_moved += 1

    log.info(f"Original files: {files_orig}")
    log.info(f"Moved files: {files_moved}")
    log.info(f"Destination: {dst_dir}")
