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

def _split_name_number(name):
    # Splits a given string into name and number where number is the at the end
    # of the string, e.g. 'foo2bar003baz001' will be split into 'foo2bar003baz'
    # and '001'

    regex='^(.*?)(\d*)$'
    m = re.search(regex, name)
    name_part = m.group(1)
    num_part = m.group(2)

    return name_part, num_part


def renumber(src_dir, dst_dir=None, inplace=False, start_at=0, prefix=None, padding=5):
    """
    Renames files representing an image sequence in the given directory to
    number them sequentially.

    Args:
        src_dir (str): Path to source directory containing the image sequence

        dst_dir (str, optional): Path to destination directory where the
            renamed files should be created. If not specified or None, a
            directory named 'renumbered_XXXXXXXX' (where XXXXXXXX is a random
            number) is created in the `src_dir`. Defaults to None

        inplace (bool, optional): If true, the files are named in place and
            `dst_dir` is ignored. Defaults to False

        start_at (int, optional): The number at which the image sequence should
            start. For example if start_at=3 then images will be named as
            image03.jpg, image04.jpg, ....
            Default 0.

        prefix (str, optional): The prefix to place before the number in filenames.
            If not supplied it is generated from the first file in the sequence.

        padding (int, optional): Specifies the number of leading zeroes in the
            number part of the image file name. Defaults to 5.

    Returns(str):
        Path to the directory where renumbered files are created

    """

    file_list = []

    # collect only the files we want - could check file type or extensions here
    for f in os.listdir(src_dir):
        if f == '.DS_Store':
            continue
        if os.path.isfile(os.path.join(src_dir,f)):
            file_list.append(f)

    file_list.sort()

    # get prefix if it is not assigned
    if prefix == None:
        file_name, ext = os.path.splitext(file_list[0])
        name_part, num_part = _split_name_number(file_name)
        prefix = name_part

    # append the underscore to prefix only if it is not empty and doenst end in '_'
    if not prefix == '' and not prefix.endswith('_'):
        prefix = prefix + '_'

    # Create destination directory as required
    if dst_dir is None:

        if inplace:
            dst_dir = src_dir
        else:
            dir_only=os.path.basename(src_dir)
            renumbered_dir_name = '{0}_{1}_{2}'.format(os.path.basename(src_dir), 'renumbered', uuid.uuid4().hex[:8])
           # dst_dir = os.path.dirname(src_dir)
            dst_dir = os.path.join(os.path.dirname(src_dir), renumbered_dir_name)
            if not os.path.exists(dst_dir):
                os.makedirs(dst_dir)

    counter = start_at
    for f in file_list:
        file_name, ext = os.path.splitext(file_list[0])

        dst_file_name = '{0}{1}{2}'.format(prefix, str(counter).zfill(padding), ext)

        src = os.path.join(src_dir, f)
        dst = os.path.join(dst_dir, dst_file_name)

        if inplace:
           # print('moving file: ', src, '->', dst)
            shutil.move(src, dst)
        else:
           # print('copying file: ', src, '->', dst)
            shutil.copy2(src, dst)
        counter+=1

    return dst_dir



def renumber_many(src_dirs, dst_dir=None, inplace=False, start_at=0, max_number=10000, prefix=None, padding=5):
    '''
        accepts a list of directories to be combined and renumbered. Combines files into
        directories with max_number in each directory.
    '''


    for directory in src_dirs:
        d(directory)

        if len(directory) < max_number:
            print('len(directory)=', len(directory), 'which is less than max_number=', max_number)

