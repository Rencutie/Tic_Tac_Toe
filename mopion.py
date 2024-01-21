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

turn = "red"


class Square:
    """
    each square is an object of this class

    """

    def __init__(self, xstart, ystart, color="neutral"):
        self.xstart = xstart
        self.ystart = ystart
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
        elif turn == "blue" and self.color == "neutral":
            self.color = "blue"
            turn = "red"


def redTurn():
    bleu_turn.blit(screen, (650, 100))


def isFull():
    """check if every square is full

    Returns:
        True: every square is full
        False: not every square is full
    """
    for square in square_list:
        if square.color == "neutral":
            return False
    return True


square_list = []

for row in range(3):
    # create all the squares to put them into the list
    for column in range(3):
        x = column * square_size
        y = row * square_size
        square = Square(x, y)
        square_list.append(square)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            # check if a square is pressed and change it accordingly
            if event.type == pygame.MOUSEBUTTONDOWN:
                for square in square_list:
                    if square.rect.collidepoint(pygame.mouse.get_pos()):
                        square.change_color()

        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                print("restart")
                # restarting the game, putting the squares back to neutral
                for square in square_list:
                    square.color = "neutral"
                game_active = True

    if game_active:
        # background
        screen.fill((255, 255, 255))
        pygame.draw.rect(screen, "silver", tabRect)
        screen.blit(bleu_turn, (605, 100))
        # drawing squares
        for square in square_list:
            square.draw(screen)

        # check if all the squares are full and stop the game if they are
        if isFull():
            game_active = False

    pygame.display.update()
    Clock.tick(60)
