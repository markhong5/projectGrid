
import Player
import Enemy
import Item
import random

ENEMY_LIST = [Enemy.Enemy("Spider", 3, 4, 2, "SSSSS"), Enemy.Enemy("Mushroom", 1, 1, 1, "MMMMM"),
              Enemy.Enemy("Tiger", 5, 6, 4, "TTTTT")]
ITEM_LIST = [Item.Item("C", "5coin", 5, "C"), Item.Item("P", "10heal", 10, "H"), Item.Item("W", "5sword", 5, "W")]
class NotValidMoveError(Exception):
    """Must be a valid space for the player to move to"""
    pass

class GameBoard:
    def __init__(self, width, height):
        #player tile will start at top left
        self.board = []
        self.width = width
        self.height = height
        self.playerLocationX = 0
        self.playerLocationY = 2

    def makeBoard(self, typeBoard):
        for i in range(0, self.height):
            row = []
            for y in range(0, self.width):
                if y == self.playerLocationX and i == self.playerLocationY:
                    row.append(Player.Player())
                elif typeBoard == "spider":
                    spiderEnemy = Enemy.Enemy("Spider", 3, 4, 2, "SSSSS")
                    row.append(spiderEnemy)
                elif typeBoard == "5coin":
                    coinItem = Item.Item("C", "5coin", 5, "5c")
                    row.append(coinItem)
                elif typeBoard == "normal":
                    #60% of the time, choose a random monster to place
                    #otherwise, add a bonous item
                    if random.random() <= .6:
                        row.append(ENEMY_LIST[random.randint(0, len(ENEMY_LIST) - 1)])
                    else:
                        row.append(ITEM_LIST[random.randint(0, len(ITEM_LIST) - 1)])
            self.board.append(row)
    def createBoard(self, board):
        self.board = board

    def printBoard(self):
        boardString = ""
        for i in range(self.height):
            for y in range(self.width):
                boardString += self.board[i][y].print_tile()
                if y != self.width - 1:
                    boardString += "||"
            boardString += "\n"
        return boardString

    def getPlayer(self):
        return self.board[self.playerLocationY][self.playerLocationX]

    def getNewTile(self):
        if random.random() <= .6:
            return ENEMY_LIST[random.randint(0, len(ENEMY_LIST) - 1)]
        else:
            return ITEM_LIST[random.randint(0, len(ITEM_LIST) - 1)]

    def makeMove(self, move):
        if(move == "Right"):
            if(self.playerLocationX + 1 >= self.width):
                raise NotValidMoveError("too far to the right")
            else:
                incomingTile = self.board[self.playerLocationY][self.playerLocationX + 1]
                if isinstance(incomingTile, Enemy.Enemy):
                    self.getPlayer().defeatMonster(incomingTile.defeated())
                elif isinstance(incomingTile, Item.Item):
                    self.getPlayer().getItem(incomingTile)

                self.board[self.playerLocationY][self.playerLocationX + 1] = self.getPlayer()
                self.board[self.playerLocationY][self.playerLocationX] = self.getNewTile()
                self.playerLocationX += 1
        elif(move == "Left"):
            if(self.playerLocationX - 1 < 0):
                raise NotValidMoveError("too far to the left")
            else:
                incomingTile = self.board[self.playerLocationY][self.playerLocationX - 1]
                if isinstance(incomingTile, Enemy.Enemy):
                    self.getPlayer().defeatMonster(incomingTile.defeated())
                elif isinstance(incomingTile, Item.Item):
                    self.getPlayer().getItem(incomingTile)

                self.board[self.playerLocationY][self.playerLocationX - 1] = self.getPlayer()
                self.board[self.playerLocationY][self.playerLocationX] = self.getNewTile()
                self.playerLocationX -= 1
        elif(move == "Down"):
            if(self.playerLocationY + 1 >= self.height):
                raise NotValidMoveError("too far down")
            else:
                incomingTile = self.board[self.playerLocationY + 1][self.playerLocationX]
                if isinstance(incomingTile, Enemy.Enemy):
                    self.getPlayer().defeatMonster(incomingTile.defeated())
                elif isinstance(incomingTile, Item.Item):
                    self.getPlayer().getItem(incomingTile)

                self.board[self.playerLocationY + 1][self.playerLocationX] = self.getPlayer()
                self.board[self.playerLocationY][self.playerLocationX] = self.getNewTile()
                self.playerLocationY += 1
        elif(move == "Up"):
            if(self.playerLocationY - 1 < 0):
                raise NotValidMoveError("too far up")
            else:
                incomingTile = self.board[self.playerLocationY - 1][self.playerLocationX]
                if isinstance(incomingTile, Enemy.Enemy):
                    self.getPlayer().defeatMonster(incomingTile.defeated())
                elif isinstance(incomingTile, Item.Item):
                    self.getPlayer().getItem(incomingTile)

                self.board[self.playerLocationY - 1][self.playerLocationX] = self.getPlayer()
                self.board[self.playerLocationY][self.playerLocationX] = self.getNewTile()
                self.playerLocationY -= 1

    def isEnemy(self, x, y):
        return True if isinstance(self.board[x][y], Enemy.Enemy) else False

    def __getitem__(self, item):
        return self.board[item]

