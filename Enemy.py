import Tile



class Enemy(Tile.Tile):

    def __init__(self, name, hp, xp_given, coin_given, tile_description, ability=[None, None],
                 image="GameImages/four04.png"):
        self.name = name
        self.hp = hp
        self.xp_given = xp_given
        self.coin_given = coin_given
        self.tile_description = tile_description
        self.color = "RED"
        self.ability = ability
        self.image = image

    def print_tile(self):
        enemyTile = str(self.hp) + "-" + self.tile_description
        return f"{enemyTile:<10}"

    def defeated(self):
        return [self.hp, self.xp_given, self.coin_given]

    def countDown(self):
        """Count's down to when a given action will occur"""

        self.ability[1] -= 1
        if self.ability[1] < 0:
            return True
        else:
            return False

    def getAbility(self):
        """get what an ability is"""
        return self.ability



