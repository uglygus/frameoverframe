# to run all tests:
# $ cd frameoverframe/frameoverframe/tests, the inner one that has this test file>
# $ python -m unittest
#


import os
import os.path
import tempfile
import unittest
from pathlib import Path

import frameoverframe as fof


def file_count(dirname):
    return sum([len(files) for r, d, files in os.walk(dirname)])


def dummy_sdcard(dirname):

    sdcard = os.path.join(dirname, "SDCARD")
    os.makedirs(sdcard)
    print("sdcard=", sdcard)

    lots_o_files(sdcard, prefix="DSC", ext="JPG")
    lots_o_files(sdcard, prefix="DSC", ext="ARW")

    print("Done makeing dir ", sdcard, "and populating it.")

    return sdcard


def lots_o_files(dirname, count=1000, prefix="", ext=""):

    for i in range(0, count):
        filename = f"{dirname}/{prefix}{i:05}.{ext}"
        Path(filename).touch()


class testUnmix(unittest.TestCase):
    def test_unmix_count_same(self):
        tmpdir = tempfile.TemporaryDirectory(dir=".")
        sdcard = dummy_sdcard(tmpdir.name)

        original_count = file_count(tmpdir.name)

        fof.unmix.unmix(sdcard)

        final_count = file_count(tmpdir.name)

        self.assertEqual(original_count == final_count, True)


if __name__ == "__main__":
    unittest.main()
