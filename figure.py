from enums import Players, Pieces
from pygame import Surface

class Figure:
    def __init__(self, player: Players, piece: Pieces, image: Surface) -> None:
        self.player = player
        self.piece = piece
        self.image = image
