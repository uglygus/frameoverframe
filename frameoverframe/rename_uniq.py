#!/usr/bin/env python3
"""
cmdline-template.py
python template to process command line files and folders
option to run recursively
"""

import argparse
import os
import errno
import subprocess
import sys


def already_renamed(filename):
    ''' returns true if a filename starts with enclosing folders name
        followed by an underscore.
    '''

    prefix = os.path.basename(os.path.split(filename)[0])
    fileonly = os.path.basename( os.path.normpath(filename))
   
    if fileonly.startswith(prefix):
        return True
    return False


def rename_uniq_file(filename):
    ''' rename individual files so they have a prefix matching the enclosing folder.
        developed  for image sequences

        ./A_Video/00000.png --> ./A_Video/A_Video_00000.png

    '''

    directory = os.path.split(filename)[0]
    file = os.path.split(filename)[1]
    ext = os.path.splitext(os.path.split(filename)[1])[1]
    enc_dirname = os.path.basename(os.path.split(filename)[0])

#     print('rename_uniq_file::')
#     print('filename=', filename)
#     print('directory=', directory)
#     print('file=', file)
#     print('ext=', ext)
#     print('enc_dirname=',enc_dirname)

    if already_renamed(filename):
        print('filename already starts with enclosing folder, skipping:', filename)
        return


    newfilename = os.path.join(directory, enc_dirname + '_' + file)
  #  print('newfilename=', newfilename)

    orig_path = os.path.join(directory, filename)
    new_path = os.path.join(directory, newfilename)

    print('moving ', orig_path, '->', new_path)
    os.rename(orig_path, new_path)

    return

def rename_uniq_dir(dirname):
    ''' process individual directory. '''

    file_list = []
    for f in os.listdir(dirname):
        if f == '.DS_Store':
            continue
        if os.path.isfile(os.path.join(dirname,f)):
            file_list.append(os.path.join(dirname,f))

    file_list.sort()

 #   print('file_list=', file_list)

    for f in file_list:
        rename_uniq_file(f)

    return
