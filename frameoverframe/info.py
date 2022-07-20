#!/usr/bin/env python3

"""
fof info

fps()
getbrightness()

"""

import math
import os
from datetime import datetime

import exifread
import matplotlib.pyplot as plt
from PIL import Image, ImageStat

import frameoverframe.utils as utils


def num_frames(dirfile):

    image_count = len(os.listdir(dirfile))
    print("Length: ", image_count, "frames")
    return image_count


def print_exif_tags(filename, alltags=False):

    # Open image file for reading (binary mode)
    f = open(filename, "rb")
    tags = exifread.process_file(f)

    if not tags:
        print(f"No EXIF tags : {filename}")
    else:
        print(f"{filename}")

    for tag in tags.keys():

        if alltags:
            if tag not in ("JPEGThumbnail", "TIFFThumbnail"):
                print(f"{tag} == {tags[tag]}")
        else:
            if tag in (
                "Image Make" "Image Model",
                "EXIF ExifImageWidth",
                "EXIF ExifImageLength",
                "EXIF ExposureTime",
                "EXIF FNumber",
                "Image DateTime",
                "LensModel",
                "MakerNote WhiteBalance",
            ):
                print(f"{tag} :  {tags[tag]}")


def get_brightness(filename):
    """Average pixels, then transform to "perceived brightness".
    sourced from here:
    https://stackoverflow.com/questions/3490727/what-are-some-methods-to-analyze-image-brightness-using-python
    """
    im = Image.open(filename)
    stat = ImageStat.Stat(im)
    print(filename, " stat= ", stat)
    r, g, b = stat.mean

    return math.sqrt(0.241 * (r**2) + 0.691 * (g**2) + 0.068 * (b**2))


def fps_pair(img1, img2):
    """

    calculated time difference betweeen images based on exif data

    Args:
        img1 (str): path to an image file
        img2 (str): path to an image file

    Returns(int):
        time in seconds between img1 and img2


    """

    # todo turn these into epochs so we can do some math

    img1date = utils.exif_creation_date(img1)
    img2date = utils.exif_creation_date(img2)

    # these will be None if there is no date in the exif
    if not img1date or not img2date:
        return 0

    img1date = datetime.strptime(img1date, "%Y:%m:%d %H:%M:%S")
    img2date = datetime.strptime(img2date, "%Y:%m:%d %H:%M:%S")

    diff = img2date - img1date

    return diff.total_seconds()


def fps_dir(input_dir):
    """

    calculated time difference betweeen images based on exif data

    Args:
        input_dir (str): path to a folder of images

    Returns(int):
        displays a graph of the fps

    """

    files = utils.sorted_listdir(input_dir)
    prev = ""
    prev = files[0]

    diffs = []
    for f in files:
        diff = fps_pair(prev, f)
        diffs.append(diff)
        print("diff=", diff)
        prev = f

    avg = sum(diffs) / len(diffs)
    print("The average is fps as shot is ", round(avg, 2), "seconds between frames.")

    plt.plot(diffs)
    plt.title(input_dir)
    plt.ylabel("seconds")
    plt.xlabel("frame #")
    plt.show()
