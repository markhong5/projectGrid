
import arcade
import gameBoard
# Set how many rows and columns we will have
ROW_COUNT = 3
COLUMN_COUNT = 3

# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 200
HEIGHT = 250

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

    def __init__(self, center_x, center_y, type, bonus):
        super().__init__()

        # Bonus is the number
        self.center_x = center_x
        self.center_y = center_y
        self.bonus = bonus
        #type is weather its a enemy, weapon, coin, or heal
            #E = enemy
            #C = coin
            #W = weapon
            #P = heal
        self.type = type

    def draw_tile_number(self):
        """ Draw how many hit points we have """

        tile_string = f"{self.type} : {self.bonus}"
        arcade.draw_text(tile_string,
                         start_x=self.center_x + BONUS_OFFSET_X,
                         start_y=self.center_y + BONUS_OFFSET_Y,
                         font_size=45,
                         color=arcade.color.WHITE)

class MyGame(arcade.View):
    """
    Main application class.
    """

    def __init__(self):
        """
        Set up the application.
        """
        super().__init__()

        self.shape_list = None
        self.tile_list = None
        self.myGameBoard = gameBoard.GameBoard(3, 3)
        self.myGameBoard.makeBoard("normal")

        arcade.set_background_color(arcade.color.BLACK)
        self.recreate_grid()
        print(self.myGameBoard.printBoard())
        print(self.myGameBoard.getPlayer().print_playerDetails())

    def recreate_grid(self):
        self.shape_list = arcade.ShapeElementList()
        self.tile_list = arcade.ShapeElementList()
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

                current_rect = arcade.create_rectangle_filled(x, y, WIDTH, HEIGHT, color)
                #If it is not a player tile
                if color != arcade.color.GREEN:
                    currentTile = None
                    if self.myGameBoard.isEnemy(row, column):
                        currentTile = ShapeTile(x, y, "E", self.myGameBoard[row][column].hp)
                    else:
                        currentTile = ShapeTile(x, y, self.myGameBoard[row][column].type,
                                                self.myGameBoard[row][column].bonus)
                    self.tile_list.append(currentTile)

                self.shape_list.append(current_rect)

    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        arcade.start_render()

        self.shape_list.draw()
        for tile in self.tile_list:
            tile.draw_tile_number()
        #Have information text at the top of the screen
        arcade.draw_text(self.myGameBoard.getPlayer().print_playerDetails(), 10, SCREEN_HEIGHT - UIHEIGHT - 5, arcade.color.WHITE, 20)

    def move(self, movement):
        try:
            self.myGameBoard.makeMove(movement)
            self.recreate_grid()
        except gameBoard.NotValidMoveError:
            print("INVALID MOVE")


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