import Enemy
import unittest
class TestTile(unittest.TestCase):

    def test_printEnemyCorrectly(self):
        aEnemy = Enemy.Enemy("Spider", 3, 4, 2, "SSSSS")

        self.assertEqual(aEnemy.print_tile(), "3-SSSSS   ")

        bEnemy = Enemy.Enemy("Tiger", 8, 9, 10, "TTTTT")
        self.assertEqual(bEnemy.print_tile(), "8-TTTTT   ")

        cEnemy = Enemy.Enemy("Dragon", 20, 15, 20, "DDDDD")

        correctString = "20-DDDDD"
        self.assertEqual(cEnemy.print_tile(), f"{correctString:<10}")

    def test_defeatedEnemy(self):
        aEnemy = Enemy.Enemy("Spider", 3, 4, 2, "SSSSS")

        self.assertEqual(aEnemy.defeated(), [3, 4, 2])

        bEnemy = Enemy.Enemy("Tiger", 8, 9, 10, "TTTTT")
        self.assertEqual(bEnemy.defeated(), [8, 9, 10])

        cEnemy = Enemy.Enemy("Dragon", 20, 15, 20, "DDDDD")

        self.assertEqual(cEnemy.defeated(), [20, 15, 20])