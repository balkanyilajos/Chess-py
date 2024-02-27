from win32api import GetSystemMetrics
import pygame
from enums import Players
from piece import *

class Chess:
    SIZE = int(GetSystemMetrics(0) * 0.6) if GetSystemMetrics(0) < GetSystemMetrics(1) else int(GetSystemMetrics(1) * 0.6)
    NUMBER_OF_CUBES_IN_A_ROW = 8
    NUMBER_OF_CUBES_IN_A_COLUMN = 8

    CUBE_SIZE = int(SIZE / NUMBER_OF_CUBES_IN_A_ROW)
    CUBE_COLOR_1 = pygame.Color(109, 82, 73, 255)
    CUBE_COLOR_2 = pygame.Color(248, 243, 227, 255)
    VALID_MOVE_COLOR = pygame.Color(158, 158, 158, 200)

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.SIZE, self.SIZE))
        self.boardSurface = pygame.Surface((self.SIZE, self.SIZE))

        self.validMoveSurface = pygame.Surface((self.SIZE, self.SIZE), pygame.SRCALPHA)
        self.mouseSurface = pygame.Surface((self.SIZE, self.SIZE), pygame.SRCALPHA)

        self.clock = pygame.time.Clock()
        self.running: bool = True

        self.board: piece.Piece = [[None for x in range(self.NUMBER_OF_CUBES_IN_A_ROW)] \
                                     for y in range(self.NUMBER_OF_CUBES_IN_A_COLUMN)]
        self.activePiece: piece.Piece = None
        self.actualPlayer: Players = Players.WHITE
        self.showValidMoves: bool = False

        self._start()

    def _start(self):
        self._createPieces()

        while self.running:
            for event in pygame.event.get():
                self._update(event)
            self._draw() 
        pygame.quit()

    def _update(self, event: pygame.event.Event):
        if event.type == pygame.QUIT:
            self.running = False
            return
                    
        if event.type == pygame.MOUSEBUTTONDOWN:
            coordinate = self._getIndexFromCoordinate(*pygame.mouse.get_pos())
            indexX, indexY = coordinate
            if(not self.isTableCellEmpty(*coordinate)
            and self.isPieceOfPlayer(self.getBoardPiece(indexX, indexY))):
                self.activePiece = self.deletePieceFromTable(*coordinate)         

        if event.type == pygame.MOUSEBUTTONUP and self.activePiece != None:
            coordinate = self._getIndexFromCoordinate(*pygame.mouse.get_pos())
            if(self.activePiece.isMoveable(*coordinate)):
                self.showValidMoves = False
                self.addPieceToTable(self.activePiece, *coordinate)
                self.actualPlayer = Players.getNextPlayer(self.actualPlayer)
            else:
                self.showValidMoves = True
                self.validMoveSurface.fill((0,0,0,0))
                self.addPieceToTable(self.activePiece)
                self._drawValidMoves(self.activePiece)
                    
            self.activePiece = None

    def _draw(self):
        if not self.showValidMoves:
            self.validMoveSurface.fill((0,0,0,0))
        self.screen.fill((0,0,0,0))
        self.mouseSurface.fill((0,0,0,0))

        self._createBackground()
        self._drawPieces()

        if self.activePiece != None:
            self._drawGrabbedByMousePiece()

        self.boardSurface.blit(self.validMoveSurface, (0, 0))
        self.boardSurface.blit(self.mouseSurface, (0, 0))
        self.screen.blit(self.boardSurface, (0, 0))
        pygame.display.update()
        pygame.display.flip()

    def _createBackground(self):
        player = self.actualPlayer
        for y in range(0, self.SIZE, self.CUBE_SIZE):
            for x in range (0, self.SIZE, self.CUBE_SIZE):
                color = self.CUBE_COLOR_1 if player == Players.WHITE else self.CUBE_COLOR_2
                player = Players.getNextPlayer(player)

                pygame.draw.rect(self.boardSurface, color, (x, y, self.CUBE_SIZE, self.CUBE_SIZE))
            player = Players.getNextPlayer(player)

    def _createPieces(self):

        blackSpecialPieces = [rook.BlackRook, knight.BlackKnight, bishop.BlackBishop, king.BlackKing, \
                              queen.BlackQueen, bishop.BlackBishop, knight.BlackKnight, rook.BlackRook]
        whiteSpecialPieces = [rook.WhiteRook, knight.WhiteKnight, bishop.WhiteBishop, king.WhiteKing, \
                              queen.WhiteQueen, bishop.WhiteBishop, knight.WhiteKnight, rook.WhiteRook]

        for i in range(self.NUMBER_OF_CUBES_IN_A_ROW):
            self.addPieceToTable(blackSpecialPieces[i](self, i, 0, self.CUBE_SIZE), i, 0)
            self.addPieceToTable(pawn.BlackPawn(self, i, 1, self.CUBE_SIZE), i, 1)
            self.addPieceToTable(pawn.WhitePawn(self, i, self.NUMBER_OF_CUBES_IN_A_COLUMN-2, self.CUBE_SIZE), i, self.NUMBER_OF_CUBES_IN_A_COLUMN-2) 
            self.addPieceToTable(whiteSpecialPieces[i](self, i, self.NUMBER_OF_CUBES_IN_A_COLUMN-1, self.CUBE_SIZE), i, self.NUMBER_OF_CUBES_IN_A_COLUMN-1)

    def isTableCellEmpty(self, indexX: int, indexY: int) -> bool:
        return self.getBoardPiece(indexX, indexY) == None

    def isPieceOfPlayer(self, otherPlayer: piece.Piece):
        return otherPlayer.player == self.actualPlayer

    def isMovingForward(self, piece: piece.Piece, indexY: int) -> bool:
        return piece.y > indexY if piece.player == Players.WHITE else piece.y < indexY

    def isValidCoordinate(self, indexX: int, indexY: int) -> bool:
        return indexX >= 0 and indexX < self.NUMBER_OF_CUBES_IN_A_ROW \
               and indexY >= 0 and indexY < self.NUMBER_OF_CUBES_IN_A_COLUMN

    def deletePieceFromTable(self, indexX: int, indexY: int) -> piece.Piece:
        temp = self.getBoardPiece(indexX, indexY)
        self.board[indexY][indexX] = None
        return temp

    def addPieceToTable(self, piece: piece.Piece, indexX: int = None, indexY: int = None):
        if indexX == None or indexY == None:
            indexX = piece.x
            indexY = piece.y

        self.board[indexY][indexX] = piece
        self.board[indexY][indexX].x = indexX
        self.board[indexY][indexX].y = indexY

    def _getIndexFromCoordinate(self, x: float, y: float) -> tuple[int, int]:
        if self.actualPlayer == Players.WHITE:
            yIndex = int(y / self.CUBE_SIZE)
        else:
            yIndex = self.NUMBER_OF_CUBES_IN_A_ROW - int(y / self.CUBE_SIZE) - 1
        return (int(x / self.CUBE_SIZE), yIndex)

    def getBoardPiece(self, indexX, indexY) -> piece.Piece:
        return self.board[indexY][indexX]

    def _getCoordinatesFromIndex(self, indexX: int, indexY: int) -> tuple[float, float]:
        if self.actualPlayer == Players.BLACK:
            y = (self.NUMBER_OF_CUBES_IN_A_COLUMN-1 - indexY) * self.CUBE_SIZE
        else:
            y = indexY * self.CUBE_SIZE
        return (indexX * self.CUBE_SIZE, y)

    def _drawPieces(self):
        iterator = range(self.NUMBER_OF_CUBES_IN_A_ROW) if self.actualPlayer == Players.WHITE else range(self.NUMBER_OF_CUBES_IN_A_ROW-1, -1, -1)
        for y in iterator:
            for x in range(self.NUMBER_OF_CUBES_IN_A_COLUMN):
                if(not self.isTableCellEmpty(x, y)):
                    ySize = y*self.CUBE_SIZE if self.actualPlayer == Players.WHITE else (self.NUMBER_OF_CUBES_IN_A_ROW-y-1)*self.CUBE_SIZE
                    self.boardSurface.blit(self.getBoardPiece(x, y).image, (x*self.CUBE_SIZE, ySize))

    def _drawValidMoves(self, piece: piece.Piece):
        points = piece.getMoveablePositions()
        for point in points:
            print(point)
            x, y = self._getCoordinatesFromIndex(*point)
            pygame.draw.rect(self.validMoveSurface, self.VALID_MOVE_COLOR, (x, y, self.CUBE_SIZE, self.CUBE_SIZE))

    def _drawGrabbedByMousePiece(self):
        x, y = pygame.mouse.get_pos()
        self.mouseSurface.blit(self.activePiece.image, (x - self.CUBE_SIZE / 2, y - self.CUBE_SIZE / 2))
