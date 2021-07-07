class NotImplementedError(Exception):
    """For every child tile object, it must override Tile's base functions. Else fail"""
    pass

class Tile:
    #My tile class will be the parent of all of my future classes
    #most of the methods are
    def print_tile(self):
        #How a tile looks when printed
        raise NotImplementedError("moveTile is not implemented")




