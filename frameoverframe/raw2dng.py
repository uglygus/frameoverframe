#!/usr/bin/env python3
"""
Adobe DNG Converter wrapper

"""

import logging
import os
import platform
import re
import shlex
import shutil
import subprocess
from pathlib import Path

import frameoverframe.config as config
import frameoverframe.utils as utils
from frameoverframe.unmix import unmix

log = logging.getLogger("frameoverframe")


def what_strange_land_is_this():
    if platform.system() == "Darwin":
        return "Darwin"
    if platform.system() == "linux" or platform.system() == "Linux":
        if "Microsoft" in platform.uname().release or "microsoft" in platform.uname().release:
            log.debug("under WSL")
            return "WSL"
        else:
            return "Linux"
    raise FileNotFoundError(
        "Unknown system -- I should work under WSL and on Mac.\n" "Windows has not been tested.",
    )
    return None


def WSL_path_converter(path):
    """Converts a path from linux to Windows format
    Uses Microsoft's 'wslpath' command.
    """

    wslpath_bin = shutil.which("wslpath")

    sys_call = [wslpath_bin, "-w", path]

    quoted_sys_call = [shlex.quote(i) for i in sys_call]
    i_had_to_touch_path_because_wsl_sucks = False

    if not os.path.exists(path):
        # https://github.com/microsoft/WSL/issues/4908
        log.debug(
            "WSL_path_converter() path does not exist. touching file to get it. because wslpath sucks."
        )
        i_had_to_touch_path_because_wsl_sucks = True
        Path(path).touch()

    i_had_to_touch_path_because_wsl_sucks = False

    if not os.path.exists(path):
        # https://github.com/microsoft/WSL/issues/4908
        log.debug(
            "WSL_path_converter() path does not exist. touching file to get it. because wslpath sucks."
        )
        i_had_to_touch_path_because_wsl_sucks = True
        Path(path).touch()

    log.info("Calling : " + " ".join(quoted_sys_call))
    winpath = subprocess.check_output(sys_call)

    if i_had_to_touch_path_because_wsl_sucks:
        os.unlink(path)

    winpath = winpath.strip()

    return winpath.decode("utf-8")


def raw2dng(input_dirs, output_dir):
    """convert RAW to DNG"""

    log.debug("Top of raw2dng() input_dirs={} output_dir={}".format(input_dirs, output_dir))

    # add possible locations for Adobe DNG Converter to the PATH
    os.environ["PATH"] = (
        os.environ["PATH"]
        + ":/mnt/c/Program Files/Adobe/Adobe DNG Converter:"
        + ":/Applications/Adobe DNG Converter.app/Contents/MacOS:"
    )

    AdobeDNG_bin = (
        shutil.which("Adobe DNG Converter") or shutil.which("Adobe DNG Converter.exe") or None
    )

    if AdobeDNG_bin is None:
        log.debug("ERROR: Adobe DNG Converter is required and is not in the PATH. ")
        raise FileNotFoundError("Adobe DNG Converter[.exe] not found.")

    if not isinstance(input_dirs, list):
        input_dirs = [input_dirs]

    input_dirs.sort()

    first_file = os.listdir(input_dirs[0])[0]
    first_ext = os.path.splitext(first_file)[1]

    print("first_file=", first_file)
    print("first_ext=", first_ext)
    #    input("....")
    for _dir in input_dirs:
        log.debug("_dir=={}".format(_dir))
        for raw_ext in config.RAW_EXTENSIONS:
            raw_ext.replace(".", "_")
            outpur_dir = _dir.replace(raw_ext, first_ext)
        log.debug("output_dir={}".format(output_dir))

        for file in utils.sorted_listdir(_dir):

            _, ext = os.path.splitext(file)

            if not ext.upper() in config.RAW_EXTENSIONS:
                log.debug("skipping. File doesn't have a RAW extension.")
                continue

            if ext.casefold() == ".dng".casefold():
                log.debug("skipping. File is already a DNG.")
                continue

            log.debug("file={}, ext={}".format(file, ext))
            output_file = re.sub(ext, ".dng", file, flags=re.I)
            log.debug("look for output_file={}".format(output_file))

            if os.path.isfile(output_file):
                log.info("{} already exists".format(output_file))
                continue

            if what_strange_land_is_this() == "WSL":
                file = WSL_path_converter(file)

            sys_call = [AdobeDNG_bin, "-c", "-p2", file]

            quoted_sys_call = [shlex.quote(i) for i in sys_call]
            log.info("\nCalling : " + " ".join(quoted_sys_call))

            result = subprocess.run(sys_call)
            if result.returncode != 0:
                log.debug("Adobe DNG Converter failed check your images.")
                return 1
            # input("...")
        unmix(_dir)
        return 0
