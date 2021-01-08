import pygame
from pygame import *
import os
import sys
import random

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
WHITE = (255, 255, 255)
BACKGROUND_COLOR = (41, 41, 41)

###############
# Clases
###############


class PieceToEat(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.color = (197, 36, 36)
        self.image = pygame.Surface([15, 15])
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH-10)
        self.rect.y = random.randint(0, SCREEN_HEIGHT-10)

    def recalculate(self):
        self.rect.x = random.randint(0, SCREEN_WIDTH-10)
        self.rect.y = random.randint(0, SCREEN_HEIGHT-10)


class Piece(pygame.sprite.Sprite):
    "Piece of snake"

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([15, 15])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def colision(self, objetivo):
        if self.rect.colliderect(objetivo.rect):
            return True

        return False

    def checkBorders(self):
        # cuando llega a los bordes
        if self.rect.x < 0:
            self.rect.x = SCREEN_WIDTH
        elif self.rect.x > SCREEN_WIDTH:
            self.rect.x = 0
        elif self.rect.y < 0:
            self.rect.y = SCREEN_HEIGHT
        elif self.rect.y > SCREEN_HEIGHT:
            self.rect.y = 0


###############
# Main
###############


def main():
    pygame.init()
    # creamos la ventana y le indicamos un titulo:
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Snake")

    # se define la letra por defecto
    fuente = pygame.font.Font(None, 20)

    clock = pygame.time.Clock()

    snake_list = []
    snake_sprites = pygame.sprite.Group()
    piece = Piece(10, 25)
    snake_list.append(piece)
    snake_sprites.add(piece)

    pieceToEat = PieceToEat()

    cambio_x = 15
    cambio_y = 0

    total_length = 1
    velocidad = 10

    while True:
        clock.tick(velocidad)

        # Comprobamos si colisionan los objetos
        if snake_list[0].colision(pieceToEat):
            pieceToEat.recalculate()
            newPiece = Piece(snake_list[-1].rect.x, snake_list[-1].rect.y)
            snake_sprites.add(newPiece)
            snake_list.insert(-1, newPiece)
            total_length += 1
            velocidad += 5
        # else:
        #   for i in snake_list:
        #       #cuando se choca consigo mismo
        #       if snake_list[0] != i and snake_list[0].colision(i):
        #          sys.exit()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    cambio_x = -15
                    cambio_y = 0
                if event.key == pygame.K_RIGHT:
                    cambio_x = 15
                    cambio_y = 0
                if event.key == pygame.K_UP:
                    cambio_x = 0
                    cambio_y = -15
                if event.key == pygame.K_DOWN:
                    cambio_x = 0
                    cambio_y = 15

        x = snake_list[0].rect.x + cambio_x
        y = snake_list[0].rect.y + cambio_y
        newPiece = Piece(x, y)

        snake_sprites.add(newPiece)
        snake_list.insert(0, newPiece)

        # remove the last one
        last_piece = snake_list.pop()
        snake_sprites.remove(last_piece)

        newPiece.checkBorders()

        text = "Length: %d  Speed: %d" % (total_length, velocidad)
        mensaje = fuente.render(text, 1, (255, 255, 255))

        # actualizamos la pantalla
        screen.fill(BACKGROUND_COLOR)
        snake_sprites.draw(screen)
        screen.blit(pieceToEat.image, pieceToEat.rect)
        screen.blit(mensaje, (15, 5))
        pygame.display.flip()


if __name__ == "__main__":
    main()
