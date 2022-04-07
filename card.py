# https://stackoverflow.com/questions/44580764/what-is-a-good-way-to-layer-like-this-in-pygame

import pygame

CARDSIZE = 30

class Card(pygame.sprite.Sprite):
    def __init__(self, image, pos, layer=1):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(image, (CARDSIZE, CARDSIZE))
        self._layer = layer
        self.rect = self.image.get_rect(topleft=pos)
        # self.rect = pygame.Rect(xpos, ypos, image.get_width(), image.get_height())
        self.clicked = False
        self.is_in_cell = False
        self.alphabet = None
        self.is_in_cell = False

    def alphabet(self):
        alphabet = [k for k, v in locals().items()]
        return alphabet

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    # the appearance of the card when clicked
    def is_clicked():
        return False

    # turn True when the card is placed on a cell
    def is_in_cell():
        return False    


