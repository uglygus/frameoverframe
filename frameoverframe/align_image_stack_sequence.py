#!/usr/bin/env python3
"""
    fof module align_image_stack_sequence




"""

import logging
import os
import shlex
import shutil
import sys
import time
from pathlib import Path
from subprocess import PIPE, run

import multiprocessingsimple
from PIL import Image

log = logging.getLogger("frameoverframe")


def convert_to_png(infile, outfile="", delete_original=True):
    """
    use PIL to convert an image to png and optionally delete original

    input  (str) : image filename
    output (str) : image filename

    """

    if outfile == "":
        infile_dir = os.path.dirname(infile)
        infile_name = os.path.splitext(infile)[0]
        outfile = os.path.join(infile_dir, infile_name + ".png")

    try:
        Image.open(infile).save(outfile)
    except IOError:
        # log.warning("Cannot convert to PNG:", infile)
        raise IOError("Cannot convert to PNG:", infile)

    if delete_original:
        os.unlink(infile)

    return outfile


def align_image_stack(infiles, out_dir="", prefix="aligned-"):
    """
    wrapper for the commandline app align_image_stack by Panotools.
    Tries to be low level and not do too much processing for the
    created files. Annoyingly you cannot control the numbering or
    the output dir. Numbering will be left to another function but
    we will accept an output dir here.

    Takes any number of image files and creates a new TIF file for
    each one. The new files are named "aligned-0000.tif" etc.

    Calls:  align_image_stack -a aligned-  --align-to-first [images]

    infiles (list) : list of strings, paths to image files to stack
    out_dir (string) : directory to output files to (default: current directory)
    prefix (string) : prefix for new aligned images

    returns (list): list of new aligned files
    """

    align_image_stack_bin = shutil.which("align_image_stack")
    if align_image_stack_bin is None:
        raise FileNotFoundError(
            f"Cannot find binary for 'align_image_stack' in your $PATH.\n"
            "It is part of hugin. To install:\n"
            "on MacOS 'brew install hugin' ; export PATH=/Applications/Hugin/tools_mac:$PATH\n"
            "on linux https://ubuntuhandbook.org/index.php/2020/12/install-hugin-2020-ubuntu-20-04/\n"
            "on Windows or others: http://hugin.sourceforge.net/"
        )

    original_cwd = os.getcwd()

    aligned_images = []

    if not out_dir:
        out_dir = os.getcwd()
    else:
        os.chdir(out_dir)

    # fmt: off
    sys_call = [
        align_image_stack_bin,
        "-a", prefix,
        "-g",  str(8), # -g number of grids to search for points default=5 higher is slower.
        "--align-to-first",
    ]
    # fmt: on

    quoted_sys_call = []

    for item in infiles:
        sys_call.append(item)
        quoted_sys_call.append(shlex.quote(item))

    calling_str = "Calling : ", " ".join(quoted_sys_call)
    log.info(calling_str)

    result = run(sys_call, stdout=PIPE, stderr=PIPE, universal_newlines=True, check=False)

    if result.returncode != 0:
        log.warning("align_image_stack FAILED returncode = ", result.returncode)
        log.warning("stdout = ", result.stdout)
        log.warning("stderr = ", result.stderr)
        raise ChildProcessError("Call to 'align_image_stack' failed.")

    for infile in infiles:
        aligned_images.append(os.path.join(out_dir, os.path.basename(infile)))

    log.debug("aligned_images = f{aligned_images}")

    os.chdir(original_cwd)

    return aligned_images


def align_image_stack_sequence(infiles, bracket, out_dir="", prefix="aligned-"):
    """
    given a sequence of images eg IMG_00.jpg - IMG_08.jpg and a bracket of 3
    create a new sequence images in which each bracket (IMG_00.tif-IMG_02.tif etc)
    is aligned with the first image in the bracket.

    This aligns each bracket with itself not every image with the first.

    infiles (list) : list of strings, paths to image files to stack
    bracket (int) : number of images in each bracket
    out_dir (string) : directory to output files to (default: current directory)

    """

    infiles.sort()

    #  aligned_ext = '.tif'  # filetype created by align_image_stack commandline tool
    final_ext = ".png"  # filetype we end up using

    if out_dir == "":
        parent_dir = Path(infiles[0]).absolute().parent

        aligned_dir = str(parent_dir) + "_aligned"

        out_dir = os.path.join(parent_dir, aligned_dir)

    tmp_dir = os.path.join(out_dir, "tmp")

    shutil.rmtree(tmp_dir, ignore_errors=True)
    os.makedirs(tmp_dir)

    bracket_counter = 0
    global_counter = 0
    images = []
    for infile in infiles:
        images.append(infile)

        if bracket_counter >= bracket - 1:

            # test if this stack has already been processed on a previous run.
            already_processed = 0
            for i in range(0, bracket):

                an_orig_filename = os.path.splitext(os.path.basename(infiles[global_counter - i]))[
                    0
                ]

                an_aligned_image_name = an_orig_filename + final_ext
                an_aligned_image_name = os.path.join(out_dir, an_aligned_image_name)

                if os.path.exists(an_aligned_image_name):
                    already_processed += 1

            if already_processed != bracket:

                align_image_stack(images, tmp_dir)

                move_counter = 0

                tmp_dir_list = os.listdir(tmp_dir)

                # convert newly aligned images from .tif to .png to save space (almost 50%)
                png_pool = multiprocessingsimple.MultiprocessingSimple()

                for tif_file in tmp_dir_list:
                    png_pool.add_job(convert_to_png, args=(os.path.join(tmp_dir, tif_file),))

                while png_pool.still_working():
                    time.sleep(1)
                    log.debug("Waiting for png_pool to finish")
                    png_pool.status()

                tmp_dir_list = os.listdir(tmp_dir)
                tmp_dir_list.sort()

                # copy the newly aligned images for this bracket from tmp_dir to out_dir
                working_counter = bracket
                for image in tmp_dir_list:

                    orig_filename = os.path.splitext(
                        os.path.basename(infiles[global_counter - working_counter + 1])
                    )[0]

                    aligned_image_name = orig_filename + final_ext
                    shutil.move(
                        os.path.join(tmp_dir, image), os.path.join(out_dir, aligned_image_name)
                    )
                    move_counter += 1
                    working_counter -= 1

            bracket_counter = 0
            global_counter += 1
            images = []
            continue

        bracket_counter += 1
        global_counter += 1

    shutil.rmtree(tmp_dir)
