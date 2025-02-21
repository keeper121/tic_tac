from tic_tac.core import game, board

if __name__ == "__main__":
    # number_of_players = input("How many players will play?")
    # size = input("What the game size? Specify in format: width, height")
    number_of_players = 2
    width, height = 7, 5
    win_length = 3 # win len
    # width, height = map(int, size.split(","))

    board_inst = board.Board(
        width=width,
        height=height,
    )

    game_inst = game.Game(
        board=board_inst,
        number_of_players=number_of_players,
        win_length=win_length
    )
    game_inst.run()
