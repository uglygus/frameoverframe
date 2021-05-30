#!/usr/bin/env python3

import rawpy
import imageio
import datetime
from PIL import Image

#  fbdd_noise_reduction=FBDDNoiseReductionMode.Off
path = '/mnt/g/pixelshift tests/16x series/16x-merged-fullsize/DSC04657-DSC04672.dng'

timestamp =  datetime.datetime.now().strftime('%H_%M_%S')

with rawpy.imread(path) as raw:
    rgb = raw.postprocess(use_camera_wb=True,
                          no_auto_bright=True,
                          exp_shift=5.0,
                          exp_preserve_highlights=0.8,
                          fbdd_noise_reduction=rawpy.FBDDNoiseReductionMode.Off,
                          output_bps=16,
                          )
    #gamma=(1,1), no_auto_bright=True, output_bps=16)


imageio.imsave(f'default_{timestamp}.tiff', rgb)

print('type(rgb=)', type(rgb))
new_im = Image.fromarray(rgb)
new_im.save(f'default_pil_{timestamp}.png')
