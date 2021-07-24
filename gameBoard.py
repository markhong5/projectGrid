
import Player
import Enemy
import Item
import random
import copy
"""
Block ability: player cannot take over the tile for x amount of turns
    PROBLEM: what if the player get's stuck between 2 walls, game is over
movement ability: enemy moves to different blocks
explosion ability: enemy blows up cardinal directional tiles and deals damage
burn/posion ability: enemy deals damage over time
"""
ENEMY_LIST = [Enemy.Enemy("Spider", 3, 4, 2, "SSSSS",image="GameImages/Elise_Spiderling_Render.png" ),
              Enemy.Enemy("Minion", 1, 1, 1, "MMMMM",image="GameImages/Chaos_Minion_Melee_Render.png"),
              Enemy.Enemy("Tiger", 5, 6, 4, "TTTTT",image="GameImages/tigerUdyr.jpg")]
SPECIAL_ENEMIES = [Enemy.Enemy("Bomb", 2, 2, 2, "BBBBB", ["Explode", 3], "GameImages/shroom.png")]
ITEM_LIST = [Item.Item("C", "5coin", 5, "C", 0, image="GameImages/Coin_icon.png"),
             Item.Item("P", "10heal", 10, "H", 8, image="GameImages/potion.jpg"),
             Item.Item("W", "5sword", 5, "W", 3, image="GameImages/longSword.png")]
class NotValidMoveError(Exception):
    """Must be a valid space for the player to move to"""
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message

class GameBoard:
    def __init__(self, height, width, spawnTile = "Normal"):
        #player tile will start at bottom left
        self.board = []
        self.height = height
        self.width = width
        self.playerLocationX = 0
        self.playerLocationY = 2
        self.spawnTile = spawnTile #Controls the types of tiles that spawns

    def makeBoard(self, typeBoard = "normal"):
        for i in range(0,self.height):
            row = []
            for y in range(0,self.width):
                if y == self.playerLocationX and i == self.playerLocationY:
                    row.append(Player.Player())
                elif typeBoard == "spider":
                    spiderEnemy = Enemy.Enemy("Spider", 3, 4, 2, "SSSSS")
                    row.append(spiderEnemy)
                elif typeBoard == "5coin":
                    coinItem = Item.Item("C", "5coin", 5, "5c", 0)
                    row.append(coinItem)
                elif typeBoard == "normal":
                    #60% of the time, choose a random monster to place
                    #otherwise, add a bonous item
                    row.append(self.getNewTile())
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
        if self.spawnTile == "Normal":
            if random.random() <= .6:
                return copy.deepcopy(ENEMY_LIST[random.randint(0, len(ENEMY_LIST) - 1)])
            else:
                return copy.deepcopy(ITEM_LIST[random.randint(0, len(ITEM_LIST) - 1)])
        elif self.spawnTile == "Special":
            if random.random() <= .6:
                return copy.deepcopy(SPECIAL_ENEMIES[random.randint(0, len(SPECIAL_ENEMIES) - 1)])
            else:
                return copy.deepcopy(ITEM_LIST[random.randint(0, len(ITEM_LIST) - 1)])
        elif self.spawnTile == "Both":
            x = random.random()
            if x <= .6 and x > .2:
                return copy.deepcopy(ENEMY_LIST[random.randint(0, len(ENEMY_LIST) - 1)])
            elif x <= .2:
                return copy.deepcopy(SPECIAL_ENEMIES[random.randint(0, len(SPECIAL_ENEMIES) - 1)])
            else:
                return copy.deepcopy(ITEM_LIST[random.randint(0, len(ITEM_LIST) - 1)])


    def makeMove(self, move):
        if(move == "Right"):
            if(self.playerLocationX + 1 >= self.height):
                raise NotValidMoveError("too far to the right")
            else:
                incomingTile = self.board[self.playerLocationY][self.playerLocationX + 1]
                self._updatePlayer(incomingTile)

                self.board[self.playerLocationY][self.playerLocationX + 1] = self.getPlayer()
                self.board[self.playerLocationY][self.playerLocationX] = self.getNewTile()
                self.playerLocationX += 1
        elif(move == "Left"):
            if(self.playerLocationX - 1 < 0):
                raise NotValidMoveError("too far to the left")
            else:
                incomingTile = self.board[self.playerLocationY][self.playerLocationX - 1]
                self._updatePlayer(incomingTile)

                self.board[self.playerLocationY][self.playerLocationX - 1] = self.getPlayer()
                self.board[self.playerLocationY][self.playerLocationX] = self.getNewTile()
                self.playerLocationX -= 1
        elif(move == "Down"):
            if(self.playerLocationY + 1 >= self.width):
                raise NotValidMoveError("too far down")
            else:
                incomingTile = self.board[self.playerLocationY + 1][self.playerLocationX]
                self._updatePlayer(incomingTile)

                self.board[self.playerLocationY + 1][self.playerLocationX] = self.getPlayer()
                self.board[self.playerLocationY][self.playerLocationX] = self.getNewTile()
                self.playerLocationY += 1
        elif(move == "Up"):
            if(self.playerLocationY - 1 < 0):
                raise NotValidMoveError("too far up")
            else:
                incomingTile = self.board[self.playerLocationY - 1][self.playerLocationX]
                self._updatePlayer(incomingTile)

                self.board[self.playerLocationY - 1][self.playerLocationX] = self.getPlayer()
                self.board[self.playerLocationY][self.playerLocationX] = self.getNewTile()
                self.playerLocationY -= 1
        self._updateBoard()

    def _updatePlayer(self, incomingTile):
        if isinstance(incomingTile, Enemy.Enemy):
            self.getPlayer().defeatMonster(incomingTile.defeated())
        elif isinstance(incomingTile, Item.Item):
            self.getPlayer().getItem(incomingTile)

    def _updateBoard(self):
        for i in range(self.height):
            for y in range(self.width):
                tile = self.board[i][y]
                if isinstance(tile, Enemy.Enemy) and tile.getAbility()[0] != None:
                    if tile.getAbility()[0] == "Explode":
                        if tile.countDown() == True:
                            self._explodeBomb(tile, i, y)

    def _explodeBomb(self, bomb, y, x):
        """Tile explodes, dealing it's hp as damage to nearby enemies and dying
        if it hits an item Tile, then that item tile is destroyed
        """

        if y != 0:
            aboveTile = self.board[y - 1][x]
            if isinstance(aboveTile, Item.Item):
                self.board[y - 1][x] = self.getNewTile()
            else:
                aboveTile.hp = aboveTile.hp - bomb.hp
                if aboveTile.hp <= 0 and isinstance(aboveTile, Enemy.Enemy):
                    self.board[y - 1][x] = self.getNewTile()
        if y != self.height - 1:
            belowTile = self.board[y + 1][x]
            if isinstance(belowTile, Item.Item):
                self.board[y + 1][x] = self.getNewTile()
            else:
                belowTile.hp = belowTile.hp - bomb.hp
                if belowTile.hp <= 0 and isinstance(belowTile, Enemy.Enemy):
                    self.board[y + 1][x] = self.getNewTile()
        if x != 0:
            leftTile = self.board[y][x - 1]
            if isinstance(leftTile, Item.Item):
                self.board[y][x - 1] = self.getNewTile()
            else:
                leftTile.hp = leftTile.hp - bomb.hp
                if leftTile.hp <= 0 and isinstance(leftTile, Enemy.Enemy):
                    self.board[y][x - 1] = self.getNewTile()
        if x != self.width - 1:
            rightTile = self.board[y][x + 1]
            if isinstance(rightTile, Item.Item):
                self.board[y][x + 1] = self.getNewTile()
            else:
                rightTile.hp = rightTile.hp - bomb.hp
                if rightTile.hp <= 0 and isinstance(rightTile, Enemy.Enemy):
                    self.board[y][x + 1] = self.getNewTile()

        self.board[y][x] = self.getNewTile()

    def isEnemy(self, x, y):
        return True if isinstance(self.board[x][y], Enemy.Enemy) else False

    def isItem(self, x, y):
        return True if isinstance(self.board[x][y], Item.Item) else False

    def __getitem__(self, item):
        return self.board[item]

