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

from datetime import datetime

import  frameoverframe.utils as utils


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

    print(f'thin() {src_dir=}, {dst_dir=}, {inplace=}')

    src_dir.sort()

    for one_src_dir in src_dir:    
        utils.test_one_extension(one_src_dir)
    
    file_list=[]
    
    # collect only the files we want - could check file type or extensions here
    for one_src_dir in src_dir:
        for f in os.listdir(one_src_dir):
            if f == '.DS_Store':
                continue
            if os.path.isfile(os.path.join(one_src_dir,f)):
                file_list.append(os.path.join(one_src_dir,f))

        print(f'RAW:   {file_list=}')

        file_list.sort()
    
        print(f'SORTED:   {file_list=}')
    
        # Create destination directory as required
        if dst_dir is None:

            if inplace:
                dst_dir = one_src_dir
            else:
                dateTimeObj = datetime.now()
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S)")
                print('Current Timestamp : ', timestamp)
                dir_only=os.path.basename(one_src_dir)
                thinned_dir_name = '{0}_{1}_{2}'.format(os.path.basename(one_src_dir), 'thinned',timestamp)

                dst_dir = os.path.join(os.path.dirname(one_src_dir), thinned_dir_name)
                if not os.path.exists(dst_dir):
                    os.makedirs(dst_dir)


        print(f'BEFORE:   {file_list=}')

        file_list=file_list[::every]
    
        print(f'AFTER:    {file_list=}')
    
       # sys.exit()
    
        file_name, ext = os.path.splitext(file_list[0])
        name_part, num_part = utils._split_name_number(file_name)
        prefix = name_part
    
        for f in file_list:
          #  file_name, ext = os.path.splitext(file_list[0])

            src_dir, src_name = os.path.split(f)

            dst_name = src_name

            print(f'{src_dir=}, {src_name=}')

            
            src = os.path.join(src_dir, src_name)
            dst = os.path.join(dst_dir, dst_name)

            if inplace:
                print('moving file: ', src, '->', dst)
                shutil.move(src, dst)
            else:
                print('copying file: ', src, '->', dst)
                shutil.copy2(src, dst)
           



def renumber(src_dir, dst_dir=None, inplace=False, sort_method=None, start_at=0, prefix=None, padding=5):
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

        sort_method(str): Method to use for sorting the files. 'name'=sort by name,
            'exif_date'=sort by exit_date.

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

    utils.test_one_extension(src_dir)

    print('renumber start_at=', start_at)
    print('renumber prefix=', prefix)
    print('renumber inplace=', inplace)
    print('renumber sort_method=', sort_method)

    # collect only the files we want - could check file type or extensions here
    for f in os.listdir(src_dir):
        if f == '.DS_Store':
            continue
        if os.path.isfile(os.path.join(src_dir,f)):
            file_list.append(f)

    file_list_name = sort_by_name(file_list)
    if sort_method == "exif_date":
        file_list_date = sort_by_exif_date(file_list, src_dir)
    else:
        print('EXIF date not present. Sorting by name.')
        file_list_date = None
        sort_method = 'name'


    print(f'{file_list_name=}')
    print(f'{file_list_date=}')



    # double check sort_method
    if sort_method == None:
        if file_list_name != file_list_date:
            print(f'STOPPING: Alphanumeric order and exif date order do not match!. Specify a --sort_method on the commandline. For dir: {src_dir}')

            i=0
            for i in range(len(file_list_name)):
                if file_list_name[i] != file_list_date[i]:
                    print(f'differnet name=,{file_list_name[i]} --- {file_list_date[i]}')

            sys.exit(1)
        else:
            sort_method = 'name'

    print(f' sort method: {sort_method}')
    if sort_method == 'name':
        file_list = sort_by_name(file_list)
    elif sort_method == 'exif_date':
        file_list = sort_by_exif_date(file_list, src_dir)
    else:
        print(f'unknown sort method: {sort_method}')
        sys.exit(1)

    # get prefix if it is not assigned
    if prefix == None:
        file_name, ext = os.path.splitext(file_list[0])
        name_part, num_part = _split_name_number(file_name)
        prefix = name_part

    print(f'{prefix=}')

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
            print('moving file: ', src, '->', dst)
            shutil.move(src, dst)
        else:
            print('copying file: ', src, '->', dst)
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
