#!/usr/bin/env python3
"""
test_images - test each image in every input folder.
relies on identify from imagemagick
"""
import errno
import logging
import os
import shutil
import subprocess
import sys

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
        log.info("skipping (not a file): ", image)
        return None

    if ext in vid_exts:
        log.info("skipping : ", image)
        return None

    identify_bin = shutil.which("identify")

    sys_call = [identify_bin, image]

    result = subprocess.run(sys_call, capture_output=True)

    concat_result = str(result.stdout + result.stderr)
    #  log.info('concat_result=', concat_result)

    error_strings = [
        "no decode delegate for this image format",
        "Not a JPEG file",
        "Corrupt",
        "contains no image",
        "Premature end of JPEG file",
        "ImproperImageHeader",
        "NoDecodeDelegateForThisImageFormat",
    ]

    # log.info('image_error=', image_error)

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

    try:
        for image_dir in input_dirs:
            for image in sorted_listdir(image_dir):
                test_image = image
                print(f"{test_image=}")
                result = test_image(image)
                if result is not None:
                    log.debug(result)
    except FileNotFoundError as e:
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), filename)

    if 0 == len(sorted_listdir(image_dir)):
        print("Input directory contains no images.")
