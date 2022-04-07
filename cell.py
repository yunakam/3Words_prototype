# https://stackoverflow.com/questions/44580764/what-is-a-good-way-to-layer-like-this-in-pygame

import pygame, random
from pygame.locals import *


class Cell(pygame.sprite.Sprite):
    def __init__(self, screen, cell_bdcolor, rect, layer=0):
        pygame.sprite.Sprite.__init__(self)
        self._layer = layer
        self.screen = screen
        self.cell_bdcolor = cell_bdcolor
        self.rect = rect
        self.size = self.rect.size
        self.has_thecard = False
        self.card = None

    def draw(self):
        pygame.draw.rect(self.screen, self.cell_bdcolor, self.rect, 2)
        # screen.blit(self.image, self.rect)
    
    def switch(self, on_off):
        if on_off == 1:     # 'on'
            # pygame.draw.rect(self.screen, self.cell_bdcolor, self.rect, 0)
            self.has_thecard = True
            pygame.display.flip()
        elif on_off == 0:
            # self.draw()
            self.has_thecard = False
            pass
        # screen.blit(self.image, self.rect)


# Tried to make a function to draw a random number of cells in each plate here, but didnt work b/c of cell_group
def draw_cells_on_plate(min, max, topleft, width, surf, bdcolor='black', cellsize=40, parent_group=None):
    global cell_group0
    cell_group0 = pygame.sprite.LayeredUpdates()
    number = random.randint(min, max)
    print("number of cells in plate0: ", number)
    total_width = 40*number + 5*(number-1)
    x, y = topleft[0]+(width - total_width)//2, topleft[1]+30
    for _ in range(number):
        c = Cell(surf, bdcolor, Rect(x, y, cellsize, cellsize))
        cell_group0.add(c)
        parent_group.add(c)
        x += 45    
