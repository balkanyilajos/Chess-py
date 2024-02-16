from win32api import GetSystemMetrics
import pygame
import os
from enums import Players, Pieces
from figure import Figure

SIZE = int(GetSystemMetrics(0) * 0.6) if GetSystemMetrics(0) < GetSystemMetrics(1) else int(GetSystemMetrics(1) * 0.6)
NUMBER_OF_CUBES_IN_A_ROW = 8
ONE_CUBE_SIZE = int(SIZE / NUMBER_OF_CUBES_IN_A_ROW)

PLAYER_COLOR_1 = (109, 82, 73)
PLAYER_COLOR_2 = (248, 243, 227)

FIGURES_POSITION: Figure = [[None for x in range(NUMBER_OF_CUBES_IN_A_ROW)] for y in range(NUMBER_OF_CUBES_IN_A_ROW)]

ACTIVE_FIGURE: Figure = None

def createBackground(screen: pygame.Surface, isUpPlayer1: bool = True):
    for y in range(0, SIZE, ONE_CUBE_SIZE):
        for x in range (0, SIZE, ONE_CUBE_SIZE):
            color = PLAYER_COLOR_1 if isUpPlayer1 else PLAYER_COLOR_2
            isUpPlayer1 = not isUpPlayer1

            pygame.draw.rect(screen, color, (x, y, ONE_CUBE_SIZE, ONE_CUBE_SIZE))

        isUpPlayer1 = not isUpPlayer1

def createFigures(isUpPlayer1: bool = True):
    player1PawnPositionY = NUMBER_OF_CUBES_IN_A_ROW - 2 if isUpPlayer1 else 1
    player1SpecialPiecesPositionY = NUMBER_OF_CUBES_IN_A_ROW - 1 if isUpPlayer1 else 0
    player2PawnPositionY = NUMBER_OF_CUBES_IN_A_ROW - 2 if not isUpPlayer1 else 1
    player2SpecialPiecesPositionY = NUMBER_OF_CUBES_IN_A_ROW - 1 if not isUpPlayer1 else 0

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
        FIGURES_POSITION[player1PawnPositionY][i] = Figure(Players.PLAYER_1, player1Pawn[0], player1Pawn[1])   
        FIGURES_POSITION[player2PawnPositionY][i] = Figure(Players.PLAYER_1, player2Pawn[0], player2Pawn[1])

        index = i if i < len(player1SpecialPieces) else len(player1SpecialPieces) + 2 - i
        FIGURES_POSITION[player1SpecialPiecesPositionY][i] = Figure(Players.PLAYER_1, player1SpecialPieces[index][0], player1SpecialPieces[index][1])
        FIGURES_POSITION[player2SpecialPiecesPositionY][i] = Figure(Players.PLAYER_1, player2SpecialPieces[index][0], player2SpecialPieces[index][1])

def deleteFigureFromTable(indexX: int, indexY: int) -> Figure:
    temp = FIGURES_POSITION[indexY][indexX]
    FIGURES_POSITION[indexY][indexX] = None
    return temp

def getIndexFromCoordinate(x: float, y: float) -> tuple[int, int]:
    return (int(x / ONE_CUBE_SIZE), int(y / ONE_CUBE_SIZE))

def drawFigures(screen: pygame.Surface):
    for y in range(len(FIGURES_POSITION)):
        for x in range(len(FIGURES_POSITION[y])):
            if(FIGURES_POSITION[y][x] != None):
                screen.blit(FIGURES_POSITION[y][x].image, (x*ONE_CUBE_SIZE, y*ONE_CUBE_SIZE))

def drawGrabbedByMousePiece(screen: pygame.Surface, image: pygame.Surface):
    x, y = pygame.mouse.get_pos()
    screen.blit(image, (x - ONE_CUBE_SIZE / 2, y - ONE_CUBE_SIZE / 2))

def putDownPiece(figure: Figure, indexX: int, indexY: int):
    if FIGURES_POSITION[indexY][indexX] == None:
        FIGURES_POSITION[indexY][indexX] = figure


def start():
    pygame.init()
    screen = pygame.display.set_mode((SIZE, SIZE))
    clock = pygame.time.Clock()
    running = True

    createFigures(screen)

    while running:
        running = next(screen)
        
    pygame.quit()

def next(screen: pygame.Surface) -> bool:
    global ACTIVE_FIGURE

    createBackground(screen)
    drawFigures(screen)

    if ACTIVE_FIGURE != None:
        drawGrabbedByMousePiece(screen, ACTIVE_FIGURE.image)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = getIndexFromCoordinate(*pygame.mouse.get_pos())
            if(FIGURES_POSITION[y][x] != None):
                ACTIVE_FIGURE = deleteFigureFromTable(x, y)

        if event.type == pygame.MOUSEBUTTONUP:
            putDownPiece(ACTIVE_FIGURE, *getIndexFromCoordinate(*pygame.mouse.get_pos()))
            ACTIVE_FIGURE = None

    pygame.display.update()
    pygame.display.flip()
    
    return True

if __name__ == "__main__":
    start()