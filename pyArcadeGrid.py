
import arcade
import gameBoard
# Set how many rows and columns we will have
ROW_COUNT = 3
COLUMN_COUNT = 3

# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 250
HEIGHT = 300

# This sets the margin between each cell and on the edges of the screen.
MARGIN = 10
# This sets how large the UI is at the top of the screen
UIHEIGHT = 25

#How large the bonus text is at the bottom of a tile
BONUS_OFFSET_X = -50
BONUS_OFFSET_Y = -125

# Do the math to figure out our screen dimensions
SCREEN_WIDTH = (WIDTH + MARGIN) * COLUMN_COUNT + MARGIN
SCREEN_HEIGHT = (HEIGHT + MARGIN) * ROW_COUNT + MARGIN + UIHEIGHT
SCREEN_TITLE = "League Of Legends Game"

#1 is player, Green
#2 is enemies, Red
#3 is items, Blue


class ShapeTile(arcade.Shape):
    """ Sprite with hit points """

    def __init__(self, center_x, center_y, tile, type):
        super().__init__()

        # Bonus is the number
        self.center_x = center_x
        self.center_y = center_y
        self.tile = tile
        self.type = type
        #type is weather its a enemy, weapon, coin, or heal
            #E = enemy
            #C = coin
            #W = weapon
            #P = heal

    def draw_tile_number(self):
        """ Draw important information about the tile"""
        tile_string = "NOTHING"
        if self.type == "I":
            if self.tile.type == "W" or self.tile.type == "P":
                tile_string = f"{self.tile.type} : {self.tile.bonus} : {self.tile.cost}"
            else:
                tile_string = f"{self.tile.type} : {self.tile.bonus}"
        else:
            if self.tile.getAbility()[0] == None:
                tile_string = f"{self.tile.name} : {self.tile.hp}"
            else:
                tile_string = f"{self.tile.name} : {self.tile.hp} : {self.tile.ability[1] + 1}"

        arcade.draw_text(text= tile_string,
                         start_x=self.center_x + 0, #BONUS_OFFSET_X,
                         start_y=self.center_y + 0, #BONUS_OFFSET_Y,
                         font_size= 35,
                         color=arcade.color.WHITE,
                         align= "right",
                         anchor_x="center", anchor_y="center")

class MainPlayer(arcade.Sprite):
    def __init__(self, scale=1):
        # self.player = player
        self.image = "GameImages/Alistar_Splash_Tile_Crown.jpg"
        super().__init__(self.image, scale, hit_box_algorithm="None")

class Enemies(arcade.Sprite):
    def __init__(self, enemyTexture, scale=1):
        self.image = enemyTexture
        super().__init__(self.image, scale, hit_box_algorithm="None")

class Items(arcade.Sprite):
    def __init__(self, itemTexture, scale=1):
        self.image = itemTexture
        super().__init__(self.image, scale, hit_box_algorithm="None")


class MyGame(arcade.View):
    """
    Main application class.
    """

    def __init__(self):
        """
        Set up the application.
        """
        super().__init__()
        self.tile_list = None
        self.player = None
        self.enemies = None
        self.items = None


        self.myGameBoard = gameBoard.GameBoard(3, 3, "Both")
        self.myGameBoard.makeBoard("normal")

        arcade.set_background_color(arcade.color.BLACK)
        self.recreate_grid()
        #DEBUGGING PURPOSES
        print(self.myGameBoard.printBoard())
        print(self.myGameBoard.getPlayer().print_playerDetails())

    def recreate_grid(self):
        self.tile_list = arcade.ShapeElementList()
        self.player = arcade.SpriteList()
        self.enemies = arcade.SpriteList()
        self.items =  arcade.SpriteList()
        for row in range(ROW_COUNT):
            for column in range(COLUMN_COUNT):
                if self.myGameBoard[row][column].color == "GREEN":
                    color = arcade.color.GREEN
                elif self.myGameBoard[row][column].color == "RED":
                    color = arcade.color.RED
                elif self.myGameBoard[row][column].color == "BLUE":
                    color = arcade.color.BLUE
                else:
                    color = arcade.color.WHITE

                x = (MARGIN + WIDTH) * column + MARGIN + WIDTH // 2
                #(ROW_COUNT - row - 1) is for proper pixel alignment
                y = (MARGIN + HEIGHT) * (ROW_COUNT - row - 1) + MARGIN + HEIGHT // 2

                # current_rect = arcade.create_rectangle_filled(x, y, WIDTH, HEIGHT, color)
                #If it is not a player tile
                if color != arcade.color.GREEN:
                    current_rect = arcade.create_rectangle_filled(x, y, WIDTH, HEIGHT, color)
                    if self.myGameBoard.isItem(row, column):
                        currentTile = ShapeTile(x, y, self.myGameBoard[row][column], "I")
                        item = Items(self.myGameBoard[row][column].image)
                        item.position = x, y
                        item.width = WIDTH
                        item.height = HEIGHT
                        self.items.append(item)
                    else:
                        currentTile = ShapeTile(x, y, self.myGameBoard[row][column], "E")
                        enemy = Enemies(self.myGameBoard[row][column].image)
                        enemy.position = x, y
                        enemy.width = WIDTH
                        enemy.height = HEIGHT
                        self.enemies.append(enemy)
                    self.tile_list.append(currentTile)
                else:
                    playerOne = MainPlayer()
                    playerOne.position = x, y
                    playerOne.width = WIDTH
                    playerOne.height = HEIGHT
                    self.player.append(playerOne)


    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        arcade.start_render()
        self.player.draw()
        self.enemies.draw()
        self.items.draw()
        # This draws the text for all item/enemy tiles
        for tile in self.tile_list:
            tile.draw_tile_number()
        #Have information text at the top of the screen

        arcade.draw_text(self.myGameBoard.getPlayer().print_playerDetails(), 10, SCREEN_HEIGHT - UIHEIGHT - 5, arcade.color.WHITE, 20)

    def move(self, movement):
        try:
            self.myGameBoard.makeMove(movement)
            self.recreate_grid()
        except gameBoard.NotValidMoveError as e:
            print(e.message)

        #DEBUGGING PURPOSES
        print(self.myGameBoard.printBoard())
        print(self.myGameBoard.getPlayer().print_playerDetails())
        if self.myGameBoard.getPlayer().outOfHP() == True:
            view = GameOverView()
            self.window.show_view(view)

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.RIGHT:
            self.move("Right")
        elif symbol == arcade.key.UP:
            self.move("Up")
        elif symbol == arcade.key.DOWN:
            self.move("Down")
        elif symbol == arcade.key.LEFT:
            self.move("Left")

class GameOverView(arcade.View):
    """ View to show when game is over """

    def __init__(self):
        """ This is run once when we switch to this view """
        super().__init__()
        self.texture = arcade.load_texture("GameImages/game_over.png")

        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        arcade.set_viewport(0, SCREEN_WIDTH - 1, 0, SCREEN_HEIGHT - 1)

    def on_draw(self):
        """ Draw this view """
        arcade.start_render()
        self.texture.draw_sized(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                                SCREEN_WIDTH, SCREEN_HEIGHT)

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """ If the user presses the mouse button, re-start the game. """
        game_view = MyGame()
        self.window.show_view(game_view)

def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    startView = MyGame()
    window.show_view(startView)
    arcade.run()


if __name__ == "__main__":
    main()