# frameoverframe

A collection of scripts for working with image sequences, timelapse's or just straight video.


***tracer.py*** vector based tracing of frames

***renumber.py*** - renumber imge sequences in folders

***bracket.py*** - organize images in folders by either splitting or merging folders of hdr images. This moves the actual files it does not creat new ones.

***enfuse_batch.py*** - combine multiple images together to create new ones. Either for hdr images or just to make overlays.

***align\_image\_stack_sequence.py*** - wrapper for align image stack that allows it to be run against a folder of timelapse bracketed images.

***thin.py*** - reduce files from a folder by keeping 1 file and skip a number of files, does not recurse into sum folder.

***deflicker.py*** - adjust brightness of images to reduce flickering.

***img2vid.py*** - combine image frames to create a video.

***vid2img.py*** - extract image frames from a video.

***raw2dng.py*** - convert raw format images to dng format.

***recombine.py*** - recombine a list of directories to be combined and renumbered.

***rename_uniq.py*** - rename individual files so they have a prefix matching the enclosing folder.

***test_image.py*** - test image in every input folder.

***unmix.py*** - rename images with their extensions to separate images that have different formats. 


# tracer.py





# enfuse_batch.py

Run enfuse on a series of images.




###Usage


```
	lnbush -[vhsda] sourcedir targetdir

```

Recursively copies a directory but uses symlinks for all the files. Will create destination dir if it does not exist.

-s    use symbolic links [default]

-d    use hard links

-a    use Mac OSX aliases

-v    verbose

-h    Displays this help message. No further functions are performed.

Example: lnbush -va  ./media/movies ~/Desktop/movies






# bracket.py

Sort HDR bracketed images into seperate directories for each exposure.

eg:

Dir1
--file001.jpg
--file002.jpg
--file003.jpg
--file004.jpg
etc

$ fbracket.py -n 3 ./Dir1

Dir1
--Dir1-exp1
----file001.jpg
----file004.jpg
--Dir1-exp2
----file002.jpg
----file004.jpg
--Dir1-exp3
----file003.jpg
----file005.jpg

###Usage


```
	fbracket.py [-h] -n N dirs


   Given a directory split the files inside into seperate directories.


```


###Options

-r		recurse into directories

-h    Displays this help message.
