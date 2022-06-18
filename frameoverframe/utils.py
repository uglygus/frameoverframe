#!/usr/bin/env python3

import inspect
import logging
import math
import os
import re
import shlex
import shutil
import sys
from functools import reduce
from itertools import product, takewhile
from pathlib import Path
from subprocess import PIPE, run

import exifread  # legacy, used this to read tags
from exif import Image as exifImage  # need this to write tags
from exif import LightSource
from PIL import Image

import frameoverframe.config as config

log = logging.getLogger("frameoverframe")

import frameoverframe.utils as utils


def exif_creation_date(filename):
    """given an image file return the creation time: EXIF DateTimeOriginal."""

    # Open image file for reading in binary mode
    try:
        fh = open(filename, "rb")
    except FileNotFoundError:
        return ()

    tags = exifread.process_file(fh, stop_tag="DateTimeOriginal", details=False)

    try:
        exifdate = tags["EXIF DateTimeOriginal"].printable
    except KeyError:
        exifdate = None

    return exifdate


def exif_read_filename(filename):
    """given an image file read the exif tag that contains the original filename"""

    with open(filename, "rb") as image_file:
        my_image = exifImage(image_file)

        if my_image.has_exif == False:
            raise TypeError("image has no EXIF tags.", my_image)

        # print("exif_add_filename_tag() : filename=", filename)
        # print("my_image.has_exif=", my_image.has_exif)
        # print("my_image has tags:", my_image.list_all())

        # my_image.original_filename = filename
        # my_image.image_description = filename
        # my_image.light_source = LightSource.DAYLIGHT

        # print("my_image.has_exif=", my_image.has_exif)
        # print("now my_image has tags:", my_image.list_all())
        # print("my_image.image_description = ", my_image.image_description)

        # print("exif_read_filename returning=", my_image.image_description)
        return my_image.image_description
    return


def exif_write_filename(filename):
    """given an image file add an exif tag that contains the current filename"""

    with open(filename, "rb") as image_file:
        my_image = exifImage(image_file)

        # print("exif_add_filename_tag() : filename=", filename)
        # print("my_image.has_exif=", my_image.has_exif)
        # print("my_image has tags:", my_image.list_all())

        # my_image.original_filename = filename
        my_image.image_description = filename
        # my_image.light_source = LightSource.DAYLIGHT

        # print("my_image.has_exif=", my_image.has_exif)
        # print("now my_image has tags:", my_image.list_all())
        # print("my_image.image_description = ", my_image.image_description)
        # print("--")

    with open(filename, "wb") as image_file:
        image_file.write(my_image.get_file())

        # print("reading with exif_read_filename(filename), == ", exif_read_filename(filename))
        #
        # input("added exif data to :: ......")

    return


def file_not_exist(filepath):
    """Check whether a path exists and has content.

    Args:
        filepath (path-like object): filepath

    Returns:
        bool: True if file doesn't exist OR file size is zero otherwise False.

    """
    return not os.path.isfile(filepath) or os.stat(filepath).st_size == 0


def me():
    """returns the name of the function that called me()"""
    return inspect.stack()[1][3] + "()"


def rm_trash_files(src_dir):

    #  print("config.TRASH_FILES==", config.TRASH_FILES)
    #  print(f"rm_trash_files({src_dir}) -->")
    for filename in os.listdir(src_dir):

        # for regex in config.TRASH_FILES:
        #     if re.search(regex, filename, re.IGNORECASE):
        #         print(filename, "--contains somethign--", regex)
        # print("filename=", filename)
        if filename in config.TRASH_FILES:
            print(f"unlinking-> {os.path.join(src_dir, filename)}")
            os.unlink(os.path.join(src_dir, filename))


def test_one_extension(src_dir, fatal=True):
    """make sure the directory only has one extension type otherwise error out

    return: True if there is only one extension in the directorypath
            False if there is more then one extension and fatal is set to False
            ERROR sys.exit(1) if there is more than one extension and fatil is set to True
    """

    if len(ext_list(src_dir)) > 1:
        if fatal:
            log.warning(
                f"ERROR: Directory contains files with more than one extension.\n"
                f" Consider running 'unmix {src_dir}'"
            )
            sys.exit(1)
        return False
    return True


def ext_list(directorypath):
    """returns a list of extensions in the directorypath

    Args:
        filepath (path-like object): directorypath

    Returns:
        nothing
    """

    rm_trash_files(directorypath)

    dirlist = sorted_listdir(directorypath)

    extlist = []

    for item in dirlist:
        ext = os.path.splitext(os.path.split(item)[1])[1]
        if ext not in extlist:
            extlist.append(ext)

    log.debug(f"{utils.__name__} returning {ext_list=}")
    return extlist


def folder_contains_ext(src_dir, search_exts):
    """
    search_exts: is a string or list of strings.
                 ignores case
    Returns: True if any of the files in the folder have one of the search_exts.
    """
    if not isinstance(search_exts, list):
        search_exts = [search_exts]

    actual_exts = ext_list(src_dir)
    log.debug(f"Checking folder_contains ({src_dir}, {search_exts})")
    for ext, raw_ext in product(actual_exts, search_exts):
        if ext == "":
            continue
        log.debug(f"ext={ext}, raw_ext={raw_ext}")
        ext = ext.lstrip(".")
        if re.search(rf"{ext}$", raw_ext, re.IGNORECASE):
            log.debug("folder_contains_ext returning: True")
            return True
    log.debug("folder_contains_ext returning:False")
    return False


recursing = None
really_fullpaths = []


def sorted_listdir(directory, ignore_hidden=True, recursive=False, first_pass=True):
    """returns a list : the full path to every file in a directory sorted alphanumerically.

    Args:
      directory (path-like object): path to a directory
      ignore_hidden (bool): when true do not return hidden files. (default=True)

      first_pass(bool): if True reset the global really_fullpaths[] (default=True)
    Returns:
        list (str): List of filenames in the directory sorted alphanumerically.
    """

    global really_fullpaths
    global recursing

    try:
        names = os.listdir(directory)
    except FileNotFoundError as e:
        if log.level == logging.DEBUG:
            log.exception(f"sorted_listdir() : {e}")
        raise

    if first_pass:
        # print("resetting really_fullpaths")
        really_fullpaths = []

    names.sort()

    fullpaths = []

    for filename in names:
        log.debug("sorted_listdir(): top of outer for: filename= %s", filename)
        fullpath = os.path.join(directory, filename)
        if ignore_hidden and filename.startswith("."):
            continue
        if os.path.isdir(fullpath) == True:
            # print(filename, "sorted_listdir()  is a DIRectory")
            if recursive:
                log.debug("sorted_listdir(): recursive=True")
                really_fullpaths.append(os.path.join(directory, filename))
                fullpaths.append(os.path.join(directory, filename))
                sorted_listdir(
                    os.path.join(directory, filename), recursive=True, first_pass=False
                )
            log.debug("sorted_listdir(): not recursive")
            really_fullpaths.append(os.path.join(directory, filename))
            fullpaths.append(os.path.join(directory, filename))

        else:
            # log.debug("sorted_listdir(): it is NOT a directory")
            really_fullpaths.append(os.path.join(directory, filename))
            fullpaths.append(os.path.join(directory, filename))

    # log.debug(f"sorted_listdir(): returning: {really_fullpaths}")
    # input("done")
    return really_fullpaths


def create_workdir(filename, action="", nested=True):
    """creates and returns the workingdir for a given video file and module
    example
    =======
    nested=TRUE
    filename = /test/out.mp4  action = autotrace
    returns: /test/out/autotrace

    nested=FALSE
    filename = /test/out.mp4  action = autotrace
    returns: /test/out-autotrace


    Args:
        filename (str):
        action (str): The action the directory is needed for. eg 'autotrace'  (Default value = '')

    Returns:
        str : The newly created directory name.
    """

    directory = os.path.split(filename)[0]
    filenameonly = Path(filename).stem

    if nested:
        outdir = directory + "/" + filenameonly + "/" + action
    else:
        outdir = directory + "/" + filenameonly + "-" + action

    try:
        os.makedirs(outdir, exist_ok=True)
    except OSError as error:
        raise OSError(f"ERROR: creating folder {filename} \n {error} ") from error

    return outdir


def open_eps(filename, width=None):
    """takes a filename and returns a scaled PIL Image
        scaling is done AFTER the image has been rasterized
        so this is not really that useful for scaling.
        use resize_eps() to scale eps's without losing quality.

    Args:
        filename (str): eps file.
        width (int): width to scale the eps to. (Default value = None)

    Returns:
        PIL Image object :
    """

    # print("width=", width)
    original = [float(d) for d in Image.open(filename).size]
    # print("original=", original)
    scale = width / original[0]
    # print("scale=", scale)
    img = Image.open(filename)

    # print("new im size = ", img.size)

    if width is not None:
        # print("scaling-loading")
        img.load(scale=math.ceil(scale))
        # print("new im size after scaling = ", img.size)
    if scale != 1:
        # print("scaling-thumbnail")
        img.thumbnail([int(scale * d) for d in original], Image.ANTIALIAS)
        # print("new img_np size after thumbnail = ", img.size)

    # print("sleeping 60...")
    # time.sleep(60)
    return img


def get_eps_size(epsfile):
    """

    Args:
      epsfile:

    Returns:

    """

    width = None
    height = None

    pattern = re.compile(r"%%BoundingBox: (\d*) (\d*) (\d+) (\d+)")

    for _, line in enumerate(open(epsfile, "r")):
        m = re.search(pattern, line)

        if m:
            width = int(m.groups()[2]) - int(m.groups()[0])
            height = int(m.groups()[3]) - int(m.groups()[1])
            break

    log.debug(f"get_eps_size({epsfile}) returning: ({width}x{height})")
    return (width, height)


def common_suffix(xs):
    """Longest suffix shared by all strings in xs."""

    def allSame(cs):
        h = cs[0]
        return all(h == c for c in cs[1:])

    def firstCharPrepended(s, cs):
        return cs[0] + s

    return reduce(
        firstCharPrepended, takewhile(allSame, zip(*(reversed(x) for x in xs))), ""
    )


def split_name_number(name):
    """Splits a given string into name and number. Where number is at the end
    of the string, e.g. 'foo2bar003baz001' will be split into:
    'foo2bar003baz', '001'

    """

    regex = r"^(.*?)(\d*)$"
    m = re.search(regex, name)
    name_part = m.group(1)
    num_part = m.group(2)

    return name_part, num_part


def calculate_scale_factor(orig_tup, new_tup, allow_crop=False):
    """Calculate the scale factor to apply to make one rect fit another rect.
        Will not stretch. Returns a float to be applied to both dimensions.



        allow_crop (boolean) : True = make dimensions fill screen and crop excess
                               False = make dimensions fit within the new box leaving black bars

        returns float : the scale factor.

    Args:
      orig_tup (tuple) : original dimensions (width,height) eg (1920,1080)
      new_tup (tuple) : new dimensions (width,height) eg (3840,2160)
      allow_crop (boolean) : True  = make dimensions fill screen and crop excess
                             False = make dimensions fit within the new box leaving
                                     black bars  (Default value = False)

    Returns:
        float : ration to be applied to make new rectangle fit inside original rectangle

    """

    # +1 so that we are always erring oversize
    x_ratio = round(new_tup[0] / orig_tup[0], 1)
    y_ratio = round(new_tup[1] / orig_tup[1], 1)

    # print("x_ratio=", x_ratio)
    # print("y_ratio=", x_ratio)

    if allow_crop:
        return min(x_ratio, y_ratio)
    return max(x_ratio, y_ratio)


def replace_eps_bounding_box(newx, newy, filepath):
    """replaces this
       - %%BoundingBox: 0 0 3840 2153
       - %%HiResBoundingBox: 0.00 0.00 3840.00 2152.90

       with this
       - %%BoundingBox: 0 0 3840 2160
       - %%HiResBoundingBox: 0.00 0.00 3840.00 2160.00

    Args:
      newx (int):
      newy (int):
      filepath:

    Returns:
        nothing

    """

    bounding_box = "%%BoundingBox:"
    hires_bounding_box = "%%HiResBoundingBox:"
    new_bounding_box = "{} 0 0 {} {}".format(bounding_box, newx, newy)
    new_highres_bounding_box = "{} 0.00 0.00 {:4.2f} {:4.2f}".format(
        bounding_box, newx, newy
    )

    # Safely read the input filename using 'with'
    with open(filepath) as f:
        s = f.read()
        if bounding_box not in s:
            log.debug('"{}" not found in {}.'.format(bounding_box, filepath))
            # return
        if hires_bounding_box not in s:
            log.debug('"{}" not found in {}.'.format(hires_bounding_box, filepath))
            # return

    # Safely write the changed content, if found in the file
    with open(filepath, "w") as f:
        for line in s:
            if bounding_box in line:
                f.write(new_bounding_box)
            elif hires_bounding_box in line:
                f.write(new_highres_bounding_box)
            else:
                f.write(line)


def resize_eps(infile, outfile, newsize=(3840, 2160)):
    """This needs to calculate the right scale based on the size of the input file
        requires ghostscript
        brew install gs

    Args:
      infile:
      outfile:
      newsize:  (Default value = (3840, 2160):

    Returns:

    """

    log.debug(f"resize_eps(infile={infile} outfile={outfile} newsize={newsize}")

    print("orig_sizze=", get_eps_size(infile))
    print("newsize=", newsize)
    scale = calculate_scale_factor(get_eps_size(infile), newsize)
    print("scale=", scale)

    gs_bin = shutil.which("gs")

    if gs_bin is None:
        raise FileNotFoundError(
            "Cannot find binary for ghostscript 'gs' in your $PATH.\n"
        )

    # fmt: off
    sys_call = [
        gs_bin,
        "-q",           # quiet
        "-dBATCH",      # exit after last file
        "-o", outfile,
        "-sDEVICE=eps2write",
        "-dDEVICEWIDTHPOINTS={}".format(newsize[0]),
        "-dDEVICEHEIGHTPOINTS={}".format(newsize[1]),
        "-c", f'"<</Install {{ {scale:4.2f} {scale:4.2f} scale }}>> setpagedevice"',
        "-f",
        infile,
    ]
    # fmt: on

    quoted_sys_call = []
    for item in sys_call:
        quoted_sys_call.append(shlex.quote(item))

    calling_str = "Calling : ", " ".join(quoted_sys_call)
    log.info(calling_str)

    result = run(
        sys_call, stdout=PIPE, stderr=PIPE, universal_newlines=True, check=True
    )
    log.debug(
        "gs returncode={}, stdout={}, stderr={}".format(
            result.returncode, result.stdout, result.stderr
        )
    )

    if result.returncode:
        log.debug("FAILED: {gs_bin}")
        log.debug("returncode = {result.returncode}")
        log.debug("stdout = {result.stderr}")
        log.debug("stderr = {result.stderr}")
        sys.exit(1)

    # If the eps does not fill the box the new box will be smaller then desired
    # even when setting size explicitly
    # This will force the Bounding Box to be full size which will result in a
    # fullsize image once it is rasterized to png etc.

    sys.exit()
