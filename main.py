from win32api import GetSystemMetrics
import pygame
import os
from enums import Players, Pieces
from figure import Figure

SIZE = int(GetSystemMetrics(0) * 0.6) if GetSystemMetrics(0) < GetSystemMetrics(1) else int(GetSystemMetrics(1) * 0.6)
NUMBER_OF_CUBES_IN_A_ROW = 8
NUMBER_OF_CUBES_IN_A_COLUMN = 8
ONE_CUBE_SIZE = int(SIZE / NUMBER_OF_CUBES_IN_A_ROW)

PLAYER_COLOR_1 = (109, 82, 73)
PLAYER_COLOR_2 = (248, 243, 227)

def createBackground(screen: pygame.Surface, nextPlayer: Players):
    for y in range(0, SIZE, ONE_CUBE_SIZE):
        for x in range (0, SIZE, ONE_CUBE_SIZE):
            color = PLAYER_COLOR_1 if nextPlayer == Players.PLAYER_1 else PLAYER_COLOR_2
            nextPlayer = Players.getNextPlayer(nextPlayer)

            pygame.draw.rect(screen, color, (x, y, ONE_CUBE_SIZE, ONE_CUBE_SIZE))

        nextPlayer = Players.getNextPlayer(nextPlayer)

def createFigures(figuresPosition: Figure, nextPlayer: Players):
    player1PawnPositionY = NUMBER_OF_CUBES_IN_A_ROW - 2 if nextPlayer == Players.PLAYER_1 else 1
    player1SpecialPiecesPositionY = NUMBER_OF_CUBES_IN_A_ROW - 1 if nextPlayer == Players.PLAYER_1 else 0
    player2PawnPositionY = NUMBER_OF_CUBES_IN_A_ROW - 2 if not nextPlayer == Players.PLAYER_1 else 1
    player2SpecialPiecesPositionY = NUMBER_OF_CUBES_IN_A_ROW - 1 if not nextPlayer == Players.PLAYER_1 else 0

    player1Pawn = (Pieces.PAWN, pygame.transform.smoothscale(pygame.image.load(os.path.join("data", "white_pawn.svg")), (ONE_CUBE_SIZE, ONE_CUBE_SIZE)))
    player2Pawn = (Pieces.PAWN, pygame.transform.smoothscale(pygame.image.load(os.path.join("data", "black_pawn.svg")), (ONE_CUBE_SIZE, ONE_CUBE_SIZE)))
    player1SpecialPieces = [(Pieces.ROOK, pygame.transform.smoothscale(pygame.image.load(os.path.join("data", "white_rook.svg")), (ONE_CUBE_SIZE, ONE_CUBE_SIZE))),
                            (Pieces.KNIGHT, pygame.transform.smoothscale(pygame.image.load(os.path.join("data", "white_knight.svg")), (ONE_CUBE_SIZE, ONE_CUBE_SIZE))),
                            (Pieces.BISHOP, pygame.transform.smoothscale(pygame.image.load(os.path.join("data", "white_bishop.svg")), (ONE_CUBE_SIZE, ONE_CUBE_SIZE))),
                            (Pieces.KING, pygame.transform.smoothscale(pygame.image.load(os.path.join("data", "white_king.svg")), (ONE_CUBE_SIZE, ONE_CUBE_SIZE))),
                            (Pieces.QUEEN, pygame.transform.smoothscale(pygame.image.load(os.path.join("data", "white_queen.svg")), (ONE_CUBE_SIZE, ONE_CUBE_SIZE)))]
    player2SpecialPieces = [(Pieces.ROOK, pygame.transform.smoothscale(pygame.image.load(os.path.join("data", "black_rook.svg")), (ONE_CUBE_SIZE, ONE_CUBE_SIZE))),
                            (Pieces.KNIGHT, pygame.transform.smoothscale(pygame.image.load(os.path.join("data", "black_knight.svg")), (ONE_CUBE_SIZE, ONE_CUBE_SIZE))),
                            (Pieces.BISHOP, pygame.transform.smoothscale(pygame.image.load(os.path.join("data", "black_bishop.svg")), (ONE_CUBE_SIZE, ONE_CUBE_SIZE))),
                            (Pieces.KING, pygame.transform.smoothscale(pygame.image.load(os.path.join("data", "black_king.svg")), (ONE_CUBE_SIZE, ONE_CUBE_SIZE))),
                            (Pieces.QUEEN, pygame.transform.smoothscale(pygame.image.load(os.path.join("data", "black_queen.svg")), (ONE_CUBE_SIZE, ONE_CUBE_SIZE)))]
    
    for i in range(NUMBER_OF_CUBES_IN_A_ROW):
        figuresPosition[player1PawnPositionY][i] = Figure(Players.PLAYER_1, player1Pawn[0], player1Pawn[1])   
        figuresPosition[player2PawnPositionY][i] = Figure(Players.PLAYER_2, player2Pawn[0], player2Pawn[1])

        index = i if i < len(player1SpecialPieces) else len(player1SpecialPieces) + 2 - i
        figuresPosition[player1SpecialPiecesPositionY][i] = Figure(Players.PLAYER_1, player1SpecialPieces[index][0], player1SpecialPieces[index][1])
        figuresPosition[player2SpecialPiecesPositionY][i] = Figure(Players.PLAYER_2, player2SpecialPieces[index][0], player2SpecialPieces[index][1])

def isTableEmpty(figuresPosition: Figure, indexX: int, indexY: int) -> bool:
    return figuresPosition[indexY][indexX] == None

def isFigureInTheSamePosition(figureIndexX: int, figureIndexY: int, indexX: int, indexY: int) -> bool:
    return figureIndexX == indexX and figureIndexY == indexY

def isFigureOfPlayer(figurePlayer: Players, player: Players):
    return figurePlayer == player

def deleteFigureFromTable(figuresPosition: Figure, indexX: int, indexY: int) -> Figure:
    temp = figuresPosition[indexY][indexX]
    figuresPosition[indexY][indexX] = None
    return temp

def addFigureToTable(figuresPosition: Figure, figure: Figure, indexX: int, indexY: int) -> Figure:
    figuresPosition[indexY][indexX] = figure

def getIndexFromCoordinate(x: float, y: float, nextPlayer: Players) -> tuple[int, int]:
    yIndex = int(y / ONE_CUBE_SIZE) if nextPlayer == Players.PLAYER_1 else NUMBER_OF_CUBES_IN_A_ROW - int(y / ONE_CUBE_SIZE) - 1
    return (int(x / ONE_CUBE_SIZE), yIndex)

def drawFigures(screen: pygame.Surface, figuresPosition: Figure, nextPlayer: Players):
    iterator = range(NUMBER_OF_CUBES_IN_A_ROW) if nextPlayer == Players.PLAYER_1 else range(NUMBER_OF_CUBES_IN_A_ROW-1, -1, -1)
    for y in iterator:
        for x in range(NUMBER_OF_CUBES_IN_A_COLUMN):
            if(figuresPosition[y][x] != None):
                ySize = y*ONE_CUBE_SIZE if nextPlayer == Players.PLAYER_1 else (NUMBER_OF_CUBES_IN_A_ROW-y-1)*ONE_CUBE_SIZE
                screen.blit(figuresPosition[y][x].image, (x*ONE_CUBE_SIZE, ySize))

def drawGrabbedByMousePiece(screen: pygame.Surface, image: pygame.Surface):
    x, y = pygame.mouse.get_pos()
    screen.blit(image, (x - ONE_CUBE_SIZE / 2, y - ONE_CUBE_SIZE / 2))


def start():
    pygame.init()
    screen = pygame.display.set_mode((SIZE, SIZE))
    clock = pygame.time.Clock()
    running = True

    figuresPosition: Figure = [[None for x in range(NUMBER_OF_CUBES_IN_A_ROW)] \
                                     for y in range(NUMBER_OF_CUBES_IN_A_COLUMN)]
    activeFigure: Figure = None
    activeFigureCoordinate: tuple[int, int] = None
    nextPlayer: Players = Players.PLAYER_1

    createFigures(figuresPosition, nextPlayer)

    while running:
        createBackground(screen, nextPlayer)
        drawFigures(screen, figuresPosition, nextPlayer)

        if activeFigure != None:
            drawGrabbedByMousePiece(screen, activeFigure.image)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                coordinate = getIndexFromCoordinate(*pygame.mouse.get_pos(), nextPlayer)
                if(not isTableEmpty(figuresPosition, *coordinate)
                   and isFigureOfPlayer(figuresPosition[coordinate[1]][coordinate[0]].player, nextPlayer)):
                    activeFigure = deleteFigureFromTable(figuresPosition, *coordinate)
                    activeFigureCoordinate = coordinate                    

            if event.type == pygame.MOUSEBUTTONUP and activeFigure != None:
                coordinate = getIndexFromCoordinate(*pygame.mouse.get_pos(), nextPlayer)
                if(isTableEmpty(figuresPosition, *coordinate) 
                   and not isFigureInTheSamePosition(*activeFigureCoordinate, *coordinate)):
                    addFigureToTable(figuresPosition, activeFigure, *coordinate)
                    nextPlayer = Players.getNextPlayer(nextPlayer)
                else:
                    addFigureToTable(figuresPosition, activeFigure, *activeFigureCoordinate)
                    
                activeFigure = None
                activeFigureCoordinate = None

        pygame.display.update()
        pygame.display.flip()
        
    pygame.quit()

if __name__ == "__main__":
    start()