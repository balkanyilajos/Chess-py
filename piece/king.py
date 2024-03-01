from __future__ import annotations
from typing import TYPE_CHECKING
import pygame
import os

from enums import Players
from piece.piece import Piece

if TYPE_CHECKING:
     from chess import Chess

class King(Piece):
    def __init__(self, chess: Chess, x: int, y: int, player: Players, image: pygame.Surface):
        super().__init__(chess, x, y, player, image)

    def _getAdjacentCoords(self) -> list[tuple[int,int]]:
        return [(1+self._x, 0+self._y), (-1+self._x, 0+self._y), (0+self._x, 1+self._y), (0+self._x, -1+self._y),
                (1+self._x, 1+self._y), (-1+self._x, -1+self._y), (1+self._x, -1+self._y), (-1+self._x, 1+self._y)]

    def getMoveablePositions(self) -> list[tuple[int, int]]:
        coords = self._getAdjacentCoords()
        counter = 0
        for x, y in reversed(coords):
            isKingAddedToBoard = False
            if self._chess.isValidCoordinate(x, y):
                if self._chess.isTableCellEmpty(x, y):
                    self._chess.addPieceToTable(King(self._chess, x, y, self._player, self._image), x, y, modifyCoordsInPiece=False)
                    isKingAddedToBoard = True
            else:
                coords.remove((x,y))
                continue
                
            #print(self._chess.isTableCellEmpty(x,y), x, y)
            for piece in self._chess.getBoardGenerator():
                if isinstance(piece, King):
                    if not self._chess.isPieceOfPlayer(piece.player) and \
                    abs(piece.x-x) == 0 and abs(piece.y-y) == 0:
                        coords.remove((x, y))
                else:
                    if self._chess.isPieceOfPlayer(piece.player):
                        if abs(piece.x-x) == 0 and abs(piece.y-y) == 0:
                            coords.remove((x, y))
                    elif piece.isMoveable(x, y):
                        coords.remove((x, y))
            
            if isKingAddedToBoard:
                self._chess.deletePieceFromTable(x, y)
                counter += 1

        # for cell in self._chess.getBoardGenerator():
        #     if isinstance(cell, King) and not self._chess.isPieceOfPlayer(cell.player):
        #             coords -= cell._getAdjacentCoords()
        #     elif isinstance(cell, Piece):
        #         if self._chess.isPieceOfPlayer(cell.player):
        #             coords.discard((cell.x, cell.y))
        #         else:
        #             for coord in cell.getMoveablePositions():
        #                 coords.discard(coord) 

        return coords

class BlackKing(King):
    def __init__(self, chess: Chess, x: int, y: int, size: int):
        super().__init__(chess, x, y, Players.BLACK, pygame.transform.smoothscale(pygame.image.load(os.path.join("data", "black_king.svg")), (size, size)) )

class WhiteKing(King):
    def __init__(self, chess: Chess, x: int, y: int, size: int):
        super().__init__(chess, x, y, Players.WHITE, pygame.transform.smoothscale(pygame.image.load(os.path.join("data", "white_king.svg")), (size, size)) )
