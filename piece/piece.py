from enums import Players
from pygame import Surface
from abc import  ABC, abstractmethod

class Piece(ABC):
    def __init__(self, table, x: int, y: int, player: Players, image: Surface) -> None:
        self._table = table
        self._x = x
        self._y = y
        self._player = player
        self._image = image

    @property
    def player(self) -> Players:
        return self._player
    
    @property
    def image(self) -> Surface:
        return self._image

    def isPieceInTheSamePosition(self, other: "Piece"):
        return self._x == other._x and self._y == other._y

    def isPieceInTheSamePosition(self, indexX, indexY):
        return self._x == indexX and self._y == indexY

    @abstractmethod
    def move(self, indexX: int, indexY: int) -> bool:
        pass
