from enum import unique, Enum

@unique
class Pieces(Enum):
    PAWN = (1, 1)
    BISHOP = (2, 3)
    KNIGHT = (3, 3)
    ROOK = (4, 5)
    QUEEN = (5, 9)
    KING = (6, 100)

@unique
class Players(Enum):
    PLAYER_1 = 1
    PLAYER_2 = 2

    @classmethod
    def getNextPlayer(self, player: int) -> int:
        if player == self.PLAYER_1:
            return self.PLAYER_2
        else:
            return self.PLAYER_1