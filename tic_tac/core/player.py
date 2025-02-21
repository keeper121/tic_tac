import enum
import attr

class PlayerType(enum.Enum):
    COMPUTER: str = "COMPUTER"
    USER: str = "USER"

@attr.s(auto_attribs=True, kw_only=True)
class Player:
    id: int
    type: PlayerType

