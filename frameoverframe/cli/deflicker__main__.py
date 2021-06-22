#!/usr/bin/env python3
"""
A small tool for deflickering images for time lapse videos.
The brightness of the images are adjusted to a rolling mean above <N> images
For the calculation of the image brightness, outliers are discarded via
sigma clipping if the --sigma option is given

Usage:
    timelapse-deflicker.py <inputdir> [options]

Options:
    -o <dir>, --outdir=<dir>  Output directory [default: INPATH/INFOLDERNAME_deflickered]
    -w <N>, --window=<N>      Window size for rolling mean [default: 10]
    -q, --quiet               Only output errors and warnings
    -f <fmt>, --format=<fmt>  Output format for the scaled images [default: png]
    -s <s>, --sigma=<s>       Sigma for the sigma clipping


    forked from timelapse-deflicker by Maximilian Nöthe
    https://github.com/MaxNoe/timelapse-deflicker
"""

import logging
import os
import sys

from docopt import DocoptExit, docopt
from schema import And, Or, Schema, SchemaError, Use

from frameoverframe.deflicker import deflicker, find_images
from frameoverframe.utils import create_workdir


def mkdir_p(directory):
    """create directory without complaining if it already exists."""
    logger = logging.getLogger()
    if not os.path.exists(directory):
        logger.info("Created directory: {}".format(directory))
        os.makedirs(directory)
    return directory


formats = ["png", "tiff", "tif", "jpg", "jpeg"]

args_schema = Schema(
    {
        "<inputdir>": Schema(os.path.exists, "<inputdir> does not exist"),
        "--window": And(Use(int), lambda x: x > 0, error="--window has to be a positive integer"),
        "--format": Or(*formats, error="Unsupported format"),
        "--sigma": Or(
            None,
            And(Use(float), lambda x: x > 0, error="--sigma must be positive"),
        ),
        "--outdir": Use(mkdir_p),
        "--quiet": bool,
    }
)


def main():
    """
    deflicker: commandline app
    """
    try:
        args = docopt(
            __doc__,
        )  # version=deflicker.__version__)
        args = args_schema.validate(args)

        print("args==", args)

        logging.basicConfig(
            level=logging.WARNING if args["--quiet"] else logging.INFO,
            format="%(asctime)s - %(levelname)s | %(message)s",
            datefmt="%H:%M:%S",
        )
        logger = logging.getLogger()
        logger.info("This is deflicker")

        images = find_images(args["<inputdir>"])
        if not images:
            logger.error('No images found in "{}"'.format(args["<inputdir>"]))
            sys.exit(1)

        if args["--outdir"] == "INPATH/INFOLDERNAME_deflickered":

            args["--outdir"] = create_workdir(args["<inputdir>"], "deflickered", nested=False)

        print("args==", args)

        try:
            deflicker(
                images,
                args["--window"],
                args["--outdir"],
                fmt=args["--format"],
                sigma=args["--sigma"],
            )
        except ValueError as e:
            print(e)
            return 1
        except OSError as e:
            print("OSError =", e)
            return 1

    except DocoptExit as e:
        print(e)
    except SchemaError as e:
        print(e)
    except (KeyboardInterrupt, SystemExit):
        pass


if __name__ == "__main__":
    sys.exit(main())
