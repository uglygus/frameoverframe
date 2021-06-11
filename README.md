# frameoverframe

A collection of scripts for working with image sequences, timelapse's or just straight video.


***tracer*** vector based tracing of frames

***renumber*** - renumber imge sequences in folders

***bracket*** - organize images in folders by either splitting or merging folders of hdr images. This moves the actual files it does not creat new ones.

***enfuse_batch*** - combine multiple images together to create new ones. Either for hdr images or just to make overlays.

***align\_image\_stack_sequence*** - wrapper for align image stack that allows it to be run against a folder of timelapse bracketed images.

***thin*** - reduce files from a folder by keeping 1 file and skip a number of files, does not recurse into sum folder.

***deflicker*** - adjust brightness of images to reduce flickering.

***img2vid*** - combine image frames to create a video.

***vid2img*** - extract image frames from a video.

***raw2dng*** - convert raw format images to dng format.

***recombine*** - recombine a list of directories to be combined and renumbered.

***rename_uniq*** - rename individual files so they have a prefix matching the enclosing folder.

***test_image*** - test image in every input folder.

***unmix*** - rename images with their extensions to separate images that have different formats.



[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
