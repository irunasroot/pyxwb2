import unittest

from pyxwb2 import XwingDataPack


class TestXwingDataPack(unittest.TestCase):

    def test_load(self):
        self.data_pack = XwingDataPack()
        

if __name__ == "__main__":
    unittest.main()
