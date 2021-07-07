import Tile

class Enemy(Tile.Tile):

    def __init__(self, name, hp, xp_given, coin_given, tile_description):
        self.name = name
        self.hp = hp
        self.xp_given = xp_given
        self.coin_given = coin_given
        self.tile_description = tile_description
        self.color = "RED"

    def print_tile(self):

        enemyTile = str(self.hp) + "-" + self.tile_description
        return f"{enemyTile:<10}"

    def defeated(self):
        return [self.hp, self.xp_given, self.coin_given]