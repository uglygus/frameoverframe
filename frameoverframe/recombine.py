#!/usr/bin/env python3
"""
    Recombines folders of images

        accepts a list of directories to be combined and renumbered. Combines files into
        directories with max_files in each directory.


"""


import os
import shutil
import argparse
import sys
import re
import math
from time import strftime
from pathlib import Path

from .renumber import renumber
from .utils import sorted_listdir


def strip_bad_ending(string):
    """
    strips off spaces, underscores and dashes from the right of string
    Args:
      string:

    Returns:

    """
    return string.rstrip(' _-')


def _split_name_number(name):
    """Splits a given string into name and number where number is at the end
        of the string, e.g. 'foo2bar003baz_001' will be split into 'foo2bar003baz_'
        and '001'

    Args:
      name:

    Returns:

    """

    regex = r'^(.*?)(\d*)$'
    m = re.search(regex, name)
    name_part = m.group(1)
    num_part = m.group(2)

    return name_part, num_part


def recombine(src_dirs, dst_dir=None, copy_files=False, max_files=10000, prefix=':folder', padding=5):
    """Accepts a list of directories to be combined and renumbered. Combines files into
        directories with max_files in each directory.

    Args:
      src_dirs:
      dst_dir:  (Default value = None)
      copy_files:  (Default value = False)
      max_files:  (Default value = 10000)
      prefix:  (Default value = ':folder')
      padding:  (Default value = 5)

    Returns:

    """

    src_dirs.sort()

    if dst_dir is None:
        new_basename = _split_name_number(os.path.basename(src_dirs[0]))[0]
        #print('new_basename = ', new_basename)
        new_basename = strip_bad_ending(new_basename)
        #print('new_basename = ', new_basename)
        dst_dir = os.path.join(os.path.dirname(src_dirs[0]), new_basename)

    if prefix == ':folder':
        prefix = os.path.basename(os.path.normpath(src_dirs[0]))

    item_count = 0
    for directory in src_dirs:
        item_count += len(sorted_listdir(directory))

    dirs_needed = math.ceil(item_count / max_files)

    print('Creating', dirs_needed, 'new directories. For', item_count, 'items...')

    dst_dirs = []

    # only append a number to destination dirs if there is more than one
    for i in range(0, dirs_needed):
        if dirs_needed > 1:
            dst_dirs.append('{}_{:02d}'.format(dst_dir, i))
        else:
            dst_dirs.append(dst_dir)

    all_files = []

    for directory in src_dirs:

        for item in sorted_listdir(directory):
            if not os.path.isfile(os.path.join(directory, item)):
                continue
            all_files.append(os.path.join(directory, item))

    current_dir = 0
    count = 0

    tmp_dst_dirs = []
    for dst_dir in dst_dirs:
        if os.path.exists(dst_dir):
            print('WARNING: Output directory already exists.', dst_dir)
            dst_dir = dst_dir + '~recombined_' + strftime("%Y%m%d_%H%M%S")
            print('Renaming output directory to:', dst_dir)
        tmp_dst_dirs.append(dst_dir)
    dst_dirs=tmp_dst_dirs

    #print('dst_dirs=',dst_dirs)

    for item in all_files:
        if count >= max_files:
            count = 0
            current_dir += 1

        dst = dst_dirs[current_dir]

        if not os.path.exists(dst):
            os.makedirs(dst)

        item_dest = dst + '/' + os.path.basename(Path(item).parent) + '-' + os.path.basename(item)

        if copy_files:
          #  print('recombine copying : ', item, ' -->', item_dest)
            shutil.copyfile(item, item_dest)
        else:
          #  print('recombine moving : ', item, ' -->', item_dest)
            shutil.move(item, item_dest)
        count += 1

    # remove empty directories
    if not copy_files:
        for directory in src_dirs:
            shutil.rmtree(directory)

   # input('about to remove timestamps')
   # print('dst_dirs = ', dst_dirs)
    new_dst_dirs = []
    # remove empty directories
    # remove = 20200810_132823
    # ~recombined_20200810_133221
    # ~recombined_dddddddd_dddddd
    p = re.compile('(.+)~recombined_\d\d\d\d\d\d\d\d_\d\d\d\d\d\d')
    for directory in dst_dirs:
        m = p.search(directory)
        if m is None:
            new_dst_dirs.append(directory)
    #        print('m was None')
            continue
    #    print('m.group()=',m.group())
    #    print('m.group=1', m.group(1))
        new_dir = m.group(1)

        if os.path.exists(new_dir):
            new_dir= new_dir + '~recombined_' + strftime("%Y%m%d_%H%M%S")

       # print('shutil.move(', directory, ', ' ,new_dir)
        shutil.move(directory, new_dir)
        new_dst_dirs.append(new_dir)
    dst_dirs = new_dst_dirs

    #input('about to renumber')
    # renumber new files
    for one_dst_dir in dst_dirs:
        prefix = os.path.basename(os.path.normpath(one_dst_dir))
        renumber(one_dst_dir, inplace=True, prefix=prefix, sort_method='name', padding=padding)


def dir_path(path):
    """for argparse directory type test.

    Args:
      path:

    Returns:

    """
    if os.path.isdir(path):
        return path
    else:
        raise argparse.ArgumentTypeError(f"readable_dir:{path} is not a valid path")
