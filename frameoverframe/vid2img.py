#!/usr/bin/env python3
"""
ffmpeg wrapper
Takes a video file and createws a folder of still images

"""

import logging
import os
import shlex
import shutil
import subprocess
import sys

log = logging.getLogger("frameoverframe")


def vid2img(input_mov, output_folder=None):
    """convert video file to a folder of images"""

    log.debug(f"input_mov = {input_mov}")
    input_folder = os.path.dirname(input_mov)
    log.debug(f"input_folder= {input_folder}")
             
    filename = os.path.splitext(os.path.basename(input_mov))[0]

    if not output_folder:
        output_folder = os.path.join(input_folder, filename)

    log.debug(f"creating output_folder= {output_folder}")
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    ffmpeg_bin = shutil.which("ffmpeg")

    if ffmpeg_bin == None:
        raise FileNotFoundError("FFMPEG binary not found in your $PATH.")

    if log.level <= logging.DEBUG:
        ff_logflags = []
    elif log.level == logging.INFO:
        ff_logflags = ["-loglevel", "error", "-stats"]
    elif log.level >= logging.WARN:
        ff_logflags = ["-loglevel", "error", "-nostats"]

    sys_call = [ffmpeg_bin]
    sys_call.extend(ff_logflags)
    sys_call.extend(
        [
            "-i",
            input_mov,
            output_folder + "/" + filename + "_" + "%08d" + ".jpg",
        ]
    )

    quoted_sys_call = [shlex.quote(i) for i in sys_call]
    log.info("Calling : " + " ".join(quoted_sys_call))

    subprocess.call(sys_call)
