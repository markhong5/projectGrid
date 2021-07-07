import Item
import unittest
class TestTile(unittest.TestCase):

    def test_types_Of_Items(self):

        coinItem = Item.Item("C", "5coin", 5, "C")
        coinTile = "5-C"
        self.assertEqual(coinItem.print_tile(), f"{coinTile:<10}")

        potionItem = Item.Item("P", "10heal", 10, "H")
        healTile = "10-H"
        self.assertEqual(potionItem.print_tile(), f"{healTile:<10}")

        weaponItem = Item.Item("W", "5sword", 5, "W")
        weaponTile = "5-W"
        self.assertEqual(weaponItem.print_tile(), f"{weaponTile:<10}")

