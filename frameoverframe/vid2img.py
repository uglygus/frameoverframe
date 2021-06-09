#!/usr/bin/env python3
"""
ffmpeg wrapper
Takes a video file and createws a folder of still images

"""

import subprocess
import os
import shutil
import sys
from PIL import Image
import tempfile

from quotelib import quote

from frameoverframe.utils import sorted_listdir, test_one_extension
import frameoverframe.utils as utils


def vid2img(input_mov, output_folder=None):
    """convert video file to a folder of images"""

    input_folder = os.path.dirname(input_mov)

    filename = os.path.splitext(os.path.basename(input_mov))[0]

    if not output_folder:
        output_folder = input_folder + "/" + filename

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    ffmpeg_bin = shutil.which("ffmpeg")

    input(" calling ffmpeg ...")

    if ffmpeg_bin:
        print("got here")
        sys_call = [
            ffmpeg_bin,
            "-i",
            input_mov,
            output_folder + "/" + filename + "_" + "%08d" + ".png",
        ]

        print("\ncalling : ", " ".join(quote(sys_call)), "\n")
        subprocess.call(sys_call)

    else:
        print("ERROR: ffmpeg is required and is not intstalled. ")
        sys.exit(1)
