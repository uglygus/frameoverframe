# to run all tests:
# $ cd frameoverframe/frameoverframe/tests, the inner one that has this test file>
# $ python -m unittest
#


# import logging
import os
import shlex
import shutil
import subprocess

# import os.path
# import sys
# import tempfile
# import unittest
from pathlib import Path

from frameoverframe.utils import exif_write_filename

#
# import frameoverframe as fof
#
# log = logging.getLogger("frameoverframe")
#


IM_COLORS = [
    "lightblue",
    "LightPink1",
    "MediumSpringGreen",
    "MediumForestGreen",
    "DarkSeaGreen2",
    "yellow",
    "gold2",
]


def file_count(dirname):
    return sum([len(files) for r, d, files in os.walk(dirname)])


def dir_count(dirname):
    return sum([len(d) for r, d, files in os.walk(dirname)])


def dummy_sdcard(dirname):

    sdcard = os.path.join(dirname, "SDCARD")
    os.makedirs(sdcard)
    # print("sdcard=", sdcard)

    lots_o_files(sdcard, prefix="DSC", ext="JPG")
    lots_o_files(sdcard, prefix="DSC", ext="ARW")

    # print("Done makeing dir ", sdcard, "and populating it.")

    return sdcard


def new_image(filepath, wh="3096x2160", color="lightblue"):
    """create a single jpg image with its filename in the image"""

    # convert -size 1920x1080 -background lightblue -fill blue  -pointsize 72 -gravity center label:Anthony label.jpg
    dirname, filename = os.path.split(filepath)
    convert_bin = shutil.which("convert")

    text = os.path.basename(dirname) + "/" + filename
    # print("wh=", wh)
    # input("wh...")

    # fmt: off
    sys_call = [convert_bin,
                "-size", wh,
                "-background", color,
                "-fill", "black",
                "-pointsize", "72",
                "-gravity", "center",
                "label:" + text,
                filepath,
                ]
    # fmt: on

    quoted_sys_call = [shlex.quote(i) for i in sys_call]
    print("Calling : " + " ".join(quoted_sys_call))

    result = subprocess.run(sys_call)
    if result.returncode != 0:
        print("convert call failed!")
        return 1


def lots_o_files(dirname, count=1000, prefix="", ext=""):
    """creates empty files"""
    for i in range(0, count):
        filename = f"{dirname}/{prefix}{i:05}.{ext}"
        Path(filename).touch()


def lots_o_images(dirname, count=1000, color="lightblue", prefix="", ext="JPG"):
    """creates image files with the filename as embedded text"""
    for i in range(0, count):
        filepath = f"{dirname}/{prefix}{i:05}.{ext}"
        new_image(filepath, color=color)
        exif_write_filename(filepath)
