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
HIGHLIGHT_COLOR = (181, 183, 186)
# Assets

game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'img')
background_image = pygame.image.load(os.path.join(img_folder, 'background.png'))

# initialize pygame and create window
pygame.init()
pygame.mixer.init()
pygame.font.init()  # you have to call this at the start,

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Simon Says')
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
sprite_list = []
simon_says_squares_highlight = []
simon_says_remember_choices = []
number_of_choices = 4

key_pressed_dictionary = {
    pygame.K_1: 1,
    pygame.K_2: 2,
    pygame.K_3: 3,
    pygame.K_4: 4,
    pygame.K_5: 5,
    pygame.K_6: 6
}


def simon_says_squares():
    simon_says_squares_highlight.clear()
    simon_says_remember_choices.clear()
    for i in range(0, number_of_choices):
        random_choice = random.randint(1, 6)
        simon_says_squares_highlight.append(random_choice)
        simon_says_remember_choices.append(random_choice)
    print(simon_says_remember_choices)

class Option(pygame.sprite.Sprite):
    # Sprite for the player
    def __init__(self, square_number, color, size_of_side, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((size_of_side, size_of_side))
        self.color = color
        self.image.fill(self.color)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.font = pygame.font.SysFont('Comic Sans MS', 60)
        self.text = self.font.render(str(square_number), True, WHITE)
        self.choose_square = False

    def toggle_highlight(self):
        self.choose_square = not self.choose_square

    def update(self):
        if self.choose_square:
            self.image.fill(HIGHLIGHT_COLOR)
        else:
            self.image.fill(self.color)

        centerx = (self.rect.width / 2) - (self.text.get_rect().width / 2)
        centery = (self.rect.height / 2) - (self.text.get_rect().height / 2)
        self.image.blit(self.text, [centerx, centery])


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
for color_square in row1:
    sprite = Option(str(counter), color_square, 200, 200 * counter, 200)
    all_sprites.add(sprite)
    sprite_list.append(sprite)
    counter += 1

counter = 1
for color_square in row2:
    sprite = Option(str(counter + 3), color_square, 200, 200 * counter, 400)
    all_sprites.add(sprite)
    sprite_list.append(sprite)
    counter += 1

running = True
mode = 'simon_says'
generate_numbers = True
next_square_time = pygame.time.get_ticks() + 1000
previous_choice = -1
human_move = 1
previous_choice_human = -1
un_highlight = False

while running:

    # keep loop running at the right speed
    clock.tick(FPS)

    # Has to be above the event types because we want the last square to high light
    # Because mode is set in the event

    # Events
    for event in pygame.event.get():
        # check for closing the window
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN and mode == 'human' and event.key in key_pressed_dictionary:
            sprite_list[key_pressed_dictionary[event.key] - 1].toggle_highlight()

            if previous_choice_human > -1:
                sprite_list[previous_choice_human].toggle_highlight()

            if simon_says_remember_choices[human_move - 1] == key_pressed_dictionary[event.key]:
                human_move += 1
                previous_choice_human = key_pressed_dictionary[event.key] - 1
                print("correct")
                if len(simon_says_remember_choices) < human_move:
                    mode = 'simon_says'
                    number_of_choices += 1
                    generate_numbers = True
                    human_move = 1
                    next_square_time = pygame.time.get_ticks() + 1000
            else:
                print("incorrect")
                mode = 'game_over'

    if mode == 'simon_says' and generate_numbers and next_square_time < pygame.time.get_ticks():
        simon_says_squares()
        generate_numbers = False
        if previous_choice_human > - 1:
            sprite_list[previous_choice_human].toggle_highlight()
            previous_choice_human = -1
            next_square_time = pygame.time.get_ticks() + 2000

    if len(simon_says_squares_highlight) == 0 and mode == 'simon_says' and next_square_time < pygame.time.get_ticks():
        mode = 'human'
        sprite_list[previous_choice].toggle_highlight()
        previous_choice = -1

    if mode == 'simon_says' and next_square_time < pygame.time.get_ticks():

        if previous_choice > -1 and un_highlight:
            sprite_list[previous_choice].toggle_highlight()
            next_square_time = pygame.time.get_ticks() + 1000
            un_highlight = False
        else:
            choice = simon_says_squares_highlight.pop(0)
            sprite_list[choice - 1].toggle_highlight()
            previous_choice = choice - 1
            next_square_time = pygame.time.get_ticks() + 1000
            un_highlight = True

    # Update
    all_sprites.update()

    # Draw / Render
    screen.blit(background_image, [0, 0])
    all_sprites.draw(screen)

    # *after* drawing everything
    pygame.display.flip()

pygame.quit()
