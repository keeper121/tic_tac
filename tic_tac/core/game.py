from warnings import catch_warnings

import attr

from tic_tac.core import board, player


@attr.s(auto_attribs=True, kw_only=True)
class Game:
    number_of_players: int = 2
    board: board.Board
    win_length: int
    players: list[player.Player] = attr.ib(init=False)

    def __attrs_post_init__(self):
        self.players = [
            player.Player(
                id=i,
                type=player.PlayerType.USER
            )
            for i in range(self.number_of_players)
        ]
        self.players[1].type = player.PlayerType.COMPUTER

    def run(self):
        """Main game loop"""
        self.board.draw()  # empty board

        current_status = board.BoardStatus.IN_PROGRESS
        while current_status == board.BoardStatus.IN_PROGRESS:
            for pl in self.players:
                while True:
                    if pl.type == player.PlayerType.USER:
                        i, j = map(int, input(f"Write a position for a move for the Player {pl.id}: ").split(","))
                    else:
                        i, j = self.board.predict_next_position(player=pl)

                    position = (i, j)
                    try:
                        self.board.step(
                            position=position,
                            player=pl,
                        )
                        break
                    except IndexError:
                        print("Wrong position. Make a step again.")

                self.board.draw()
                current_status = self.board.check_solution(
                    current_position=position,
                    player=pl,
                    win_length=self.win_length,
                )
                if current_status == board.BoardStatus.ENDED:
                    print(f"Player {pl.id} won!")
                    break
                elif current_status == board.BoardStatus.TIE:
                    print(f"It's a tie")
                    break
