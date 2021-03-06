import Tile

class Item(Tile.Tile):

    #Gold: gives money
    #potion: gives hp
    #weapon: get weapon
    #FIXME: Add chests that give unique items/bonuses

    def __init__(self, type, name, bonus, tile_descrption, cost, image = "GameImages/four04.png"):
        self.type = type
        self.name = name

        self.bonus = bonus
        self.tile_descrption = tile_descrption
        self.color = "BLUE"
        self.cost = cost
        self.image = image

    def print_tile(self):
        itemTile = str(self.bonus) + "-" + self.tile_descrption
        return f"{itemTile:<10}"

    def __str__(self):
        return f"{self.name}, Attack:{self.bonus}, Cost:{self.cost}"