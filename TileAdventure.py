import gameBoard

MOVE_DICT = {
    "w": "Up",
    "s": "Down",
    "a": "Left",
    "d": "Right"

}

if __name__ == "__main__":
    myGameBoard = gameBoard.GameBoard(3, 3, "Both")
    myGameBoard.makeBoard()
    print(myGameBoard.printBoard())
    print(myGameBoard.getPlayer().print_playerDetails())

    while(myGameBoard.getPlayer().outOfHP() != True):
        move = input("move the player (WASD)\n")

        if move in ["w", "a", "s", "d", "W", "A", "S", "D"]:
            try:
                myGameBoard.makeMove(MOVE_DICT[move.lower()])
            except gameBoard.NotValidMoveError:
                print("INVALID MOVE")
            print(myGameBoard.printBoard())
            print(myGameBoard.getPlayer().print_playerDetails())
        else:
            print("not a WASD key")

    print("\nGAME OVER")



