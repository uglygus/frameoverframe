# to run all tests:
# $ cd frameoverframe/
# $ python3 -m unittest
#

import logging.config
import os
import os.path
import re
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
from frameoverframe.utils import exif_read_filename, recursing, sorted_listdir

log.setLevel(logging.DEBUG)
log.debug("debug loggging is working in test_recombine")
log.info("info loggging is working in test_recombine")
log.warning("warn loggging is working in test_recombine")


#
# def recursive_listdir(start_dir):
#     full_list = []
#     for root, dirs, files in os.walk(start_dir):
#         path = root.split(os.sep)
#         full_list.append((len(path) - 1) * "---" + os.path.basename(root))
#         # print((len(path) - 1) * "---", os.path.basename(root))
#         for file in files:
#             full_list.append(len(path) * "---" + file)
#         #    print(len(path) * "---", file)
#
#     input("... recursive--")
#     print("full_list=", full_list)
#     return full_list


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

        self.assertEqual(sorted_list == expected_list, True)

    def test_recombine_three_dirs(self):
        """test to make sure three dirs are recombined correctly."""

        print("self.tmpdir=", self.tmpdir)
        dir1 = os.path.join(self.tmpdir, "2020-06-21 Raccoon_00")

        dir2 = os.path.join(self.tmpdir, "2020-06-21 Raccoon-2")
        dir3 = os.path.join(self.tmpdir, "2020-06-21 Raccoon 3")

        # final_dir = os.path.join(self.tmpdir, "2020-06-21 DIR_2")

        print("dir1=", dir1)
        os.makedirs(dir1)
        os.makedirs(dir2)
        os.makedirs(dir3)

        print("string dir1=", dir1)
        # input("...check tmp dir for match")
        lots_o_images(dir1, color=IM_COLORS[0], count=2, prefix="2021-09-09 raccoon ")

        lots_o_images(dir2, color=IM_COLORS[1], count=3, prefix="2021-09-09 raccoon ")

        lots_o_images(dir3, color=IM_COLORS[2], count=3, prefix="2021-09-09 raccoon ")

        new_dirs = recombine([dir1, dir2, dir3], max_files=3)

        print("new_dirs=", new_dirs)
        # input("new dirs...")
        for d in new_dirs:
            for f in sorted_listdir(d):
                print("checking file f=", f)
                # input("reading exif...")
                dirx, filx = os.path.split(exif_read_filename(f))
                orig_id = os.path.basename(dirx) + filx
                new_id = os.path.basename(d) + f

                print("original_filename (orig_id)", orig_id)
                print("new=", f, "original=", orig_id)
                # input("done one file comparison....")

        expected_filelist = []
        final_filelist = []
        print("\n--- actual files just created list -----")
        for d in new_dirs:
            for f in sorted_listdir(d):
                print(exif_read_filename(f), " ==> ", f)
                final_filelist.append(exif_read_filename(f))

        # input(" wh not stop...")
        # print(f"{expected_filelist=}")
        # print("--- final list - red from files exifname-----")
        # for item in final_filelist:
        #     print(exif_read_filename(item))

        # input("..done recombine..check file colors..")

        print("-------------------last_sorted_listdir------")
        recursing = True
        # really_fullpaths = []
        interim_layout = sorted_listdir(self.tmpdir, recursive=True)
        recursing = False

        print("\ninterim_layout=", interim_layout)
        for i in interim_layout:
            print(i)

        print("trim off the temp dirs")

        ## trim the temp dir off of final layout
        final_layout = []
        for i in interim_layout:
            m = re.match("(\./tmp\w+)(.*)", i)
            if m:
                print("m[1]=", m[2])
                final_layout.append(m[2])
                m = None
            else:
                print("no match!!! ++++")

        expected_layout = [
            "/2020-06-21 Raccoon_00",
            "/2020-06-21 Raccoon_00/2020-06-21 Raccoon_00_00000.JPG",
            "/2020-06-21 Raccoon_00/2020-06-21 Raccoon_00_00001.JPG",
            "/2020-06-21 Raccoon_00/2020-06-21 Raccoon_00_00002.JPG",
            "/2020-06-21 Raccoon_01",
            "/2020-06-21 Raccoon_01/2020-06-21 Raccoon_00_00000.JPG",
            "/2020-06-21 Raccoon_01/2020-06-21 Raccoon_00_00001.JPG",
            "/2020-06-21 Raccoon_01/2020-06-21 Raccoon_00_00002.JPG",
            "/2020-06-21 Raccoon_02",
            "/2020-06-21 Raccoon_02/2020-06-21 Raccoon_00_00000.JPG",
            "/2020-06-21 Raccoon_02/2020-06-21 Raccoon_00_00001.JPG",
        ]

        for i in interim_layout:
            print("interim   ", i)
        for i in final_layout:
            print("final     ", i)
        for i in expected_layout:
            print("expected  ", i)
        # print("final_layout==", final_layout)
        # print("expected_layout==", expected_layout)

        self.assertEqual(final_layout == expected_layout, True)


if __name__ == "__main__":
    unittest.main()
