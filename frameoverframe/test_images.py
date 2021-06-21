#!/usr/bin/env python3
"""
test_images - test each image in every input folder.
relies on identify from imagemagick
"""

import logging
import os
import shutil
import subprocess

from frameoverframe.utils import sorted_listdir

log = logging.getLogger("frameoverframe")


vid_exts = ["mov", "mp4", "avi"]


def test_image(image):
    """test a single image.

        Returns: None on success or non image file
                 error string on failure

    Args:
      image:

    Returns:
       None on success or non image file
       a string containing an error message otherwise
    """

    log.info(image)

    ext = os.path.splitext(image)[1]

    image_error = None

    if not os.path.isfile(image):
        print("skipping (not a file): ", image)
        return None

    if ext in vid_exts:
        print("skipping : ", image)
        return None

    identify_bin = shutil.which("identify")

    sys_call = [identify_bin, image]

    result = subprocess.run(sys_call, capture_output=True)

    concat_result = str(result.stdout + result.stderr)
    #  print('concat_result=', concat_result)

    error_strings = [
        "no decode delegate for this image format",
        "Not a JPEG file",
        "Corrupt",
        "contains no image",
        "Premature end of JPEG file",
        "ImproperImageHeader",
        "NoDecodeDelegateForThisImageFormat",
    ]

    # print('image_error=', image_error)

    for error_string in error_strings:
        if error_string in concat_result:
            image_error = "BAD image:" + image + " -- " + error_string

    return image_error


def test_images(input_dirs):
    """test every image in each directory

    Args:
      input_dirs:

    Returns:
      nothing
    """

    input_dirs.sort()

    for image_dir in input_dirs:
        for image in sorted_listdir(image_dir):
            result = test_image(image)
            if result is not None:
                print(result)
