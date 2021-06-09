#!/usr/bin/env python3

import os
import re
import shutil
import sys
from pathlib import Path
from subprocess import PIPE, run

import exifread
import quotelib


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


def file_not_exist(filepath):
    """Check whether a path exists and has content.

    Args:
        filepath (path-like object): filepath

    Returns:
        bool: True if file doesn't exist OR file size is zero otherwise False.

    """
    return not os.path.isfile(filepath) or os.stat(filepath).st_size == 0


def test_one_extension(src_dir, fatal=True):
    """make sure the directory only has one extension type otherwise error out

    return: True if there is only one extension in the directorypath
            False if there is more then one extension and fatal is set to False
            ERROR sys.exit(1) if there is more than one extension and fatil is set to True
    """

    # print('test_one_extension(): src_dir=',src_dir)

    if len(ext_list(src_dir)) > 1:
        if fatal:
            print(
                "ERROR: Directory contains "
                "files with more than one extension. Consider running 'unmix' ",
                src_dir,
            )
            sys.exit(1)
        else:
            return False
    return True


def ext_list(directorypath):
    """returns a list of extensions in the directorypath

    Args:
        filepath (path-like object): directorypath

    Returns:
        nothing
    """

    dirlist = sorted_listdir(directorypath)

    extlist = []

    for item in dirlist:
        ext = os.path.splitext(os.path.split(item)[1])[1]
        if not ext in extlist:
            extlist.append(ext)

    return extlist


def sorted_listdir(directory, ignore_hidden=True):
    """returns a list : the full path to every file in a directory sorted alphanumerically.

    Args:
      directory (path-like object): path to a directory
      ignore_hidden (bool): when true do not return hidden files. (default=True)

    Returns:
        list (str): List of filenames in the directory sorted alphanumerically.

    """

    names = os.listdir(directory)
    names.sort()
    fullpaths = []

    # print('sorted_listdir directory=', directory)

    for filename in names:
        if ignore_hidden and filename.startswith("."):
            continue
        else:
            fullpaths.append(os.path.join(directory, filename))

    #  print(' sorted_listdir returning fullpaths == ', fullpaths)
    return fullpaths


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

    # print('making outdir - ', outdir)
    try:
        os.makedirs(outdir, exist_ok=True)
    except OSError as e:
        print("ERROR: creating folder {} \n {} ".format(filename, e))
        sys.exit()

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

    print("width=", width)
    original = [float(d) for d in Image.open(filename).size]
    print("original=", original)
    scale = width / original[0]
    print("scale=", scale)
    im = Image.open(filename)

    print("new im size = ", im.size)

    if width is not None:
        print("scaling-loading")
        im.load(scale=math.ceil(scale))
        print("new im size after scaling = ", im.size)
    if scale != 1:
        print("scaling-thumbnail")
        im.thumbnail([int(scale * d) for d in original], Image.ANTIALIAS)
        print("new im size after thumbnail = ", im.size)

    print("sleeping 60...")
    time.sleep(60)
    return im


def get_eps_size(epsfile):
    """

    Args:
      epsfile:

    Returns:

    """

    width = None
    height = None

    pattern = re.compile("%%BoundingBox: (\d*) (\d*) (\d+) (\d+)")

    for i, line in enumerate(open(epsfile, "r")):
        m = re.search(pattern, line)

        if m:
            width = int(m.groups()[2]) - int(m.groups()[0])
            height = int(m.groups()[3]) - int(m.groups()[1])
            break

    # print('get_eps_size({}) returning: ({}x{})'.format(epsfile,width,height))
    return (width, height)


def _split_name_number(name):
    # Splits a given string into name and number where number is the at the end
    # of the string, e.g. 'foo2bar003baz001' will be split into:
    # 'foo2bar003baz', '001'
    #

    regex = "^(.*?)(\d*)$"
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

    print("x_ratio=", x_ratio)
    print("y_ratio=", x_ratio)

    if allow_crop:
        return min(x_ratio, y_ratio)
    else:
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
    new_highres_bounding_box = "{} 0.00 0.00 {:4.2f} {:4.2f}".format(bounding_box, newx, newy)

    # Safely read the input filename using 'with'
    with open(filename) as f:
        s = f.read()
        if bounding_box not in s:
            print('"{}" not found in {}.'.format(bounding_box, filepath))
            # return
        if hires_bounding_box not in s:
            print('"{}" not found in {}.'.format(highres_bounding_box, filepath))
            # return

    # Safely write the changed content, if found in the file
    with open(filename, "w") as f:
        for line in s:
            if bounding_box in line:
                f.write(new_bounding_box)
            elif highres_bounding_box in line:
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

    print("resize_eps(", "infile=", infile, ", outfile=", outfile, ", newsize=", newsize, ")")

    print("orig_sizze=", get_eps_size(infile))
    print("newsize=", newsize)
    scale = calculate_scale_factor(get_eps_size(infile), newsize)
    print("scale=", scale)

    gs_bin = shutil.which("gs")

    if not gs_bin:
        print(f"ERROR: ABORTING:  Cannot find executable 'gs' {gs_bin=}")

        sys.exit(1)

    print(f" ------##---- {gs_bin=}")
    call_list = [
        gs_bin,
        "-q",  # quiet
        "-dBATCH",  # exit after last file
        "-o",
        outfile,  #   quotelib.quote(outfile),
        "-sDEVICE=eps2write",
        "-dDEVICEWIDTHPOINTS={}".format(newsize[0]),
        "-dDEVICEHEIGHTPOINTS={}".format(newsize[1]),
        "-c",
        '"<</Install {{ {:4.2f} {:4.2f} scale }}>> setpagedevice"'.format(scale, scale),
        "-f",
        infile,
    ]

    print("before")
    print("calling : ", " ".join(quotelib.quote(call_list)))
    print("after")

    result = run(call_list, stdout=PIPE, stderr=PIPE, universal_newlines=True)
    print(
        "gs returncode={}, stdout={}, stderr={}".format(
            result.returncode, result.stdout, result.stderr
        )
    )

    if result.returncode:
        print("FAILED: ", gs_bin)
        print("returncode = ", result.returncode)
        print("stdout = ", result.stderr)
        print("stderr = ", result.stderr)
        sys.exit(1)

    # If the eps does not fill the box the new box will be smaller then desired
    # even when setting size explicitly
    # This will force the Bounding Box to be full size which will result in a
    # fullsize image once it is rasterized to png etc.

    sys.exit()
