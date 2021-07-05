# to run all tests:
# $ cd frameoverframe/
# $ python3 -m unittest
#


import logging
import os
import os.path
import sys
import tempfile
import unittest
from pathlib import Path

import frameoverframe as fof

# from frameoverframe.test.utils import dir_count, dummy_sdcard, file_count, lots_o_files

log = logging.getLogger("frameoverframe")


class TestUtils(unittest.TestCase):
    def setUp(self):
        self.tmpdir_obj = tempfile.TemporaryDirectory(dir=".")
        self.tmpdir = self.tmpdir_obj.name
        self.sdcard = dummy_sdcard(self.tmpdir)

    def tearDown(self):
        self.tmpdir_obj.cleanup()

    def test_folder_contains_SINGLE(self):
        """test to make sure folder_contains()
        works with a single input.
        """
        self.assertEqual(utils.folder_contains(self.sdcard, "jpg"), True)

    def test_unmix_dircount_is_two(self):
        """test to make sure the number of files is the same
        before and after unmixing.
        """

        # original_count = file_count(self.tmpdir)

        fof.unmix.unmix(self.sdcard)

        # final_count = count(self.tmpdir)
        #
        # print(f"{original_count=}")
        # print(f"{final_count=}")

        self.assertEqual(dir_count(self.tmpdir), 2)


if __name__ == "__main__":
    unittest.main()
