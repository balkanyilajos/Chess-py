from win32api import GetSystemMetrics
import pygame
import os
from enums import Players, Pieces

SIZE = int(GetSystemMetrics(0) * 0.6) if GetSystemMetrics(0) < GetSystemMetrics(1) else int(GetSystemMetrics(1) * 0.6)
NUMBER_OF_CUBES_IN_A_ROW = 8
ONE_CUBE_SIZE = int(SIZE / NUMBER_OF_CUBES_IN_A_ROW)

PLAYER_COLOR_1 = (109, 82, 73)
PLAYER_COLOR_2 = (248, 243, 227)

FIGURES_POSITION = [[None for x in range(NUMBER_OF_CUBES_IN_A_ROW)] for y in range(NUMBER_OF_CUBES_IN_A_ROW)]

def createBackground(screen: pygame.Surface, isUpPlayer1: bool = True):
    for y in range(0, SIZE, ONE_CUBE_SIZE):
        for x in range (0, SIZE, ONE_CUBE_SIZE):
            color = PLAYER_COLOR_1 if isUpPlayer1 else PLAYER_COLOR_2
            isUpPlayer1 = not isUpPlayer1

            pygame.draw.rect(screen, color, (x, y, ONE_CUBE_SIZE, ONE_CUBE_SIZE))

        isUpPlayer1 = not isUpPlayer1

def createAndDisplayFigures(screen: pygame.Surface, isUpPlayer1: bool = True):
    player1PawnPositionY = NUMBER_OF_CUBES_IN_A_ROW - 2 if isUpPlayer1 else 1
    player1SpecialPiecesPositionY = NUMBER_OF_CUBES_IN_A_ROW - 1 if isUpPlayer1 else 0
    player2PawnPositionY = NUMBER_OF_CUBES_IN_A_ROW - 2 if not isUpPlayer1 else 1
    player2SpecialPiecesPositionY = NUMBER_OF_CUBES_IN_A_ROW - 1 if not isUpPlayer1 else 0

    player1Pawn = (Pieces.PAWN, pygame.image.load(os.path.join("data", "white_pawn.svg")))
    player2Pawn = (Pieces.PAWN, pygame.image.load(os.path.join("data", "black_pawn.svg")))
    player1SpecialPieces = [(Pieces.ROOK, pygame.image.load(os.path.join("data", "white_rook.svg"))),
                            (Pieces.KNIGHT, pygame.image.load(os.path.join("data", "white_knight.svg"))),
                            (Pieces.BISHOP, pygame.image.load(os.path.join("data", "white_bishop.svg"))),
                            (Pieces.KING, pygame.image.load(os.path.join("data", "white_king.svg"))),
                            (Pieces.QUEEN, pygame.image.load(os.path.join("data", "white_queen.svg")))]
    player2SpecialPieces = [(Pieces.ROOK, pygame.image.load(os.path.join("data", "black_rook.svg"))),
                            (Pieces.KNIGHT, pygame.image.load(os.path.join("data", "black_knight.svg"))),
                            (Pieces.BISHOP, pygame.image.load(os.path.join("data", "black_bishop.svg"))),
                            (Pieces.KING, pygame.image.load(os.path.join("data", "black_king.svg"))),
                            (Pieces.QUEEN, pygame.image.load(os.path.join("data", "black_queen.svg")))]
    
    for i in range(NUMBER_OF_CUBES_IN_A_ROW):
        FIGURES_POSITION[player1PawnPositionY][i] = (Players.PLAYER_1, player1Pawn[0])
        screen.blit(pygame.transform.smoothscale(player1Pawn[1], (ONE_CUBE_SIZE, ONE_CUBE_SIZE)), (i * ONE_CUBE_SIZE, player1PawnPositionY * ONE_CUBE_SIZE))    
        FIGURES_POSITION[player2PawnPositionY][i] = (Players.PLAYER_1, player2Pawn[0])
        screen.blit(pygame.transform.smoothscale(player2Pawn[1], (ONE_CUBE_SIZE, ONE_CUBE_SIZE)), (i * ONE_CUBE_SIZE, player2PawnPositionY * ONE_CUBE_SIZE))

        index = i if i < len(player1SpecialPieces) else len(player1SpecialPieces) + 2 - i
        FIGURES_POSITION[player1SpecialPiecesPositionY][i] = (Players.PLAYER_1, player1SpecialPieces[index][0])
        screen.blit(pygame.transform.smoothscale(player1SpecialPieces[index][1], (ONE_CUBE_SIZE, ONE_CUBE_SIZE)), (i * ONE_CUBE_SIZE, player1SpecialPiecesPositionY * ONE_CUBE_SIZE))
        FIGURES_POSITION[player2SpecialPiecesPositionY][i] = (Players.PLAYER_1, player1SpecialPieces[index][0])
        screen.blit(pygame.transform.smoothscale(player2SpecialPieces[index][1], (ONE_CUBE_SIZE, ONE_CUBE_SIZE)), (i * ONE_CUBE_SIZE, player2SpecialPiecesPositionY * ONE_CUBE_SIZE))        

def start():
    pygame.init()
    screen = pygame.display.set_mode((SIZE, SIZE))
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        createBackground(screen)
        createAndDisplayFigures(screen)
        pygame.display.update()
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    start()