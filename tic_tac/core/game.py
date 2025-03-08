import attr

from tic_tac import core


@attr.s(auto_attribs=True, kw_only=True)
class Game:
    number_of_players: int = 2
    board: core.Board
    players: list[core.Player] = attr.ib(init=False)

    computer: bool = False
    computer_type: core.PlayerType = core.PlayerType.COMPUTER_HARD

    def __attrs_post_init__(self):
        self.players = [
            core.Player(id=i, type=core.PlayerType.USER)
            for i in range(self.number_of_players)
        ]
        if self.computer:
            self.players[1].type = self.computer_type

    def run(self):
        """Main game loop"""
        self.board.draw()  # empty board

        current_status = core.BoardStatus.IN_PROGRESS
        while current_status == core.BoardStatus.IN_PROGRESS:
            for pl in self.players:
                while True:
                    if pl.type == core.PlayerType.USER:
                        i, j = map(
                            int,
                            input(
                                f"Write a position for a move for the Player {pl.id}: "
                            ).split(","),
                        )
                    else:
                        i, j = self.board.predict_next_position(current_player=pl)

                    position = (i, j)
                    try:
                        self.board.step(
                            position=position,
                            player=pl,
                        )
                        break
                    except IndexError:
                        print("Wrong position. Make a step again.")

                current_status = self.board.check_solution(
                    current_position=position,
                    player=pl,
                )
                self.board.draw(position=position, current_status=current_status)
                if current_status == core.BoardStatus.ENDED:
                    print(f"Player {pl.id} ({pl.type.value}) won!")
                    break
                elif current_status == core.BoardStatus.TIE:
                    print("It's a tie")
                    break
