#!/usr/bin/env python3
"""
Adobe DNG Converter wrapper

"""

import logging
import os
import platform
import shlex
import shutil
import subprocess

import frameoverframe.utils as utils
from frameoverframe.unmix import unmix

log = logging.getLogger("frameoverframe")


def what_strange_land_is_this():
    if platform.system() == "Darwin":
        return "Darwin"
    if platform.system() == "linux":
        if "Microsoft" in platform.uname().release:
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

    log.info("Calling : " + " ".join(quoted_sys_call))
    winpath = subprocess.check_output(sys_call)
    winpath = winpath.strip()
    return winpath


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

    for _dir in input_dirs:
        for file in utils.sorted_listdir(_dir):
            if what_strange_land_is_this() == "WSL":
                file = WSL_path_converter(file)
            sys_call = [AdobeDNG_bin, "-c", file]

            quoted_sys_call = [shlex.quote(i) for i in sys_call]
            log.info("Calling : " + " ".join(quoted_sys_call))

            result = subprocess.run(sys_call)
            if result.returncode != 0:
                log.debug("Adobe DNG Vonverter failed check your images.")
                return 1
        unmix(_dir)
        return 0
