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
from frameoverframe.test.utils import dummy_sdcard
from frameoverframe.utils import folder_contains_ext

log = logging.getLogger("frameoverframe")


class TestUtils(unittest.TestCase):
    def setUp(self):
        self.tmpdir_obj = tempfile.TemporaryDirectory(dir=".")
        self.tmpdir = self.tmpdir_obj.name
        self.sdcard = dummy_sdcard(self.tmpdir)

    def tearDown(self):
        self.tmpdir_obj.cleanup()

    def test_folder_contains_SINGLE(self):
        self.assertEqual(folder_contains_ext(self.sdcard, "jpg"), True)

    def test_folder_contains_SINGLE_nomatch(self):
        self.assertEqual(folder_contains_ext(self.sdcard, "XXX"), False)

    def test_folder_contains_LIST(self):
        self.assertEqual(folder_contains_ext(self.sdcard, ["xxx", "arw"]), True)

    def test_folder_contains_LIST_nomatch(self):
        self.assertEqual(folder_contains_ext(self.sdcard, ["xxx", "yyy"]), False)


if __name__ == "__main__":
    unittest.main()
