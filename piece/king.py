from __future__ import annotations
from typing import TYPE_CHECKING
import pygame
import os

from enums import Players
from piece.piece import Piece

if TYPE_CHECKING:
     from chess import Board

class King(Piece):
    def __init__(self, board: Board, x: int, y: int, player: Players, image: pygame.Surface):
        super().__init__(board, x, y, player, image)

    def _getAdjacentCoords(self) -> list[tuple[int,int]]:
        return [(1+self._x, 0+self._y), (-1+self._x, 0+self._y), (0+self._x, 1+self._y), (0+self._x, -1+self._y),
                (1+self._x, 1+self._y), (-1+self._x, -1+self._y), (1+self._x, -1+self._y), (-1+self._x, 1+self._y)]

    def getMoveablePositions(self, recalculate:bool = False, _list: list[tuple[int, int]] = None) -> list[tuple[int, int]]:
        if not recalculate:
            return self._moveablePositions

        if _list == None:
            self._moveablePositions = coords = self._getAdjacentCoords()
        else:
            coords = _list

        originalX = self._x
        originalY = self._y
        original = self._board.deletePieceFromTable(originalX, originalY)
        for i in range(len(coords)-1, -1, -1):
            x, y = coords[i]
            isKingAddedToBoard = False
            deletedPiece = None
            # adds the kings to empty cells and checks if it can take off the enemy's pieces
            if self._board.isValidCoordinate(x, y):
                if self._board.isTableCellEmpty(x, y):
                    self._board.addPieceToTable(King(self._board, x, y, self._player, self._image), x, y, testMove=True)
                    isKingAddedToBoard = True
                elif not self.isOwnedBySamePlayer(self._board.getBoardPiece(x, y)) and _list == None:
                    deletedPiece = self._board.deletePieceFromTable(x, y)
                    canMove = (x, y) in self.getMoveablePositions(recalculate=True, _list=coords.copy())
                    self._board.addPieceToTable(deletedPiece, x, y, testMove=True)

                    if not canMove:
                        del coords[i]
                        continue
            else:
                del coords[i]
                continue
            
            #checks if it can be stepped
            for piece in self._board.getPieceGenerator():
                if isinstance(piece, King):
                    if not self.isOwnedBySamePlayer(piece) and \
                    abs(piece.x-x) <= 1 and abs(piece.y-y) <= 1:
                        del coords[i]
                        break
                else:
                    if self.isOwnedBySamePlayer(piece):
                        if abs(piece.x-x) == 0 and abs(piece.y-y) == 0:
                            del coords[i]
                            break
                    elif piece.isMoveable(x, y, recalculate=True):
                        del coords[i]
                        break

            # removes kings from empty cells
            if isKingAddedToBoard:
                self._board.deletePieceFromTable(x, y)

        self._board.addPieceToTable(original, originalX, originalY, testMove=True)
        return coords

class BlackKing(King):
    def __init__(self, board: Board, x: int, y: int, size: int):
        super().__init__(board, x, y, Players.BLACK, pygame.transform.smoothscale(pygame.image.load(os.path.join("data", "black_king.svg")), (size, size)) )

class WhiteKing(King):
    def __init__(self, board: Board, x: int, y: int, size: int):
        super().__init__(board, x, y, Players.WHITE, pygame.transform.smoothscale(pygame.image.load(os.path.join("data", "white_king.svg")), (size, size)) )