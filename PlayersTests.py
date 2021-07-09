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

        bEnemy = Enemy.Enemy("Spider", 0, 2, 2, "SSSSS")
        playerA.defeatMonster(bEnemy.defeated())
        self.assertTrue(playerA.xp == 1 and playerA.level == 2)

        cEnemy = Enemy.Enemy("Spider", 0, 24, 2, "SSSSS")
        playerA.defeatMonster(cEnemy.defeated())
        self.assertTrue(playerA.xp == 0 and playerA.level == 4)

    def test_getItem(self):
        playerA = Player.Player()
        coinItem = Item.Item("C", "5coin", 5, "C", 0)
        potionItem = Item.Item("P", "10heal", 10, "H", 8)
        weaponItem = Item.Item("W", "5sword", 5, "W", 3)
        aEnemy = Enemy.Enemy("Spider", 3, 4, 0, "SSSSS")
        playerA.defeatMonster(aEnemy.defeated())
        playerA.getItem(coinItem)

        self.assertTrue(playerA.coin == 5)
        playerA.getItem(coinItem)
        playerA.getItem(coinItem)
        playerA.getItem(potionItem)
        playerA.getItem(weaponItem)
        self.assertTrue(playerA.hp == 10)
        self.assertTrue(playerA.equipment.name == weaponItem.name and playerA.equipment.bonus == weaponItem.bonus)
        self.assertTrue(playerA.coin == 4)

    def test_cantAffordItem(self):
        playerA = Player.Player()
        coinItem = Item.Item("C", "5coin", 5, "C", 0)
        potionItem = Item.Item("P", "10heal", 10, "H", 8)
        weaponItem = Item.Item("W", "5sword", 5, "W", 3)
        aEnemy = Enemy.Enemy("Spider", 3, 4, 0, "SSSSS")
        playerA.defeatMonster(aEnemy.defeated())
        playerA.getItem(potionItem)
        playerA.getItem(weaponItem)
        self.assertTrue(playerA.hp == 7 and playerA.coin == 0 and playerA.equipment == None)
        playerA.getItem(coinItem)
        playerA.getItem(potionItem)
        playerA.getItem(weaponItem)
        self.assertTrue(playerA.hp == 7 and playerA.coin == 2)
        self.assertTrue(playerA.equipment.name == weaponItem.name and playerA.equipment.bonus == weaponItem.bonus)

    def test_outOfHP(self):
        playerA = Player.Player()
        playerA.hp = 0
        self.assertTrue(playerA.outOfHP())

    def test_levelUP(self):
        playerA = Player.Player()
        playerA.xp += playerA.toLevelUp
        playerA.levelUp()
        self.assertEqual(playerA.level, 2)
        self.assertEqual(playerA.xp, 0)
        self.assertEqual(playerA.toLevelUp, 10)
        self.assertEqual(playerA.maxHP, playerA.hp)

        playerA.xp += 9
        playerA.xp += 5

        playerA.levelUp()
        self.assertEqual(playerA.level, 3)
        self.assertEqual(playerA.xp, 4)
        self.assertEqual(playerA.toLevelUp, 15)
        self.assertEqual(playerA.maxHP, playerA.hp)

