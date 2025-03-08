import argparse
from tic_tac.core import game, board, player


def get_user_args() -> argparse.Namespace:
    # TODO add validators
    # TODO use config class
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--size",
        type=str,
        default="7,5",
        help='Game size in format "width,height" (default=7,5)',
    )
    parser.add_argument(
        "--players",
        type=int,
        default=2,
        help="How many players will play? (default=2)",
    )
    parser.add_argument(
        "--computer",
        action="store_true",
        help="Will the game be with a computer?",
    )
    parser.add_argument(
        "--computer_type",
        type=str,
        default="COMPUTER_HARD",
        help="The computer difficulty if `--computer` is selected (default=COMPUTER_HARD)",
    )
    parser.add_argument(
        "--win_length",
        type=int,
        default=3,
        help="How many cells to win? (default=3)",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = get_user_args()
    width, height = map(int, args.size.split(","))

    # Configure game
    board_inst = board.Board(width=width, height=height, win_length=args.win_length)

    game_inst = game.Game(
        board=board_inst,
        number_of_players=args.players,
        computer=args.computer,
        computer_type=player.PlayerType(args.computer_type),
    )

    # Start the gaming loop
    game_inst.run()
