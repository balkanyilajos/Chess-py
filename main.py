from win32api import GetSystemMetrics
import pygame
from enums import Players
from piece import *

class Chess:
    SIZE = int(GetSystemMetrics(0) * 0.6) if GetSystemMetrics(0) < GetSystemMetrics(1) else int(GetSystemMetrics(1) * 0.6)
    NUMBER_OF_CUBES_IN_A_ROW = 8
    NUMBER_OF_CUBES_IN_A_COLUMN = 8

    CUBE_SIZE = int(SIZE / NUMBER_OF_CUBES_IN_A_ROW)
    CUBE_COLOR_1 = (109, 82, 73)
    CUBE_COLOR_2 = (248, 243, 227)

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.SIZE, self.SIZE))
        self.clock = pygame.time.Clock()
        self.running: bool = True

        self.board: piece.Piece = [[None for x in range(self.NUMBER_OF_CUBES_IN_A_ROW)] \
                                     for y in range(self.NUMBER_OF_CUBES_IN_A_COLUMN)]
        self.activePiece: piece.Piece = None
        self.actualPlayer: Players = Players.WHITE

        self.start()

    def start(self):
        self.createFigures()

        while self.running:
            for event in pygame.event.get():
                self.update(event)
            self.draw()
            
        pygame.quit()

    def update(self, event: pygame.event.Event):
        if event.type == pygame.QUIT:
            self.running = False
            return
                    
        if event.type == pygame.MOUSEBUTTONDOWN:
            coordinate = self.getIndexFromCoordinate(*pygame.mouse.get_pos())
            indexX, indexY = coordinate
            if(not self.isTableCellEmpty(*coordinate)
            and self.isPieceOfPlayer(self.board[indexY][indexX])):
                self.activePiece = self.deleteFigureFromTable(*coordinate)
                self.activePieceCoordinate = coordinate          

        if event.type == pygame.MOUSEBUTTONUP and self.activePiece != None:
            coordinate = self.getIndexFromCoordinate(*pygame.mouse.get_pos())
            if(self.isTableCellEmpty(*coordinate)
            and not self.activePiece.isPieceInTheSamePosition(*coordinate)):
                self.addFigureToTable(self.activePiece, *coordinate)
                self.actualPlayer = Players.getNextPlayer(self.actualPlayer)
            else:
                self.addFigureToTable(self.activePiece, *self.activePieceCoordinate)
                    
            self.activePiece = None
            self.activePieceCoordinate = None

        pygame.display.update()
        pygame.display.flip()

    def draw(self):
        self.createBackground()
        self.drawFigures()

        if self.activePiece != None:
            self.drawGrabbedByMousePiece()

    def createBackground(self):
        player = self.actualPlayer
        for y in range(0, self.SIZE, self.CUBE_SIZE):
            for x in range (0, self.SIZE, self.CUBE_SIZE):
                color = self.CUBE_COLOR_1 if player == Players.WHITE else self.CUBE_COLOR_2
                player = Players.getNextPlayer(player)

                pygame.draw.rect(self.screen, color, (x, y, self.CUBE_SIZE, self.CUBE_SIZE))
            player = Players.getNextPlayer(player)

    def createFigures(self):

        blackSpecialPieces = [rook.BlackRook, knight.BlackKnight, bishop.BlackBishop, king.BlackKing, \
                              queen.BlackQueen, bishop.BlackBishop, knight.BlackKnight, rook.BlackRook]
        whiteSpecialPieces = [rook.WhiteRook, knight.WhiteKnight, bishop.WhiteBishop, king.WhiteKing, \
                              queen.WhiteQueen, bishop.WhiteBishop, knight.WhiteKnight, rook.WhiteRook]

        for i in range(self.NUMBER_OF_CUBES_IN_A_ROW):
            self.board[0][i] = blackSpecialPieces[i](self.board, i, 0, self.CUBE_SIZE)
            self.board[1][i] = pawn.BlackPawn(self.board, i, 1, self.CUBE_SIZE)
            self.board[self.NUMBER_OF_CUBES_IN_A_COLUMN-2][i] = pawn.WhitePawn(self.board, i, self.NUMBER_OF_CUBES_IN_A_COLUMN-2, self.CUBE_SIZE)
            self.board[self.NUMBER_OF_CUBES_IN_A_COLUMN-1][i] = whiteSpecialPieces[i](self.board, i, self.NUMBER_OF_CUBES_IN_A_COLUMN-1, self.CUBE_SIZE)

    def isTableCellEmpty(self, indexX: int, indexY: int) -> bool:
        return self.board[indexY][indexX] == None

    def isPieceOfPlayer(self, otherPlayer: Players):
        return otherPlayer.player == self.actualPlayer

    def deleteFigureFromTable(self, indexX: int, indexY: int) -> piece.Piece:
        temp = self.board[indexY][indexX]
        self.board[indexY][indexX] = None
        return temp

    def addFigureToTable(self, piece: piece.Piece, indexX: int, indexY: int) -> piece.Piece:
        self.board[indexY][indexX] = piece

    def getIndexFromCoordinate(self, x: float, y: float) -> tuple[int, int]:
        yIndex = int(y / self.CUBE_SIZE) if self.actualPlayer == Players.WHITE else self.NUMBER_OF_CUBES_IN_A_ROW - int(y / self.CUBE_SIZE) - 1
        return (int(x / self.CUBE_SIZE), yIndex)

    def drawFigures(self):
        iterator = range(self.NUMBER_OF_CUBES_IN_A_ROW) if self.actualPlayer == Players.WHITE else range(self.NUMBER_OF_CUBES_IN_A_ROW-1, -1, -1)
        for y in iterator:
            for x in range(self.NUMBER_OF_CUBES_IN_A_COLUMN):
                if(self.board[y][x] != None):
                    ySize = y*self.CUBE_SIZE if self.actualPlayer == Players.WHITE else (self.NUMBER_OF_CUBES_IN_A_ROW-y-1)*self.CUBE_SIZE
                    self.screen.blit(self.board[y][x].image, (x*self.CUBE_SIZE, ySize))

    def drawGrabbedByMousePiece(self):
        x, y = pygame.mouse.get_pos()
        self.screen.blit(self.activePiece.image, (x - self.CUBE_SIZE / 2, y - self.CUBE_SIZE / 2))


def main():
    Chess()

if __name__ == "__main__":
    main()