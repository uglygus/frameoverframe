#!/usr/bin/env python3
"""
    test_image

    Tests files one by one from many directories. Reports bad images to stdout.

"""

import argparse
import logging

# import logging
import logging.config

from frameoverframe.logging_my_config import DEFAULT_LOGGING
from frameoverframe.test_images import test_images


def collect_args():
    """collect commandline arguments"""

    parser = argparse.ArgumentParser(
        description="Takes one or more folders of images and tests each image "
        "using ffmpeg's identify. Reports bad images to stdout."
    )

    parser.add_argument("input_dirs", nargs="+", help="directory(s) of images...")
    parser.add_argument("--verbose", "-v", action="store_true", help="increase output verbosity")
    parser.add_argument("--debug", action="store_true", help="print debug messages")

    #   parser.add_argument( "-r", "--recursive", action="store_true", default=False,
    #       help="Descend into sub directories?. (default False)",
    #   )

    return parser


def main():
    """commandline setup"""

    # logging.info("Hello, log called from __main__")
    # log.info("called LOG from __main__")
    #

    print("DEFAULT_LOGGING=", DEFAULT_LOGGING)

    logging.config.dictConfig(DEFAULT_LOGGING)
    log = logging.getLogger("frameoverframe")

    log.debug("DEBUG message in CLI__MAIN__")
    log.info("INFO message in CLI__MAIN__")
    log.warn("WARN message in CLI__MAIN__")
    log.warn("CRITICAL message in CLI__MAIN__")

    print("log_name=", log.name, "log_parent=", log.parent, "log_level=", log.level)
    print("setting level to DEBUG")
    log.setLevel(logging.DEBUG)
    print("log_name=", log.name, "log_parent=", log.parent, "log_level=", log.level)

    log.debug("DEBUG message in CLI__MAIN__")
    log.info("INFO message in CLI__MAIN__")
    log.warn("WARN message in CLI__MAIN__")
    log.warn("CRITICAL message in CLI__MAIN__")

    parser = collect_args()
    args = parser.parse_args()

    # if args.verbose:
    #     logging.getLogger("frameoverframe.test_images").setLevel(logging.INFO)
    #
    # if args.debug:
    #     logging.getLogger("frameoverframe.test_images").setLevel(logging.DEBUG)

    # test_images(args.input_dirs)  # , args.recursive)


if __name__ == "__main__":
    main()
