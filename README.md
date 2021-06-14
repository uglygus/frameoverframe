


[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)

# frameoverframe

A collection of scripts for organizing, converting and manipulating image sequences. This has been written to solve my personal workflow needs but I will gladly accept issues and pull requests.


### Organization scripts


***bracket*** - Organize images in folders by either splitting or merging folders of images shot as brackets in camera. This moves the actual files it does not create new ones.

***renumber*** - Renumber image sequences.

***rename_uniq*** - Rename individual files so they have a prefix matching the enclosing folder.

***thin*** - Reduce files from a folder by keeping 1 file and skip a number of files, does not recurse into sum folder.

***unmix*** - Rename images with their extensions to separate images that have different
formats.

***test_image*** - Test image in every input folder.


### File format conversion scripts

***img2vid*** - Combine image frames to create a video.

***raw2dng*** - Convert raw format images to dng format.

***vid2img*** - Convert a video to an image sequence.


### Image manipulation scripts

***align\_image\_stack_sequence*** - Wrapper for align\_image\_stack that allows it to be run against a folder of bracketed images.

***deflicker*** - Adjust brightness of images to reduce flickering.

***enfuse_batch*** - Combine multiple images together to create new ones. Either for hdr images or just to make overlays.

***recombine*** - Recombine a list of directories to be combined and renumbered.

***tracer*** Vector based tracing of frames.

