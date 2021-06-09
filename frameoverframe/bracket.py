#!/usr/bin/env python3
"""Manipulate image sequences based on bracketing.

bracket.py

split:  Split files from one folder into several
        evenly distribute files one to each brackets dir alphabetically

merge:   Merge files from several folders into one
        number them sequentially in the final output.

can be run from the commandline or used as a python module
"""

import os
import shutil
import sys

from . import renumber


def split(brackets, input_dir):
    """Split files from one folder into several.

    Evenly distribute files one to each brackets dir alphabetically.

    brackets : number of directories to split the folder into
    input_dir : dir with files to split
    """
    if brackets < 2:
        print('There needs to be at least 2 brackets. I got ',
              brackets, ' brackets.')
        print('Exiting.')
        sys.exit(1)

    for i in range(brackets):
        os.makedirs(input_dir + '_' + str(i+1), exist_ok=True)

    allfiles = []
    for root, dirs, files in os.walk(input_dir, topdown=True):  # pylint: disable=unused-variable
        for name in files:
            allfiles.append((root, name))

    allfiles.sort()

    counter = 1

    for root, name in allfiles:

        print('counter=', counter, ' MV ', root+'/'+name,
              input_dir + '_' + str(counter) + '/' + name)

        shutil.move(root+'/'+name, input_dir + '_' + str(counter) + '/' + name)
        counter += 1
        if counter == brackets + 1:
            counter = 1

    for i in range(brackets):
        renumber.renumber(input_dir + '_' + str(i+1), inplace=True)

    shutil.rmtree(input_dir)


def merge(input_dirs):
    """Merge files from several folders into one.

    Number them sequentially in the final output.

    input_dirs : a list of directory paths
    returns : the new merged directory
    """
    input_dirs.sort()

    print('\ninput_dirs=', input_dirs)

    outdir = os.path.commonprefix(input_dirs).rstrip('_').rstrip('-')

    try:
        os.makedirs(outdir)
        print('made outdir')
    except FileExistsError:
        print('Output direcotry already exists.', outdir)
        sys.exit()

    dir_lists = []

    for input_dir in input_dirs:

        print('\ninput=', input_dir)

        thisdirlist = []

        for file in os.listdir(input_dir):
            if file == '.DS_Store':
                continue
            thisdirlist.append(file)

        thisdirlist.sort()

        thisdirlist = [input_dir + '/' + d for d in thisdirlist]

        print('thisdirlist=', thisdirlist)

        dir_lists.append(thisdirlist)

    print('dir_lists=', dir_lists)

    counter = 0
    keepgoing = True
    dir_list = None
    while keepgoing:
        for dir_list in dir_lists:

            print('current dir_list == ', dir_list)

            try:
                orig_file_path = dir_list.pop(0)
                print('POP done, orig_file_path=', orig_file_path)
                print('after pop current dir_list == ', dir_list)

            except IndexError:
                print('Empty directory breaking.')
                keepgoing = False
                continue

            orig_file = os.path.split(orig_file_path)[1]

            print("shutil.move(", orig_file_path, ", ",
                  outdir + '/' + str(counter) + '_'+orig_file)
            shutil.move(orig_file_path, outdir + '/' +
                        str(counter) + '_'+orig_file)

            counter += 1

    for d in input_dirs:  # pylint: disable=invalid-name
        shutil.rmtree(d)

    return outdir
