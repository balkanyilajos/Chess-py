from win32api import GetSystemMetrics
from typing import Generator
import pygame
from enums import Players, GameStates
from piece import *

class Chess:
    def __init__(self):
        pygame.init()
        self._clock = pygame.time.Clock()
        self._running: bool = True
        self._actualPlayer: Players = Players.WHITE
        self._board = Board(8, 8)
        self._gui = GUI(self, self._board)
        self._kings: dict = None
        self._gameState = GameStates.NONE
        self._winner = Players.NONE

        self._start()

    @property
    def actualPlayer(self) -> Players:
        return self._actualPlayer

    @property
    def winner(self) -> Players:
        return self._winner

    @property
    def gameState(self) -> GameStates:
        return self._gameState

    def _start(self):
        self._createPieces()
        self._kings = self._getKings()

        while self._running:
            for event in pygame.event.get():
                self._update(event)
            self._gui.refresh()
            #print(self._gameState, self._winner)
        pygame.quit()

    def _update(self, event: pygame.event.Event):
        if event.type == pygame.QUIT:
            self._running = False
            return
                    
        if event.type == pygame.MOUSEBUTTONDOWN:
            coordinate = self._gui.getIndexFromCoordinate(*pygame.mouse.get_pos())
            indexX, indexY = coordinate

            if not self._board.isTableCellEmpty(*coordinate):
                piece = self._board.getBoardPiece(indexX, indexY)
                if piece.canMove and self.isRoundOfCurrentPlayer(piece.player):
                    self._gui.activePiece = self._board.deletePieceFromTable(*coordinate)
                    self._gui.showMousePiece = True

        if event.type == pygame.MOUSEBUTTONUP:
            x, y = self._gui.getIndexFromCoordinate(*pygame.mouse.get_pos())
            if self._gui.activePiece is not None and self.isRoundOfCurrentPlayer(self._gui.activePiece.player):
                if self._gui.activePiece.isMoveable(x, y):
                    self._gui.showValidMoves = False
                    self._board.deletePieceFromTable(self._gui.activePiece.x, self._gui.activePiece.y)
                    self._board.addPieceToTable(self._gui.activePiece, x, y)
                    self._setGameState()
                    print(self._gameState, self._winner)
                    self._actualPlayer = Players.getNextPlayer(self._actualPlayer)
                    self._setPieceMovability()
                else:
                    if self._gui.activePiece.hasSamePosition(x, y):
                        self._gui.showValidMoves = not self._gui.showValidMoves
                    self._board.addPieceToTable(self._gui.activePiece)

            self._gui.showMousePiece = False

    def _createPieces(self):

        blackSpecialPieces = [rook.BlackRook, knight.BlackKnight, bishop.BlackBishop, king.BlackKing, \
                              queen.BlackQueen, bishop.BlackBishop, knight.BlackKnight, rook.BlackRook]
        whiteSpecialPieces = [rook.WhiteRook, knight.WhiteKnight, bishop.WhiteBishop, king.WhiteKing, \
                              queen.WhiteQueen, bishop.WhiteBishop, knight.WhiteKnight, rook.WhiteRook]

        for i in range(self._board.WIDTH):
            self._board.addPieceToTable(blackSpecialPieces[i](self._board, i, 0, self._gui.CUBE_SIZE), modifyCoordsInPiece=False)
            self._board.addPieceToTable(pawn.BlackPawn(self._board, i, 1, self._gui.CUBE_SIZE), modifyCoordsInPiece=False)
            self._board.addPieceToTable(pawn.WhitePawn(self._board, i, self._board.HEIGHT-2, self._gui.CUBE_SIZE), modifyCoordsInPiece=False) 
            self._board.addPieceToTable(whiteSpecialPieces[i](self._board, i, self._board.HEIGHT-1, self._gui.CUBE_SIZE), modifyCoordsInPiece=False)

    def isRoundOfCurrentPlayer(self, otherPlayer: Players):
        return otherPlayer == self._actualPlayer

    def _getKings(self) -> set[king.King]:
        kings = dict()
        for piece in self._board.getPieceGenerator():
            if isinstance(piece, king.King):
                kings[piece.player] = piece
        
        return kings

    def _setGameState(self) -> GameStates:
        nextKing: king.King = self._kings[Players.getNextPlayer(self._actualPlayer)]
        
        if self._isCheck(nextKing):
            self._gameState = GameStates.CHECK
            if self._isCheckMate(nextKing):
                self._gameState = GameStates.CHECKMATE
                self._winner = Players.getNextPlayer(self._actualPlayer) 
        
        if self._isStaleMate():
            self._gameState = GameStates.STALEMATE
        
    def _isCheck(self, kingPiece: king.King):
        for piece in self._board.getPieceGenerator():
            if not isinstance(piece, king.King) and not kingPiece.isOwnedBySamePlayer(piece) \
                and piece.isMoveable(kingPiece.x, kingPiece.y):
                return True
        
        return False

    def _isCheckMate(self, kingPiece: king.King) -> bool:
        if len(kingPiece.getMoveablePositions()) != 0:
            return False
        
        for piece in self._board.getPieceGenerator():
            if kingPiece.isOwnedBySamePlayer(piece) and not isinstance(piece, king.King):
                self._board.deletePieceFromTable(piece.x, piece.y)
                originalPieceX = piece.x
                originalPieceY = piece.y
                isInCheckMate = True
                for x, y in piece.getMoveablePositions():
                    deletedPiece = self._board.deletePieceFromTable(x, y)
                    self._board.addPieceToTable(piece, x, y, modifyCoordsInPiece=True)

                    isInCheckMate = self._isCheck(kingPiece)
                    self._board.addPieceToTable(deletedPiece, x, y, modifyCoordsInPiece=False)
                    if not isInCheckMate:
                        break
                
                self._board.addPieceToTable(piece, originalPieceX, originalPieceY, modifyCoordsInPiece=True)
                if not isInCheckMate:
                    return False
        
        return True

    def _isStaleMate(self):
        for piece in self._board.getPieceGenerator():
            if self.isRoundOfCurrentPlayer(piece.player) and piece.canMove:
                return True
        
        return False

    def _setPieceMovability(self):
        actualKing: king.King = self._kings[self._actualPlayer]

        for piece in self._board.getPieceGenerator():
            if not GameStates.isEndOfGame(self._gameState) and self.isRoundOfCurrentPlayer(piece.player):
                if not isinstance(piece, king.King) and self._isCheck(actualKing):
                    self._board.deletePieceFromTable(piece.x, piece.y)
                    originalPieceX = piece.x
                    originalPieceY = piece.y
                    pieceCanMove = False
                    for x, y in piece.getMoveablePositions():
                        deletedPiece = self._board.deletePieceFromTable(x, y)
                        self._board.addPieceToTable(piece, x, y, modifyCoordsInPiece=True)
                        pieceCanMove = not self._isCheck(actualKing)
                        self._board.addPieceToTable(deletedPiece, x, y, modifyCoordsInPiece=False)
                        if pieceCanMove:
                            break
                        
                    self._board.addPieceToTable(piece, originalPieceX, originalPieceY, modifyCoordsInPiece=True)
                    piece.canMove = pieceCanMove
                else:
                    piece.canMove = True                 

    def _isStaleMate(self):
        for piece in self._board.getPieceGenerator():
            if self.isRoundOfCurrentPlayer(piece.player) and piece.canMove:
                return False
        
        return True

class Board:

    def __init__(self, width: int, height: int):
        self.WIDTH = width
        self.HEIGHT = height
        self._emptyCell = None
        self.board: piece.Piece = [[self._emptyCell for x in range(width)] \
                                     for y in range(height)]

    @property
    def emptyCell(self) -> None:
        return self._emptyCell

    def isTableCellEmpty(self, indexX: int, indexY: int) -> bool:
        return self.getBoardPiece(indexX, indexY) == None
    
    def isValidCoordinate(self, indexX: int, indexY: int) -> bool:
        return indexX >= 0 and indexX < self.WIDTH \
               and indexY >= 0 and indexY < self.HEIGHT

    def deletePieceFromTable(self, indexX: int, indexY: int) -> piece.Piece:
        temp = self.getBoardPiece(indexX, indexY)
        self.board[indexY][indexX] = self._emptyCell
        return temp

    def addPieceToTable(self, piece: piece.Piece, indexX: int = None, indexY: int = None, modifyCoordsInPiece: bool = True):
        if indexX == None or indexY == None:
            indexX = piece.x
            indexY = piece.y
        self.board[indexY][indexX] = piece
        if modifyCoordsInPiece:
            self.board[indexY][indexX].x = indexX
            self.board[indexY][indexX].y = indexY

    def getPieceGenerator(self) -> Generator[piece.Piece, None, None]:
        for row in self.board:
            for cell in row:
                if isinstance(cell, piece.Piece):
                    yield cell

    def getBoardPiece(self, indexX, indexY) -> piece.Piece:
        return self.board[indexY][indexX]


class GUI:
    CUBE_COLOR_1 = pygame.Color(109, 82, 73, 255)
    CUBE_COLOR_2 = pygame.Color(248, 243, 227, 255)
    VALID_MOVE_COLOR = pygame.Color(158, 158, 158, 200)
    EMPTY_COLOR = pygame.Color(0, 0, 0, 0)

    def __init__(self, chess: Chess, board: Board):
        size = int(GetSystemMetrics(0) * 0.6) if GetSystemMetrics(0) < GetSystemMetrics(1) else int(GetSystemMetrics(1) * 0.6)
        self._chess = chess
        self._board = board
        self.CUBE_SIZE = int(size / board.WIDTH)
        self.SCREEN_WIDTH = self.CUBE_SIZE * self._board.WIDTH
        self.SCREEN_HEIGHT = self.CUBE_SIZE * self._board.HEIGHT

        screenSize = (board.WIDTH * self.CUBE_SIZE, board.HEIGHT * self.CUBE_SIZE)
        self.screen = pygame.display.set_mode(screenSize)
        self.boardSurface = pygame.Surface(screenSize)
        self.validMoveSurface = pygame.Surface(screenSize, pygame.SRCALPHA)
        self.mouseSurface = pygame.Surface(screenSize, pygame.SRCALPHA)

        self.showValidMoves: bool = False
        self.showMousePiece: bool = False
        self.activePiece: piece.Piece = None

    def refresh(self):
        self.screen.fill(self.EMPTY_COLOR)
        self.boardSurface.fill(self.EMPTY_COLOR)
        self.mouseSurface.fill(self.EMPTY_COLOR)
        if self.showValidMoves:
            self._drawValidMoves(self.activePiece)
        else:
            self.validMoveSurface.fill(self.EMPTY_COLOR)

        self._createBackground()
        self._drawPieces()
        if self.showMousePiece:
            self._drawGrabbedByMousePiece()

        self.boardSurface.blit(self.validMoveSurface, (0, 0))
        self.boardSurface.blit(self.mouseSurface, (0, 0))
        self.screen.blit(self.boardSurface, (0, 0))
        pygame.display.update()
        pygame.display.flip()

    def _createBackground(self):
        player = self._chess.actualPlayer
        for y in range(0, self.SCREEN_HEIGHT, self.CUBE_SIZE):
            for x in range (0, self.SCREEN_WIDTH, self.CUBE_SIZE):
                color = self.CUBE_COLOR_1 if player == Players.WHITE else self.CUBE_COLOR_2
                player = Players.getNextPlayer(player)

                pygame.draw.rect(self.boardSurface, color, (x, y, self.CUBE_SIZE, self.CUBE_SIZE))
            player = Players.getNextPlayer(player)

    def _drawPieces(self):
        iterator = range(self._board.HEIGHT) if self._chess.isRoundOfCurrentPlayer(Players.WHITE) else range(self._board.HEIGHT-1, -1, -1)
        for y in iterator:
            for x in range(self._board.WIDTH):
                if(not self._board.isTableCellEmpty(x, y)):
                    ySize = y*self.CUBE_SIZE if self._chess.isRoundOfCurrentPlayer(Players.WHITE) else (self._board.HEIGHT-y-1)*self.CUBE_SIZE
                    self.boardSurface.blit(self._board.getBoardPiece(x, y).image, (x*self.CUBE_SIZE, ySize))

    def _drawValidMoves(self, piece: piece.Piece):
        points = piece.getMoveablePositions()
        for point in points:
            x, y = self.getCoordinatesFromIndex(*point)
            pygame.draw.rect(self.validMoveSurface, self.VALID_MOVE_COLOR, (x, y, self.CUBE_SIZE, self.CUBE_SIZE))

    def _drawGrabbedByMousePiece(self):
        x, y = pygame.mouse.get_pos()
        self.mouseSurface.blit(self.activePiece.image, (x - self.CUBE_SIZE / 2, y - self.CUBE_SIZE / 2))

    def getIndexFromCoordinate(self, x: float, y: float) -> tuple[int, int]:
        if self._chess.isRoundOfCurrentPlayer(Players.WHITE):
            yIndex = int(y / self.CUBE_SIZE)
        else:
            yIndex = self._board.HEIGHT - int(y / self.CUBE_SIZE) - 1
        return (int(x / self.CUBE_SIZE), yIndex)

    def getCoordinatesFromIndex(self, indexX: int, indexY: int) -> tuple[float, float]:
        if self._chess.isRoundOfCurrentPlayer(Players.WHITE):
            y = indexY * self.CUBE_SIZE
        else:
            y = (self._board.HEIGHT-1 - indexY) * self.CUBE_SIZE
        return (indexX * self.CUBE_SIZE, y)

