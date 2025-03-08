import collections
import random
import enum
import attr
from tic_tac.core import player as pl
from tic_tac.core import utils


class BoardStatus(enum.Enum):
    IN_PROGRESS: str = "IN_PROGRESS"
    ENDED: str = "ENDED"
    TIE: str = "TIE"


@attr.s(auto_attribs=True, kw_only=True)
class PlayerBoardScore:
    best_direction: tuple[int, int]
    best_position: tuple[int, int]
    streak: int


@attr.s(auto_attribs=True, kw_only=True)
class Board:
    width: int
    height: int
    win_length: int
    board: dict[tuple[int, int], int] = attr.ib(init=False)

    def __attrs_post_init__(self) -> None:
        self.board = {}
        self.best_direction = (0, 0)

        # The checking rule for a win streak determination
        # Check the rows, columns and diagonals for the `player` in a clockwise order
        self.solution_directions = [
            [-1, 0],
            [-1, -1],
            [0, -1],
            [1, -1],
            [1, 0],
            [1, 1],
            [0, 1],
            [-1, 1],
        ]

    def step(self, position: tuple[int, int], player: pl.Player) -> None:
        """Assign the player position the board"""

        if not self._is_position_in_bounds(position):
            raise IndexError

        self.board[position] = player.id

    def draw(
        self,
        position: tuple[int, int] | None = None,
        current_status: BoardStatus = BoardStatus.IN_PROGRESS,
    ) -> None:
        """Draw the situation on the board"""

        max_gap_width = len(str(self.width))
        max_gap_height = len(str(self.height))

        # Draw the header row with indices
        print(" " * (max_gap_width), end="")
        for i in range(self.width):
            gap = " " * (max_gap_width + 1 - len(str(i)))
            print(f"{gap}{i}", end="")
        print()

        # Save win indices for future highlight
        win_indices = set()
        if current_status == BoardStatus.ENDED:
            dx, dy = self.best_direction
            i, j = position
            for k in range(self.win_length):
                win_indices.add((i, j))
                i += dx
                j += dy

        for i in range(self.height):
            for j in range(self.width):
                if j == 0:
                    gap = " " * (max_gap_width - len(str(i)))
                    print(f"{i}{gap}", end="")
                position = (i, j)
                value = self.board.get(position, "-")
                cell_str = f"{' ' * (max_gap_height)}{value}"
                if (i, j) in win_indices:
                    # draw the win sub array
                    print(utils.color_text(text=cell_str, color="red"), end="")
                else:
                    print(utils.color_text(text=cell_str, color="yellow"), end="")

            print()

    def check_solution(
        self, current_position: tuple[int, int], player: pl.Player
    ) -> BoardStatus:
        """
        Returns `BoardStatus` shows the board situation for the current player.
        """

        # Loop over directions; time complexity - O(win_length)
        for dx, dy in self.solution_directions:
            streak = 0
            i, j = current_position
            for _ in range(self.win_length):
                if (i, j) not in self.board:
                    break

                if self.board[i, j] == player.id:
                    streak += 1
                    if streak == self.win_length:

                        # save win direction
                        self.best_direction = (dx, dy)
                        return BoardStatus.ENDED

                # Move in direction
                i = i + dx
                j = j + dy

        if len(self.board) == self.width * self.height:
            # No more space on the board; it's a tie
            return BoardStatus.TIE

        return BoardStatus.IN_PROGRESS

    def predict_next_position(self, current_player: pl.Player) -> tuple[int, int]:
        """Get player's positions on the board"""

        player_positions = collections.defaultdict(list)
        for position, player_id in self.board.items():
            player_positions[player_id].append(position)

        if current_player.type == pl.PlayerType.COMPUTER_EASY:
            current_player_score = self._get_player_best_positions(
                player_id=current_player.id,
                player_positions=player_positions[current_player.id],
            )
            return current_player_score.best_position

        player_scores = {
            player_id: self._get_player_best_positions(
                player_id=player_id,
                player_positions=player_positions[player_id],
            )
            for player_id in player_positions
        }
        players_scores_by_streak = sorted(
            player_scores.values(), key=lambda x: x.streak
        )
        current_player_score = player_scores.get(current_player.id)
        #  Check the best streak to all players to prevent the win for the opposite side
        if (
            current_player_score is not None
            and current_player_score.streak > players_scores_by_streak[-1].streak
        ):
            return current_player_score.best_position
        else:
            return players_scores_by_streak[-1].best_position

    def _get_player_best_positions(
        self, player_id: int, player_positions: list[tuple[int, int]]
    ) -> PlayerBoardScore:
        """
        Returns `PlayerBoardScore` that contains the best possible score/position/direction
        for a `player_id` and specified `player_positions`
        """

        max_strick = 0
        best_position = self._get_next_available_random_position()
        best_direction = self.solution_directions[0]
        for position in player_positions:
            # TODO we can skip already visited positions
            for dx, dy in self.solution_directions:
                streak = 0
                i, j = position
                for _ in range(self.win_length):
                    if (i, j) not in self.board:
                        break

                    if self.board[i, j] == player_id:
                        streak += 1

                    i = i + dx
                    j = j + dy

                    if self._is_position_in_bounds((i, j)) and streak > max_strick:
                        max_strick = streak
                        best_position = (i, j)
                        best_direction = (dx, dy)

        return PlayerBoardScore(
            best_position=best_position,
            best_direction=best_direction,
            streak=max_strick,
        )

    def _is_position_in_bounds(self, position: tuple[int, int]) -> bool:
        """Returns True if the `position` is valid for the current board"""
        i, j = position
        return 0 <= i < self.height and 0 <= j < self.width and (i, j) not in self.board

    def _get_next_available_random_position(self) -> tuple[int, int]:
        """Returns random available position `(i, j)` on the board"""
        i, j = random.randint(0, self.height - 1), random.randint(0, self.width - 1)
        while not self._is_position_in_bounds((i, j)) or (i, j) in self.board:
            i, j = random.randint(0, self.height - 1), random.randint(0, self.width - 1)

        return i, j
