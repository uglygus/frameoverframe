 #!/usr/bin/env python3
'''
Adobe DNG Converter wrapper

'''

import subprocess
import os
import shutil
import sys
from PIL import Image
import tempfile


from quotelib import quote

from frameoverframe.utils import sorted_listdir, test_one_extension
from frameoverframe.unmix import unmix
import  frameoverframe.utils as utils

def WSL_path_converter(path):

    # wslpath -w '/mnt/g/timelapse 2021/2021-01-17 beach-cooper_ARW/DSC08253.ARW'

    sys_call = [shutil.which('wslpath'), '-w', path]
    print('\ncalling : ', ' '.join(quote(sys_call)), '\n')
    winpath = subprocess.check_output(sys_call)
    winpath = winpath.strip()
    print('winpath=',winpath)

    return winpath

def raw2dng(input_dirs, output_dir):
    ''' convert RAW to DNG '''


    print(' top of raw2dng input_dirs=',input_dirs)

    Adobe_DNG_Converter_exe = shutil.which('Adobe DNG Converter.exe')
    if not Adobe_DNG_Converter_exe:
        print('ERROR: Adobe DNG Converter.exe is required and is not in the PATH. ')
        sys.exit(1)

    if not isinstance(input_dirs,list):
        input_dirs = [input_dirs]

    input_dirs.sort()

    for _dir in input_dirs:
        for file in sorted_listdir(_dir):
            winfile = WSL_path_converter(file)
            sys_call = [Adobe_DNG_Converter_exe, '-c', winfile]
            print('calling - RAW==', sys_call)
            print('\ncalling : ', ' '.join(quote(sys_call)), '\n')
            subprocess.call(sys_call)
        unmix(_dir)