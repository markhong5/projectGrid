
import Tile
import copy

BASE_HP = 10
BASE_MAXHP = 10
LEVELXP_INCREASE = 5
MAXHP_INCREASE = 5

class Player(Tile.Tile):


    def __init__(self):
        self.hp = BASE_HP
        self.maxHP = BASE_MAXHP
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
        playerDetails = "level: {} hp:{}/{} xp:{}/{} coin:{} equipment:{} "
        return playerDetails.format(self.level, self.hp,self.maxHP, self.xp, self.toLevelUp, self.coin, self.equipment)

    def loseHP(self, hpLost):
        self.hp -= hpLost
        return self.hp

    def defeatMonster(self, monsterStats):
        if(self.equipment != None):
            self.equipment.bonus -= monsterStats[0]
            if(self.equipment.bonus <= 0):
                self.hp += self.equipment.bonus
                self.equipment = None
        else:
            self.hp -= monsterStats[0]
        self.xp += monsterStats[1]
        self.coin += monsterStats[2]
        self.levelUp()

    def getItem(self, item):
        if item.type == "C":
            self.coin += item.bonus
        elif item.type == "P" and item.cost <= self.coin:
            self.coin -= item.cost
            self.hp += item.bonus
            if(self.hp > self.maxHP):
                self.hp = self.maxHP

        elif item.type == "W" and item.cost <= self.coin:
            self.coin -= item.cost
            self.equipment = copy.deepcopy(item)


    def outOfHP(self):
        return True if self.hp <= 0 else False

    def levelUp(self):
        while self.xp >= self.toLevelUp:
            self.maxHP += MAXHP_INCREASE
            self.hp = self.maxHP
            self.xp = self.xp - self.toLevelUp
            self.toLevelUp += LEVELXP_INCREASE
            self.level += 1



