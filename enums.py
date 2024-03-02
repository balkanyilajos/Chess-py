from __future__ import annotations
from enum import unique, Enum

@unique
class GameStates(Enum):
    NONE = 0
    CHECK = 1
    STALEMATE = 2
    CHECKMATE = 3

    @classmethod
    def isEndOfGame(self, state: GameStates) -> bool:
        return state == self.CHECKMATE or self == self.STALEMATE


@unique
class Players(Enum):
    NONE = 0
    WHITE = 1
    BLACK = 2

    @classmethod
    def getNextPlayer(self, player: Players) -> Players:
        if player == self.WHITE:
            return self.BLACK
        else:
            return self.WHITE