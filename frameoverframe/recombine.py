#!/usr/bin/env python3
"""
    Recombines folders of images

        accepts a list of directories to be combined and renumbered. Combines files into
        directories with max_files in each directory.

    When sorting by filename it uses the enclosing folder and filename as the key.
    ie: /pth/to/another/file0000.jpg
        /another/pth/to/another/file0000.jpg
        should produce an error because they have the same key:
            another/file0000.jpg

    ie: /pth/to/another/file0000.jpg
        /pth/to/another-1/file0000.jpg
        should sort using the keys:
            /another/file0000.jpg  (pos1)
            /another-1/file0000.jpg (pos2)
"""


import argparse
import logging.config
import math
import os
import pathlib
import re
import shutil
import sys
from pathlib import PurePath
from time import sleep, strftime

from frameoverframe.config import LOGGING_CONFIG

from .renumber import renumber
from .utils import (
    common_suffix,
    rm_trash_files,
    sorted_listdir,
    split_name_number,
    test_one_extension,
)

log = logging.getLogger("frameoverframe")


def strip_bad_ending(string):
    """
    strips off spaces, underscores and dashes from the right of string
    Args:
      string:

    Returns:

    """
    return string.rstrip(" _-")


def parent_and_basename(filepath):
    """returns the parent and basename of a filepath
    ie: /the/path/to/folder/00001.JPG
    returns "folder/00001.JPG"
    """

    path = pathlib.PurePath(filepath)

    # print("filepath=", filepath)
    # print("filepath.parents 1=", str(Path(filepath).resolve().parents[1]))
    # print("filepath.parents 0=", str(Path(filepath).resolve().parents[0]))
    # print("parent0=", str(path.parent.name))
    # print("parent2=", str(Path(filepath).resolve().parent))
    # print("parent3=")
    # print("name=", str(path.name))
    # print("returning=", str(path.parent.name) + "/" + str(path.name))
    # input(".... perent and base ....")
    return str(path.parent.name) + "/" + str(path.name)


def sort_without_suffix_or_fulldir(items):
    """Sort a list after removing the common suffix and parent dirs.

    We need this because:
    ["A-2_ARW", "A_ARW", "A_1_ARW"].sort() produces ["A-1_ARW", "A-2_ARW", "A_ARW"]
    we want: ["A_ARW", "A-1_ARW", "A-2_ARW"]

    ALSO - importantly for my purposes because users make mistakes:
                treat '-'  and '_' interchangeably.
            incase people make:
                infolder
                infolder_1
                infolder-2
                etc
    """
    # print("sort_without_suffix: items=", items)

    working = []
    for i in items:
        working.append({"orig": i, "sortable": os.path.abspath(i)})
    # print("working===", working)
    # input("borken...")
    # print("working['sortable']")
    #    for row in working:
    #        print("row ", row, "sortable=", row["sortable"])
    # print('sortable_list === ', [for i in working[i].['sortable'] ])
    # input("...herre...")

    csuffix = common_suffix([i["sortable"] for i in working])
    suffixlen = -1 * len(csuffix)

    # print(f"{csuffix=}")
    # print(f"{suffixlen=}")

    if csuffix:
        # print(f"{csuffix=}")
        # print(f"{suffixlen=}")

        # print(f"{items[0]=}")
        # print(f"d:1  {items[0][:1]=}")
        # print(f"d:0  {items[0][:0]=}")

        sorted_items = [d[:suffixlen] for d in items]

        # strip everything before the enclosing folder
        for row in working:
            row["sortable"] = parent_and_basename(row["sortable"])
        # print("working after trimming front path==", working)
        # input("...")

        # strip the common suffix
        for row in working:
            row["sortable"] = row["sortable"][:suffixlen]
        # print("working after trimming suffix==", working)
        # input("...")

        # normalize '-_' to hyphens
        for row in working:
            row["sortable"] = row["sortable"].replace("_", "-")
        # print("working after normalizing '-_' ==", working)
        # input("...")

        working = sorted(working, key=lambda i: i["sortable"])
        # print("working was sorted using lambda.")
        # print("working=", working)
        # input("working...")
        sorted_items = [i["orig"] for i in working]
        # print(f"{sorted_items=}")

        # input("done..")
    else:
        # print("NOTHING TO TRIM NO COMMON SUFFIX")
        # print("type(items=", type(items))
        sorted_items = items
        sorted_items.sort()

    # print("orig_items", items)
    # print("sorted_items=", sorted_items)
    # #
    # print("returning working:", working)
    # #
    # input("returning ...")
    return sorted_items


def recombine(
    src_dirs,
    dst_dir=None,
    copy_files=False,
    max_files=10000,
    prefix=":folder",
    padding=5,
):
    """Accepts a list of directories to be combined and renumbered. Combines files into
        directories with max_files in each directory.

    Args:
      src_dirs:
      dst_dir:  (Default value = None)
      copy_files:  (Default value = False)
      max_files:  (Default value = 10000)
      prefix:  (Default value = ':folder')
      padding:  (Default value = 5)

    Returns:
        out_dir (list): List of directories that things were combined into. or None
    """

    if len(src_dirs) < 2:
        return src_dirs

    # removing TRASH files
    log.debug("removing TRASH files")
    for directory in src_dirs:
        rm_trash_files(directory)
    #   input(f"\ndone removing TRASHs. -- {directory}")

    print(f"{src_dirs=}")
    src_dirs = sort_without_suffix_or_fulldir(src_dirs)

    print(f"{src_dirs=}")

    log.info("recombine: Input directories will be processed in this order:")
    for d in src_dirs:
        log.info(d)
    # input("...")

    if dst_dir is None:
        new_basename = split_name_number(os.path.basename(src_dirs[0]))[0]
        # print("new_basename = ", new_basename)
        new_basename = strip_bad_ending(new_basename)
        log.info("new_basename = %s", new_basename)
        dst_dir = os.path.join(os.path.dirname(src_dirs[0]), new_basename)

    if prefix == ":folder":
        prefix = os.path.basename(os.path.normpath(src_dirs[0]))

    item_count = 0
    for directory in src_dirs:
        item_count += len(sorted_listdir(directory))

    dirs_needed = math.ceil(item_count / max_files)

    dst_dirs = []

    # only append a number to destination dirs if there is more than one
    for i in range(0, dirs_needed):
        if dirs_needed > 1:
            dst_dirs.append("{}_{:02d}".format(dst_dir, i))
        else:
            dst_dirs.append(dst_dir)

    # print(f"{dst_dirs=}")
    log.info(
        "Creating {} new directories. For {} items.".format(dirs_needed, item_count)
    )
    log.info("New directories:")
    for d in dst_dirs:
        log.info(d)

    all_files = []

    # input("dirs made...")

    # test all folders to make sure they contain only one extension
    log.info("Checking to make sure there's only one extension")
    for directory in src_dirs:
        test_one_extension(directory, fatal=True)
        log.info("{} ... OK".format(directory))

    for directory in src_dirs:
        log.debug(" Collecting files from: {}".format(directory))
        # print(" for item in :sorted_listdir(directory)==", sorted_listdir(directory))
        for item in sorted_listdir(directory):
            print("directory=", directory, "item=", item)
            if not os.path.isfile(item):
                # print(" not a file: ", os.path.join(directory, item))
                continue
            all_files.append(item)
        # input("... done writing one dir to all_files[]...")

    log.debug("recombine: Done writing all_files[] list:}")
    for f in all_files:
        log.debug(f)
    # input(".. did debug an all files print?")
    tmp_dst_dirs = []

    for dst_dir in dst_dirs:
        if os.path.exists(dst_dir):
            print("WARNING: Output directory already exists.", dst_dir)
            dst_dir = dst_dir + "~recombined_" + strftime("%Y%m%d_%H%M%S")
            print("Renaming output directory to:", dst_dir)
        tmp_dst_dirs.append(dst_dir)
    dst_dirs = tmp_dst_dirs

    log.debug("list of destination direcries made:")
    for d in dst_dirs:
        log.debug(d)

    # input("...desst dir list createed...")
    current_dir = 0
    count = 0
    for item in all_files:
        if count >= max_files:
            count = 0
            current_dir += 1

        dst = dst_dirs[current_dir]

        if not os.path.exists(dst):
            print("os.makedirs( ", dst)
            os.makedirs(dst)

        _, ext = os.path.splitext(item)
        # item_dest = (
        #     dst + "/" + os.path.basename(PurePath(item).parent) + "-" + os.path.basename(item)
        # )

        item_dest = "{}/{:05d}{}".format(dst, count, ext)
        # print("ext=", ext)
        # print("dst=", dst)
        # print("item=", item)
        # print("item_dest= {}".format(item_dest))
        # print("about to moving one...")
        if copy_files:
            log.info("recombine: copying : {} --> {}".format(item, item_dest))
            shutil.copyfile(item, item_dest)
        else:
            log.info("recombine: moving : {} --> {}".format(item, item_dest))
            shutil.move(item, item_dest)
        count += 1

    log.debug("All files moved. Input dirs should be empty if not --safe")
    # input("...")

    if not copy_files:
        for directory in src_dirs:
            shutil.rmtree(directory)

    # input('about to remove timestamps')
    print("about to remove timestamps:  dst_dirs = ", dst_dirs)
    print(f"{dst_dirs=}")

    new_dst_dirs = []
    # remove empty directories
    # remove = 20200810_132823
    # ~recombined_20200810_133221
    # ~recombined_dddddddd_dddddd
    p = re.compile(r"(.+)~recombined_\d\d\d\d\d\d\d\d_\d\d\d\d\d\d")
    for directory in dst_dirs:
        m = p.search(directory)
        if m is None:
            new_dst_dirs.append(directory)
            print("m was None")
            continue
            print("m.group()=", m.group())
            print("m.group=1", m.group(1))
        new_dir = m.group(1)

        if os.path.exists(new_dir):
            print("new_dir exists new_dir=", new_dir)
            new_dir = new_dir + "~recombined_" + strftime("%Y%m%d_%H%M%S")
            print("reset newdir: now  new_dir=", new_dir)

        # under WSL linking to the NAS this fails because the OS still reports the dir as existing
        # if it fails wait a sec and retry...
        # print ('sleep...')
        # sleep(2)

        i = 0
        again = True
        while again:
            try:
                print("shutil.move(", directory, ", ", new_dir)
                shutil.move(directory, new_dir)
                again = False
            except (PermissionError, FileExistsError) as e:
                print("caught error: ", e)
                if i >= 20:
                    print("failed 20 times, exiting.")
                    sys.exit(100)
                print("Permission Error occured retrying in 1s...")
                sleep(1)
                i = i + 1
            print("bottom of WHILE UP UP UP")

        new_dst_dirs.append(new_dir)

    dst_dirs = new_dst_dirs

    print("recombine: about to renumber")
    # renumber new files
    for one_dst_dir in dst_dirs:
        if prefix == ":folder":
            prefix = os.path.basename(os.path.normpath(one_dst_dir))

        # print("middle prefix=", prefix)
        # m = re.match("(.+)(_\d\d)", prefix)
        # if m:
        #     print("prefix=", prefix)
        #     prefix = m[1]
        # else:
        #     print("no match!")
        print("final prefix=", prefix)
        print(" About to renumber --> one_dst_dir=", one_dst_dir)
        # input("...")
        renumber(
            one_dst_dir,
            inplace=True,
            prefix=prefix,
            sort_method="name",
            padding=padding,
        )
        # print("done renumber.")
        # input("...")
    print(f"recombine returning 2 == {dst_dirs=}")

    return dst_dirs


def dir_path(path):
    """for argparse directory type test.

    Args:
      path:

    Returns:

    """
    if os.path.isdir(path):
        return path
    else:
        raise argparse.ArgumentTypeError(f"readable_dir:{path} is not a valid path")
