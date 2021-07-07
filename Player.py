
import Tile
import copy
class Player(Tile.Tile):
    BASE_HP = 10
    BASE_XP = 0
    BASE_MONEY = 0

    def __init__(self):
        self.hp = 10
        self.xp = 0
        self.coin = 0
        self.toLevelUp = 5
        self.equipment = None
        self.level = 1
        self.color = "GREEN"

    def print_tile(self):
        #How a tile looks when printed
        playerString = "PPPPP"
        return f"{playerString:<10}"

    def print_playerDetails(self):
        playerDetails = "level: {} hp:{} xp:{} coin:{} equipment:{} "
        return playerDetails.format(self.level, self.hp, self.xp, self.coin, self.equipment)

    def loseHP(self, hpLost):
        self.hp -= hpLost
        return self.hp

    def defeatMonster(self, monsterStats):
        #FIXME include levelup when enough xp is received
        if(self.equipment != None):
            self.equipment.bonus -= monsterStats[0]
            if(self.equipment.bonus <= 0):
                self.hp += self.equipment.bonus
                self.equipment = None
        else:
            self.hp -= monsterStats[0]
        self.xp += monsterStats[1]
        self.coin += monsterStats[2]

    def getItem(self, item):
        if item.type == "C":
            self.coin += item.bonus
        elif item.type == "P":
            self.hp += item.bonus
        elif item.type == "W":
            self.equipment = copy.deepcopy(item)


    def outOfHP(self):
        return True if self.hp <= 0 else False

