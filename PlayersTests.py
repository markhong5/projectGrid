import Player
import unittest
import Enemy
import Item
class TestTile(unittest.TestCase):

    def test_playerisinstanceofTile(self):

        playerA = Player.Player()

        self.assertTrue(isinstance(playerA, Player.Tile.Tile))

    def test_printPlayer(self):
        playerA = Player.Player()
        self.assertEqual(playerA.print_tile(), "PPPPP     ")

    def test_loseHP(self):
        playerA = Player.Player()
        self.assertEqual(playerA.loseHP(8), 2)

    def test_defeatMonster(self):
        playerA = Player.Player()
        aEnemy = Enemy.Enemy("Spider", 3, 4, 2, "SSSSS")
        playerA.defeatMonster(aEnemy.defeated())
        self.assertTrue(playerA.hp == 7 and playerA.xp == 4 and playerA.coin == 2)

        # bEnemy = Enemy.Enemy("Tiger", 8, 9, 10, "TTTTT")
        # self.assertEqual(bEnemy.defeated(), [8, 9, 10])
        #
        # cEnemy = Enemy.Enemy("Dragon", 20, 15, 20, "DDDDD")
        # self.assertEqual(playerA.defeatMonster(), 2)

    def test_getItem(self):
        playerA = Player.Player()
        coinItem = Item.Item("C", "5coin", 5, "C")
        potionItem = Item.Item("P", "10heal", 10, "H")
        weaponItem = Item.Item("W", "5sword", 5, "W")
        playerA.getItem(coinItem)
        playerA.getItem(potionItem)
        playerA.getItem(weaponItem)
        self.assertTrue(playerA.coin == 5)
        self.assertTrue(playerA.hp == 20)
        self.assertTrue(playerA.equipment == weaponItem)

    def test_outOfHP(self):
        playerA = Player.Player()
        playerA.hp = 0
        self.assertTrue(playerA.outOfHP())