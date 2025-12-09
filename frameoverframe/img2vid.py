#!/usr/bin/env python3
"""
ffmpeg wrapper
Takes any number of folders of images and conbines them to creates a video.
Rescales videos to be a max width of 1920 but keeps the original aspect ratio.


presets:

preview: (default)
    encoding = h264, fast encode, medium bitrate
    fps = 30
    dimensions = max 1080p if image is over 1080 in one dimension shrink it to fit in a
    1080x1080 box. Does not change images under 1080x1080.

    choices={"tiny","preview", "uhd"}

    Resolution is important!
        VLC cannot play back
            h264 at 9506x6336
            h265 at 9506x6336

best:
    encoding = DNxHR HQ
    fps = 23.976
    dimensions = original

"""

import inspect
import logging
import os
import shlex
import shutil
import subprocess
import sys
import tempfile

from colorama import Fore, Style, init
from PIL import Image, UnidentifiedImageError

from frameoverframe.config import RAW_EXTENSIONS, TRASH_FILES
from frameoverframe.utils import me, sorted_listdir, test_empty_dir, test_one_extension

log = logging.getLogger("frameoverframe")

Image.MAX_IMAGE_PIXELS = 244022272


def img2vid(input_dirs, output_file=None, profile="preview", framenumber=False):
    """convert multiple image_dirs to a single video file"""

    # TODO: this should have a verbose flag and print this...
    # print(f"img2vid: {input_dirs=}, {output_file=}, {profile=}, {framenumber=}")

    init()  # for colorama

    if not isinstance(input_dirs, list):
        input_dirs = [input_dirs]

    input_dirs.sort()

    # if any dir has more than one extension in it ERROR out
    for _dir in input_dirs:
        log.debug(f"{me()} Processing directory: {_dir}")
        if not test_one_extension(_dir, fatal=False):
            log.info(
                f"'{_dir}' -- {Fore.RED}SKIPPING{Style.RESET_ALL} Directory contains more than one extension. "
            )
            return 1

        if test_empty_dir(_dir, fatal=False):
            log.info("Directory is empty {}".format(_dir))
            return 1

        if _dir[0][0] in RAW_EXTENSIONS:
            log.info(
                f"'{_dir}' -- {Fore.RED}SKIPPING{Style.RESET_ALL} Directory contains raw file with extension, {_dir[0][0]} "
            )
            return 1

    if framenumber:
        fnumber_filter = (
            ","
            "drawtext=fontfile=Arial.ttf:"
            "text='%{frame_num}':"
            "start_number=1:"
            "x=w*0.9-tw: y=h*0.85:"
            "fontcolor=white:"
            "fontsize=100:"
            "box=0:"
            "boxcolor=white:"
            "boxborderw=5"
        )
    else:
        fnumber_filter = ""

    print("profile=", profile)
    if profile == "tiny":

        suffix = "_tiny"
        outfile_ext = ".mp4"

        # largest size is 1920x? DOES NOT CROP.
        video_filter = "scale=480:-2" + fnumber_filter

        # fmt: off
        ffmpeg_settings = [
            "-loglevel", "error", '-stats',
        #    "-r", "24000/1001",
            "-r", "30",
            "-n",
            "-vcodec", "libx264",
            "-pix_fmt", "yuv420p",
            "-preset", "fast",
            "-vf", video_filter,
        ]
        # fmt: on

    elif profile == "preview":

        suffix = "_preview"
        outfile_ext = ".mp4"

        # largest size is 1920x? DOES NOT CROP.
        video_filter = "scale=1920:-2" + fnumber_filter

        # fmt: off
        ffmpeg_settings = [
            "-loglevel", "error", '-stats',
        #    "-r", "24000/1001",
            "-r", "30",
            "-n",
            "-vcodec", "libx264",
            "-pix_fmt", "yuv420p",
            "-preset", "fast",
            "-vf", video_filter,
        ]
        # fmt: on

    elif profile == "uhd":

        suffix = "_uhd"
        outfile_ext = ".mp4"

        video_filter = "scale=3840:-2" + fnumber_filter

        # fmt: off
        ffmpeg_settings = [
            #"-r", "24000/1001",
            "-r", "30",
            "-n",
            "-vcodec", "libx264",
            "-crf", "19",
            "-pix_fmt", "yuv422p",
            "-preset", "medium",
            "-vf", video_filter,
        ]

    elif profile == "prores":

        suffix = "_prores"
        outfile_ext = ".mov"

        video_filter = "" + fnumber_filter

        # fmt: off
        ffmpeg_settings = [
            #"-r", "24000/1001",
            "-r", "30",
            "-n",
            "-vcodec", "prores_videotoolbox",
          
            "-profile:v", "hq",  
            "-pixel_format", "yuv422p10lep",
        
           # "-vf", video_filter,
        ]

        # fmt: on

    else:
        log.warning(
            'ERROR: img2vid profile not supported: allowed values are "tiny", "preview", "uhd",supplied: ',
            profile,
        )
        raise ValueError

    if output_file is None:
        out_filepath = os.path.join(
            os.path.dirname(input_dirs[0]),
            os.path.basename(os.path.normpath(input_dirs[0])) + suffix + outfile_ext,
        )
    else:
        out_filepath = output_file

    try:
        log.debug(f"{me()} opening-->{sorted_listdir(input_dirs[0])[0]}")
        im = Image.open(sorted_listdir(input_dirs[0])[0])
    except Image.DecompressionBombError:
        log.warning(
            "Image is too large for PIL to open. "
            " Change this line: PIL.Image.MAX_IMAGE_PIXELS = 244022272 in img2vid.py"
        )
    except UnidentifiedImageError:
        log.warning("Unsupported image file. %s", sorted_listdir(input_dirs[0])[0])
        sys.exit(0)
    except IndexError:
        log.info("")

    width, height = im.size

    # test that all sequences are the same size
    for input_dir in input_dirs:
        im = Image.open(sorted_listdir(input_dir)[0])

        new_width, new_height = im.size
        # print(new_width, "x", new_height, sorted_listdir(input_dir)[0])

        if new_width != width or new_height != height:
            log.warning("ERROR: All images must be the same dimensions.")
            return False

    tmp_link_dir = tempfile.mkdtemp(prefix="img2vid_")
    #print("tmp_link_dir=", tmp_link_dir)
    #input('....')
    ext = os.path.splitext(sorted_listdir(input_dirs[0])[0])[1]

    # images = []
    counter = 0
    for input_dir in input_dirs:
        this_dir_images = sorted_listdir(input_dir)

        for image in this_dir_images:
            if image in TRASH_FILES:
                #    if image.endswith(".DS_Store"):
                continue
            if image.endswith(".CR2"):
                print("ERROR: CR2 is not a recognized image format for ffmpeg.", image)
                sys.exit(1)

            tmp_link = os.path.join(tmp_link_dir, f"{counter:08}{ext}")
            print(f'making link {tmp_link}')
            ret = os.symlink(os.path.abspath(image), os.path.abspath(tmp_link))
            print('ret ==', ret)
            counter += 1
   # input('symlinks made in temp dir...')
    ffmpeg_bin = shutil.which("ffmpeg")

    if ffmpeg_bin:
        sys_call = [
            ffmpeg_bin,
            "-i",
            tmp_link_dir + "/" + "%08d" + ext,
        ]
        sys_call.extend(ffmpeg_settings)
        sys_call.append(out_filepath)

        quoted_sys_call = []
        for item in sys_call:
            quoted_sys_call.append(shlex.quote(item))

        calling_str = "Calling : " + " ".join(quoted_sys_call)
        log.info(f"\n{calling_str}\n")

        subprocess.call(sys_call)

        #shutil.rmtree(tmp_link_dir)
    else:
        log.warning("ERROR: ffmpeg is required and is not intstalled. (this is a log)")
        raise FileNotFoundError(
            "ERROR: ffmpeg is required and is not intstalled. (this is an exception)"
        )
