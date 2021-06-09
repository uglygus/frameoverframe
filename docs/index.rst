.. frameoverframe documentation master file, created by
   sphinx-quickstart on Tue Aug  4 22:45:05 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

frameoverframe
==========================================

frameoverframe
A collection of scripts for working with image sequences, timelapse's or just straight video.

tracer.py vector based tracing of frames

renumber.py - renumber imge sequences in folders

bracket.py - organize images in folders by either splitting or merging folders of hdr images. This moves the actual files it does not creat new ones.

enfuse_batch.py - combine multiple images together to create new ones. Either for hdr images or just to make overlays.

align_image_stack_sequence.py - wrapper for align image stack that allows it to be run against a folder of timelapse bracketed images.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   cli_bracket
   cli_align_image_stack
   cli_img2vid
   cli_enfuse_batch
   cli_recombine
   cli_rename_uniq
   cli_renumber
   cli_tracer
   cli_test_images
   modules








:automodule:

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
