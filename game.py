# Simon Says
# The purpose of the game is for the user to match what the computer does.  There will be 6 squares.
# The computer will show the user what they have to do as far clicking on each square.  It will increase the number of
# action by one each time.

# Class Options
# List to store which option was hit when
# We'll have to have something that will respond to user clicks
# https://stackoverflow.com/questions/6356840/how-to-detect-if-the-sprite-has-been-clicked-in-pygame
# http://www.pygame.org/docs/ref/rect.html#Rect.collidepoint

# Pygame template
import pygame
import random
import os

WIDTH = 800
HEIGHT = 600
FPS = 30

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Assets

game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'img')
background_image = pygame.image.load(os.path.join(img_folder, 'background.png'))


class Option(pygame.sprite.Sprite):
    # Sprite for the player
    def __init__(self, square_number, color, size_of_side, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((size_of_side, size_of_side))
        self.image.fill(color)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.font = pygame.font.SysFont('Comic Sans MS', 60)
        self.text = self.font.render(str(square_number), True, WHITE)

    def update(self):
        centerx = (self.rect.width / 2) - (self.text.get_rect().width / 2)
        centery = (self.rect.height / 2) - (self.text.get_rect().height / 2)
        self.image.blit(self.text, [centerx, centery])


# initialize pygame and create window
pygame.init()
pygame.mixer.init()
pygame.font.init()  # you have to call this at the start,

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Simon Says')
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
row1 = [
    (240, 103, 93),
    (113, 240, 149),
    (194, 62, 176),
]
row2 = [
    (116, 124, 204),
    (230, 176, 83),
    (122, 12, 16)
]
counter = 1
for color in row1:
    all_sprites.add(Option(str(counter), color, 200, 200 * counter, 200))
    counter += 1

counter = 1
for color in row2:
    all_sprites.add(Option(str(counter + 3), color, 200, 200 * counter, 400))
    counter += 1

running = True

while running:

    # keep loop running at the right speed
    clock.tick(FPS)
    # Events
    for event in pygame.event.get():
        # check for closing the window
        if event.type == pygame.QUIT:
            running = False

    # Update
    all_sprites.update()

    # Draw / Render
    screen.blit(background_image, [0, 0])
    all_sprites.draw(screen)

    # *after* drawing everything
    pygame.display.flip()

pygame.quit()
