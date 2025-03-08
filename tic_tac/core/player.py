import enum
import attr


class PlayerType(enum.Enum):
    COMPUTER_EASY: str = "COMPUTER_EASY"
    COMPUTER_HARD: str = "COMPUTER_HARD"
    USER: str = "USER"


@attr.s(auto_attribs=True, kw_only=True)
class Player:
    id: int
    type: PlayerType
