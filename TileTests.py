import unittest
import Tile

class TestTile(unittest.TestCase):

    def test_print_tile(self):
        newTile = Tile.Tile()
        self.assertRaises(Tile.NotImplementedError, newTile.print_tile)