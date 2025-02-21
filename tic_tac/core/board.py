import random
import enum
import attr
from tic_tac.core import player

class BoardStatus(enum.Enum):
    IN_PROGRESS: str = "IN_PROGRESS"
    ENDED: str = "ENDED"
    TIE: str = "TIE"


@attr.s(auto_attribs=True, kw_only=True)
class Board:
    width: int
    height: int
    board: dict[tuple[int, int], int] = attr.ib(init=False)

    def __attrs_post_init__(self):
        self.board = {}

        # The checking rule for a win streak determination
        # Check the rows, columns and diagonals for the `player` in a clockwise order
        self.solution_directions = [
            [-1, 0], [-1, -1], [0, -1], [1, -1], [1, 0], [1, 1], [0, 1], [-1, 1]
        ]

    def step(self, position: tuple[int, int], player: player.Player):
        """Assign the player position the board"""

        if not self._is_position_in_bounds(position):
            raise IndexError

        self.board[position] = player.id

    def draw(self) -> None:
        """Draw the situation on the board"""
        max_gap_width = len(str(self.width))
        max_gap_height = len(str(self.height))

        print(" " * (max_gap_width), end="")
        for i in range(self.width):
            gap = " " * (max_gap_width + 1 - len(str(i)))
            print(f"{gap}{i}", end="")
        print()

        for i in range(self.height):
            for j in range(self.width):
                if j == 0:
                    gap = " " * (max_gap_width - len(str(i)))
                    print(f"{i}{gap}", end="")
                position = (i, j)
                value = self.board.get(position, "-")
                print(f"{' ' * (max_gap_height)}{value}", end="")
            print()

    def check_solution(self, current_position, player: player.Player, win_length: int) -> BoardStatus:
        """
        Returns `BoardStatus` shows the board situation for the current player.
        """
        # Loop over directions; time complexity - O(win_length)
        for dx, dy in self.solution_directions:
            strick = 0
            i, j = current_position
            for _ in range(win_length):
                if (i, j) not in self.board:
                    break

                if self.board[i, j] == player.id:
                    strick += 1
                    if strick == win_length:
                        return BoardStatus.ENDED

                # Move in direction
                i = i + dx
                j = j + dy

        if len(self.board) == self.width * self.height:
            # no more space; it's a tie
            return BoardStatus.TIE

        return BoardStatus.IN_PROGRESS


    def predict_next_position(self, player: player.Player) -> tuple[int, int]:
        """Get player's positions on the board"""
        current_player_positions = [
            position
            for position, player_id in self.board.items()
            if player.id == player_id
        ]

        # We can check the best streak to all players to prevent the win
        # for the opposite side

        visited_positions = set()
        max_strick = 0
        best_position = self._get_next_available_random_position()
        for position in current_player_positions:
            for dx, dy in self.solution_directions:
                strick = 0
                i, j = position
                if (i, j) not in self.board or (i, j) in visited_positions:
                    break

                visited_positions.add((i, j))
                if self.board[i, j] == player.id:
                    strick += 1

                i = i + dx
                j = j + dy

                if self._is_position_in_bounds((i, j)) and strick > max_strick:
                    max_strick = strick
                    best_position = (i, j)

        return best_position

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




