"""
    jeu de morpion, option 2 joueurs ou solo vs IA
    on arrive dans un menue pour choisir quand on lance
    puis on peut jouer mdr
    je sais pas si je vais rentrer toutes les possibilité dans l'IA, un peu la flemme
    peut etre au hasard
"""

import pygame
from sys import exit

width, height = 800, 600

pygame.init()
screen = pygame.display.set_mode((width, height))
Clock = pygame.time.Clock()
pygame.display.set_caption("morpion")
game_active = True

xPosTabRect, yPosTabRect = 600, 0
widthTabRect, heightTabRect = 200, 600
tabRect = pygame.Rect(xPosTabRect, yPosTabRect, widthTabRect, heightTabRect)

square_size = height // 3
bleu_turn = pygame.image.load("morpion/graphics/blue_rectangle.png").convert_alpha()
bleu_turn = pygame.transform.scale(bleu_turn, (200, 100))

red_turn = pygame.image.load("morpion/graphics/red_rectangle.png").convert_alpha()
red_turn = pygame.transform.scale(red_turn, (200, 100))
turn = "red"

scoreRed = 0
scoreBlue = 0

font = pygame.font.Font(None, 36)

bluePlaySound = pygame.mixer.Sound("morpion/audio/playBlue.wav")
redPlaySound = pygame.mixer.Sound("morpion/audio/playRed.wav")
winSound = pygame.mixer.Sound("morpion/audio/win.wav")
drawSound = pygame.mixer.Sound("morpion/audio/draw.wav")
restartSound = pygame.mixer.Sound("morpion/audio/restart.wav")


class Square:
    """
    each square is an object of this class

    """

    def __init__(self, xstart, ystart, row, col, color="neutral"):
        self.xstart = xstart
        self.ystart = ystart
        self.row = row
        self.col = col
        self.color = color
        self.rect = pygame.Rect(xstart, ystart, square_size, square_size)

    def draw(self, surface):
        """draws an empty rectangle if neutral, if red add the red_cross inside
        and if blue add the blue_cross
        """
        pygame.draw.rect(surface, "black", self.rect, 1)

        if self.color == "neutral":
            pass
        elif self.color == "red":
            red_cross = pygame.image.load(
                "morpion/graphics/red_cross.png"
            ).convert_alpha()
            red_cross = pygame.transform.scale(red_cross, (square_size, square_size))
            surface.blit(red_cross, (self.xstart, self.ystart))

        elif self.color == "blue":
            blue_circle = pygame.image.load(
                "morpion/graphics/blue_circle.png"
            ).convert_alpha()
            blue_circle = pygame.transform.scale(
                blue_circle, (square_size, square_size)
            )
            surface.blit(blue_circle, (self.xstart, self.ystart))

    def change_color(self):
        """changes the color of the square depending on whose turn it is."""
        global turn
        print("is pressed")
        if turn == "red" and self.color == "neutral":
            self.color = "red"
            turn = "blue"
            redPlaySound.play()
        elif turn == "blue" and self.color == "neutral":
            self.color = "blue"
            turn = "red"
            bluePlaySound.play()


def redTurn():
    """show the red rectangle saying red turn"""
    screen.blit(red_turn, (605, 100))
    screen.blit(bleu_turn, (1650, 100))


def blueTurn():
    """show the blue rectangle saying blue turn"""
    screen.blit(bleu_turn, (605, 100))
    screen.blit(red_turn, (1650, 100))


def endScreen():
    endtext = font.render("press space", True, "black")
    endtext2 = font.render("to restart", True, "black")
    screen.blit(endtext, (605, 100))
    screen.blit(endtext2, (605, 130))


def displayScore():
    """display the score on the screen"""
    scoreText = font.render(f"Score :", True, "black")
    screen.blit(scoreText, (width - 190, 250))
    bluescoretext = font.render(f"blue : {scoreBlue}", True, "black")
    screen.blit(bluescoretext, (width - 190, 280))
    redscoretext = font.render(f"red : {scoreRed}", True, "black")
    screen.blit(redscoretext, (width - 190, 310))


def isFull():
    """check if every square is full

    Returns:
        True: every square is full
        False: not every square is full
    """
    for list in square_list:
        for square in list:
            if square.color == "neutral":
                return False
    return True


def playerWin():
    """check if player won and return the color
    of the winner if there is one
    """
    for row in range(3):
        if all(square.color == "blue" for square in square_list[row]):
            return "blue"
        elif all(square.color == "red" for square in square_list[row]):
            return "red"

    # Check columns
    for col in range(3):
        if all(square_list[row][col].color == "blue" for row in range(3)):
            return "blue"
        elif all(square_list[row][col].color == "red" for row in range(3)):
            return "red"

    # Check diagonals
    if all(square_list[i][i].color == "blue" for i in range(3)):
        return "blue"
    elif all(square_list[i][3 - i - 1].color == "blue" for i in range(3)):
        return "blue"
    elif all(square_list[i][i].color == "red" for i in range(3)):
        return "red"
    elif all(square_list[i][3 - i - 1].color == "red" for i in range(3)):
        return "red"


square_list = []

for row in range(3):
    row_list = []
    # create all the squares to put them into the list
    for column in range(3):
        x = column * square_size
        y = row * square_size

        row_list.append(Square(x, y, row, column))
    square_list.append(row_list)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            # check if a square is pressed and change it accordingly
            if event.type == pygame.MOUSEBUTTONDOWN:
                for list in square_list:
                    for square in list:
                        if square.rect.collidepoint(pygame.mouse.get_pos()):
                            square.change_color()

        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                print("restart")
                # restarting the game, putting the squares back to neutral
                for list in square_list:
                    for square in list:
                        square.color = "neutral"
                game_active = True
                restartSound.play()

    if game_active:
        # background
        screen.fill((255, 255, 255))
        pygame.draw.rect(screen, "silver", tabRect)

        # drawing squares
        for list in square_list:
            for square in list:
                square.draw(screen)

        if playerWin() == "red":
            endScreen()
            scoreRed += 1
            game_active = False
            winSound.play()
        elif playerWin() == "blue":
            endScreen()
            scoreBlue += 1
            game_active = False
            winSound.play()
        elif isFull():
            endScreen()
            scoreRed += 0.5
            scoreBlue += 0.5
            game_active = False
            drawSound.play()
        else:
            if turn == "red":
                redTurn()
            else:
                blueTurn()
        displayScore()

        # check if all the squares are full and stop the game if they are

    pygame.display.update()
    Clock.tick(60)
