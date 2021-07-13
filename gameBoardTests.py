import unittest
import gameBoard
import Tile
import Player
import Enemy
import Item
class TestgameBoard(unittest.TestCase):

    def test_BoardInitialization(self):
        gBoard = gameBoard.GameBoard(3, 3)

        self.assertEqual(gBoard.height, 3)
        self.assertEqual(gBoard.width, 3)

        aBoard = gameBoard.GameBoard(5, 3)

        self.assertEqual(aBoard.width, 3)
        self.assertEqual(aBoard.height, 5)

        bBoard = gameBoard.GameBoard(2, 7)

        self.assertEqual(bBoard.width, 7)
        self.assertEqual(bBoard.height, 2)

    def test_createBoard(self):
        gBoard = gameBoard.GameBoard(2, 2)
        gBoard.createBoard([
            [Enemy.Enemy("Spider", 3, 4, 2, "SSSSS"), Enemy.Enemy("Spider", 3, 4, 2, "SSSSS")],
            [Enemy.Enemy("Spider", 3, 4, 2, "SSSSS"), Enemy.Enemy("Spider", 3, 4, 2, "SSSSS")]
        ])

        for i in range(0, 2):
            for y in range(0, 2):
                self.assertTrue(isinstance(gBoard.board[i][y], Enemy.Enemy))

        aBoard = gameBoard.GameBoard(1, 2)
        aBoard.createBoard([
            [Item.Item("C", "5coin", 5, "C", 0), Enemy.Enemy("Spider", 3, 4, 2, "SSSSS")]
        ])

        self.assertTrue(isinstance(aBoard.board[0][0], Item.Item))
        self.assertTrue(isinstance(aBoard.board[0][1], Enemy.Enemy))

        bBoard = gameBoard.GameBoard(2, 1)

        bBoard.createBoard([
            [Item.Item("C", "5coin", 5, "C", 0)],
            [Item.Item("P", "10heal", 10, "H", 8)]
        ])
        self.assertTrue(isinstance(bBoard.board[0][0], Item.Item))
        self.assertTrue(isinstance(bBoard.board[1][0], Item.Item))

    def test_TileInBoard(self):
        gBoard = gameBoard.GameBoard(3, 3)
        gBoard.makeBoard("spider")

        for i in range(3):
            for y in range(3):
                self.assertTrue(isinstance(gBoard.board[y][i], Tile.Tile))

    def test_PrintBoard(self):
        #Make sure print board works with all spiders on a 3x3
        gBoard = gameBoard.GameBoard(3, 3)
        gBoard.makeBoard("spider")
        self.assertEqual(gBoard.printBoard(), "3-SSSSS   ||3-SSSSS   ||3-SSSSS   \n"
                                               "3-SSSSS   ||3-SSSSS   ||3-SSSSS   \n"
                                                "PPPPP     ||3-SSSSS   ||3-SSSSS   \n")

        gBoard = gameBoard.GameBoard(4, 3)
        gBoard.makeBoard("5coin")
        gBoard.printBoard()
        self.assertEqual(gBoard.printBoard(), "5-5c      ||5-5c      ||5-5c      \n"
                                               "5-5c      ||5-5c      ||5-5c      \n"
                                               "PPPPP     ||5-5c      ||5-5c      \n"
                                                "5-5c      ||5-5c      ||5-5c      \n")

    def test_GetPlayer(self):
        gBoard = gameBoard.GameBoard(3, 3)
        gBoard.makeBoard("normal")
        self.assertTrue(isinstance(gBoard.getPlayer(), Player.Player))

    def test_MoveInToEnemyRight(self):
        gBoard = gameBoard.GameBoard(3, 3)
        gBoard.makeBoard("spider")
        gBoard.makeMove("Right")
        self.assertTrue(gBoard.getPlayer() == gBoard.board[2][1])
        self.assertTrue(gBoard.getPlayer().hp == 7 and gBoard.getPlayer().xp == 4 and gBoard.getPlayer().coin == 2)

    def test_MoveInToLeft(self):
        gBoard = gameBoard.GameBoard(3, 3)

        gBoard.makeBoard("spider")
        gBoard.makeMove("Right")
        gBoard.makeMove("Left")
        self.assertTrue(gBoard.getPlayer() == gBoard.board[2][0])

    def test_MoveDown(self):
        gBoard = gameBoard.GameBoard(3, 3)

        gBoard.makeBoard("spider")
        gBoard.makeMove("Up")
        gBoard.makeMove("Down")
        self.assertTrue(gBoard.getPlayer() == gBoard.board[2][0])

    def test_MoveUp(self):
        gBoard = gameBoard.GameBoard(3, 3)

        gBoard.makeBoard("spider")
        gBoard.makeMove("Up")
        self.assertTrue(gBoard.getPlayer() == gBoard.board[1][0])

    def test_GoingBeyondBoardFails(self):
        gBoard = gameBoard.GameBoard(3, 3)
        gBoard.makeBoard("spider")
        self.assertRaises(gameBoard.NotValidMoveError, gBoard.makeMove, "Left")
        gBoard.makeMove("Right")
        self.assertTrue(gBoard.getPlayer() == gBoard.board[2][1])
        gBoard.makeMove("Right")
        self.assertTrue(gBoard.getPlayer() == gBoard.board[2][2])
        self.assertRaises(gameBoard.NotValidMoveError, gBoard.makeMove, "Right")
        self.assertTrue(gBoard.getPlayer() == gBoard.board[2][2])
        self.assertRaises(gameBoard.NotValidMoveError, gBoard.makeMove, "Down")
        self.assertTrue(gBoard.getPlayer() == gBoard.board[2][2])
        gBoard.makeMove("Up")
        gBoard.makeMove("Up")
        self.assertRaises(gameBoard.NotValidMoveError, gBoard.makeMove, "Up")
        self.assertTrue(gBoard.getPlayer() == gBoard.board[0][2])

    def test_ExplosionEnemies(self):
        gBoard = gameBoard.GameBoard(3, 3)
        gBoard.createBoard([
            [ Enemy.Enemy("Spider", 3, 4, 2, "SSSSS"), Enemy.Enemy("Spider", 3, 4, 2, "SSSSS"),Enemy.Enemy("Spider", 3, 4, 2, "SSSSS")],
            [Enemy.Enemy("Spider", 3, 4, 2, "SSSSS"), Enemy.Enemy("Bomb", 1, 1, 1, "BBBBB", ["Explode", 0]), Enemy.Enemy("Spider", 3, 4, 2, "SSSSS")],
            [Player.Player(), Enemy.Enemy("Spider", 3, 4, 2, "SSSSS"), Enemy.Enemy("Spider", 3, 4, 2, "SSSSS")]
        ])
        aBomb = gBoard[1][1]
        gBoard.makeMove("Right")
        self.assertEqual(gBoard.getPlayer().hp, 6)
        self.assertEqual(gBoard[0][1].hp, 2)
        self.assertEqual(gBoard[1][0].hp, 2)
        self.assertEqual(gBoard[1][2].hp, 2)
        self.assertTrue(gBoard[1][1] != aBomb)
        print(gBoard.printBoard())

        cBoard = gameBoard.GameBoard(3, 2)
        cBoard.createBoard([
            [Item.Item("C", "5coin", 5, "C", 0), Enemy.Enemy("Spider", 3, 4, 2, "SSSSS")],
            [Item.Item("C", "5coin", 5, "C", 0), Enemy.Enemy("Bomb", 1, 1, 1, "BBBBB", ["Explode", 0])],
            [Player.Player(), Enemy.Enemy("Bomb", 1, 1, 1, "BBBBB", ["Explode", 1])]
        ])

        pointerToCoin = cBoard[1][0]
        cBoard.makeMove("Right")
        self.assertEqual(cBoard.getPlayer().hp, 8)
        self.assertEqual(cBoard[0][1].hp, 2)
        self.assertIsNot(pointerToCoin, cBoard[1][0])

    def test_CountDown(self):
        gBoard = gameBoard.GameBoard(3, 3)
        gBoard.createBoard([
            [ Enemy.Enemy("Spider", 3, 4, 2, "SSSSS"), Enemy.Enemy("Spider", 3, 4, 2, "SSSSS"),Enemy.Enemy("Spider", 3, 4, 2, "SSSSS")],
            [Enemy.Enemy("Spider", 3, 4, 2, "SSSSS"), Enemy.Enemy("Bomb", 1, 1, 1, "BBBBB", ["Explode", 3]), Enemy.Enemy("Spider", 3, 4, 2, "SSSSS")],
            [Player.Player(), Enemy.Enemy("Spider", 3, 4, 2, "SSSSS"), Enemy.Enemy("Spider", 3, 4, 2, "SSSSS")]
        ])
        aBomb = gBoard[1][1]
        gBoard.makeMove("Right")
        self.assertIs(aBomb, gBoard[1][1])
        gBoard.makeMove("Right")
        self.assertIs(aBomb, gBoard[1][1])
        gBoard.makeMove("Up")

        self.assertIs(aBomb, gBoard[1][1])
        gBoard.makeMove("Left")
        self.assertIsNot(aBomb, gBoard[1][1])