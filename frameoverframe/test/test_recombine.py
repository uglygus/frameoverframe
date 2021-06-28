# to run all tests:
# $ cd frameoverframe/
# $ python3 -m unittest
#

import logging.config
import os
import os.path
import sys
import tempfile
import unittest
from pathlib import Path

#   logging.config.dictConfig() and logging.getLogger()
#   must come after importing LOGGING_CONFIG
#   but before any other frameoverframe modules.
from frameoverframe.config import LOGGING_CONFIG

logging.config.dictConfig(LOGGING_CONFIG)
log = logging.getLogger("frameoverframe")


from frameoverframe.recombine import parent_and_basename, recombine, sort_without_suffix_or_fulldir
from frameoverframe.test.utils import IM_COLORS, dummy_sdcard, file_count, lots_o_images
from frameoverframe.utils import read_exif_filename, sorted_listdir

log.setLevel(logging.DEBUG)
log.debug("debug loggging is working in test_recombine")
log.info("info loggging is working in test_recombine")
log.warn("warn loggging is working in test_recombine")


class TestRecombine(unittest.TestCase):
    def setUp(self):
        self.tmpdir_obj = tempfile.TemporaryDirectory(dir=".")
        self.tmpdir = self.tmpdir_obj.name
        # self.sdcard = dummy_sdcard(self.tmpdir)

    def tearDown(self):
        self.tmpdir_obj.cleanup()

    def test_sort_without_suffix_or_fulldir(self):
        """sort but ignore suffix usually _ARW or _JPG

        ALSO - importantly for my purposes because users make mistakes:
            treat '-'  and '_' interchangeably.

        """

        orig_list = [
            "/mnt/d/timelapse2021/butterflies_2_JPG/",
            "/mnt/c/timelapse2021/butterflies_JPG/",
            "/mnt/c/timelapse2021/butterflies-1_JPG/",
            "another_path/timelapse2021/butterflies-3_JPG/",
        ]

        expected_list = [
            "/mnt/c/timelapse2021/butterflies_JPG/",
            "/mnt/c/timelapse2021/butterflies-1_JPG/",
            "/mnt/d/timelapse2021/butterflies_2_JPG/",
            "another_path/timelapse2021/butterflies-3_JPG/",
        ]

        sorted_list = sort_without_suffix_or_fulldir(orig_list)

        # print(f"{orig_list=}")
        # print(f"{sorted_list=}")
        # print(f"{expected_list=}")
        # input("...a sorting...")

        self.assertEqual(sorted_list == expected_list, True)

    def test_recombine_two_dirs(self):
        """test to make sure two dirs are recombined correctly."""

        print("self.tmpdir=", self.tmpdir)

        print("new dir called=-", os.path.join(self.tmpdir, "DIR_1"))

        dir1 = os.path.join(self.tmpdir, "2020-06-21 DIR_1")

        # os.makedirs(o, exist_ok=True)
        dir2 = os.path.join(self.tmpdir, "2020-06-21 DIR_2")
        final_dir = os.path.join(self.tmpdir, "2020-06-21 DIR_2")

        print("dir1=", dir1)
        os.makedirs(dir1, exist_ok=True)
        os.makedirs(dir2, exist_ok=True)

        print("string dir1=", dir1)
        # input("...check tmp dir for match")
        lots_o_images(dir1, color=IM_COLORS[0], count=5, prefix="2021-09-09 raccoon ")

        lots_o_images(dir2, color=IM_COLORS[1], count=5, prefix="2021-09-09 raccoon ")

        # print("dir fof=", dir(fof))

        new_dirs = recombine([dir1, dir2])

        for d in new_dirs:
            for f in sorted_listdir(d):
                print("checking file f=", f)
                # input("reading exif...")
                dirx, filx = os.path.split(read_exif_filename(f))
                orig_id = os.path.basename(dirx) + filx
                new_id = os.path.basename(d) + f

                print("original_filename (orig_id)", orig_id)
                print("new=", f, "original=", orig_id)
                # input("done one file comparison....")
        input("..done recombine..check file colors..")

        self.assertEqual(True, True)

    # def test_recombine_one_existing_and_two_new_dirs(self):
    #     """Adding two new directories to a pre-existing dir."""
    #
    #     print("Adding two new directories to a pre-existing dir.")
    #     print("self.tmpdir=", self.tmpdir)
    #
    #     prefix = "2021-06-23 butterflies"
    #
    #     pre_existing_dir = os.path.join(self.tmpdir, prefix + "_1")
    #
    #     print("pre-existing dir", pre_existing_dir)
    #
    #     dir1 = os.path.join(self.tmpdir, "2021-06-23 butterflies-1")
    #
    #     #### only got to here...
    #
    #     # os.makedirs(o, exist_ok=True)
    #     dir2 = os.path.join(self.tmpdir, "2021-06-23 butterflies-2")
    #     # final_dir = os.path.join(self.tmpdir, "2020-06-21 DIR_2")
    #
    #     print("dir1=", dir1)
    #     os.makedirs(dir1, exist_ok=True)
    #     os.makedirs(dir2, exist_ok=True)
    #
    #     print("string dir1=", dir1)
    #     lots_o_images(
    #         pre_existing_dir, color=IM_COLORS[0], count=23, prefix="2021-06-23 butterflies"
    #     )
    #
    #     # input("...check tmp dir for match")
    #     lots_o_images(dir1, color=IM_COLORS[0], count=5, prefix="2021-09-09 raccoon ")
    #
    #     lots_o_images(dir2, color=IM_COLORS[1], count=11, prefix="2021-09-09 raccoon ")
    #
    #     # print("dir fof=", dir(fof))
    #
    #     recombine([dir1, dir2])
    #
    #     input("..done recombine....")
    #
    #     self.assertEqual(True, True)


if __name__ == "__main__":
    unittest.main()
