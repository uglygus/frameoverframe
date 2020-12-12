#!/usr/bin/env python3
'''
ffmpeg wrapper
Takes any number of folders of images and conbines them to creates a video.
Rescales videos to be a max width of 1920 but keeps the original aspect ratio.


presets:

preview: (default)
    encoding = h264, fast encode, medium bitrate
    fps = 23.976
    dimensions = max 1080p if image is over 1080 in one dimension shrink it to fit in a
    1080x1080 box. Does not change images under 1080x1080.

best:
    encoding = DNxHR HQ
    fps = 23.976
    dimensions = original

'''

import subprocess
import os
import shutil
import sys
from PIL import Image
import tempfile

from quotelib import quote

from frameoverframe.utils import sorted_listdir, test_one_extension
import  frameoverframe.utils as utils

def img2vid(input_dirs, output_file, profile='preview'):
    ''' convert multiple image_dirs to a single video file '''


    print(' top of img2vid input_dirs=',input_dirs)

    if not isinstance(input_dirs,list):
        input_dirs = [input_dirs]

    input_dirs.sort()

    # if any dir has more than one extension in it ERROR out
    for _dir in input_dirs:
        if not test_one_extension(_dir, fatal=False):
            print ('SKIPPING: Directory contails more than one extension. ', _dir)
            return

#     profileff=''

    if profile == 'preview':

        suffix = '_preview'
        outfile_ext = '.mp4'

        ffmpeg_settings = [
                '-r', "24000/1001",
                '-vcodec', 'libx264',
                '-pix_fmt', 'yuv420p',
                '-preset', 'veryfast',
                '-vf', 'scale=1920:-1',  # largest size is 1920x? DOES NOT CROP
            ]

    elif profile == 'best_h264':

        suffix = '_best_h264'
        outfile_ext = '.mp4'

        ffmpeg_settings = [
            '-r', "24000/1001",
            '-vcodec', 'libx264',
            '-crf', "17",
            '-pix_fmt', 'yuv422p',
            '-preset', 'veryslow',
            '-vf', "scale=3840:2160:force_original_aspect_ratio=increase,crop=3840:2160",  # fit in UHD4k and crop as needed
           # '-vf', "scale=3840:2160:force_original_aspect_ratio=decrease,pad=3840:2160:-1:-1:color=black",  # fit in UHD4k and pad
        ]

    elif profile == 'best_mxf':

        suffix = '_best_mxf_sq'
        outfile_ext = '.mxf'

        ffmpeg_settings = [
            '-r', "24000/1001",
            '-vcodec', 'dnxhd',
            '-profile:v', "dnxhr_sq",
            '-pix_fmt', 'yuv422p',
            '-vf', "scale=3840:2160:force_original_aspect_ratio=increase,crop=3840:2160",  # fit in UHD4k and crop as needed
           # '-vf', "scale=3840:2160:force_original_aspect_ratio=decrease,pad=3840:2160:-1:-1:color=black",  # fit in UHD4k and pad
        ]

    else:
        print('ERRROR: img2vid profile not supported: allowed values are "preview", "best" supplied: ', profile)
        raise

    if output_file is None:
        print('setting output_filepath')
        out_filepath = os.path.join( os.path.dirname(input_dirs[0]),
                       os.path.basename(os.path.normpath(input_dirs[0])) + suffix + outfile_ext )
    else:
        print('NOT setting output_filepath')
        out_filepath = output_file

    im = Image.open(sorted_listdir(input_dirs[0])[0])
    width, height = im.size

    # test that all sequences are the same size
    for input_dir in input_dirs:
        im = Image.open(sorted_listdir(input_dir)[0])

        new_width, new_height = im.size
        print(new_width, 'x', new_height, sorted_listdir(input_dir)[0])

        if new_width != width or new_height != height:
            print('ERROR: All images must be the same dimensions.')
            return False

    tmp_link_dir = tempfile.mkdtemp(prefix='img2vid_')
    print('tmp_link_dir=', tmp_link_dir)

    ext = os.path.splitext(sorted_listdir(input_dirs[0])[0])[1]

    images = []
    counter = 0
    for input_dir in input_dirs:
        this_dir_images = sorted_listdir(input_dir)

        for image in this_dir_images:
            if image.endswith('.DS_Store'):
                continue
            if image.endswith('.CR2'):
                print('ERROR: CR2 is not a recognized image format for ffmeg.', image)
                sys.exit(1)

           # print('making link: {} --> {}'.format(image, os.path.join(tmp_link_dir, '{:08}{}'.format(counter, ext))))
            os.symlink(image, os.path.join(tmp_link_dir, '{:08}{}'.format(counter, ext)))
            counter += 1

    ffmpeg_bin = shutil.which('ffmpeg')

    if ffmpeg_bin:
        sys_call = [ffmpeg_bin,
                    '-i', tmp_link_dir + '/' + '%08d' + ext,
                    ]
        sys_call.extend(ffmpeg_settings)
        sys_call.append(out_filepath)

        print('\ncalling : ', ' '.join(quote(sys_call)), '\n')
        subprocess.call(sys_call)

     #   shutil.rmtree(tmp_link_dir)
    else:
        print('ERROR: ffmpeg is required and is not intstalled. ')
        sys.exit(1)
