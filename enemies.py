import pygame
import random
import os
score_lis = []

WIDTH = 800
HEIGHT = 600

# Colors;
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (1, 1, 232)
GREEN = (55, 238, 2)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("CODING GAME...")
clock = pygame.time.Clock()


# set up assets folders
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, "images")
sprite_sheet_folder = os.path.join(img_folder, "sprite_sheet_for Enemy4")

# Load all game grafhics
space_ship_basic_enemy = pygame.image.load(os.path.join(img_folder, "Enemy1.png")).convert()

class Enemy1(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = space_ship_basic_enemy
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH + random.randrange(self.rect.width, self.rect.width + 1)
        self.rect.y = random.randrange(self.rect.height, HEIGHT - self.rect.height)
        self.lives = 1
        self.speedx = random.randrange(-2, -5, -1)
        self.speedy = random.randrange(-4, 2) or random.randrange(2, 5)
        self.score_value = 10

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.left < (0 - self.rect.width):
            self.kill()
        if self.lives < 0:
            self.kill()
            score_lis.append(self.score_value)
        if self.rect.top <= 0:
            self.rect.top = 0
            if self.speedy < 0:
                self.speedy = (self.speedy)*-1
            elif self.speedy == 0:
                self.speedy += 1
            elif self.speedy > 0:
                pass
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            if self.speedy > 0:
                self.speedy = (self.speedy)*-1
            elif self.speedy == 0:
                self.speedy -= 1
            elif self.speedy < 0:
                pass


def sprite_explosion_mine_animation(local):
    lis1 = [100, 99, 98, 97, 96, 95, 94, 93, 92, 91]
    lis2 = [90, 89, 88, 87, 86, 85, 84, 83, 82, 81]
    lis3 = [80, 79, 78, 77, 76, 75, 74, 73, 72, 71]
    lis4 = [70, 69, 68, 67, 66, 65, 64, 63, 62, 61]
    lis5 = [60, 59, 58, 57, 56, 55, 54, 53, 52, 51]
    lis6 = [50, 49, 48, 47, 46, 45, 44, 43, 42, 41]
    lis7 = [40, 39, 38, 37, 36, 35, 34, 33, 32, 31]
    lis8 = [30, 29, 28, 27, 26, 25, 24, 23, 22, 21]
    lis9 = [20, 19, 18, 17, 16, 15, 14, 13, 12, 11]
    lis10 = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
    if local in lis1:
        return pygame.image.load(os.path.join(sprite_sheet_folder, "1.png")).convert()
    elif local in lis2:
        return pygame.image.load(os.path.join(sprite_sheet_folder, "2.png")).convert()
    elif local in lis3:
        return pygame.image.load(os.path.join(sprite_sheet_folder, "3.png")).convert()
    elif local in lis4:
        return pygame.image.load(os.path.join(sprite_sheet_folder, "4.png")).convert()
    elif local in lis5:
        return pygame.image.load(os.path.join(sprite_sheet_folder, "5.png")).convert()
    elif local in lis6:
        return pygame.image.load(os.path.join(sprite_sheet_folder, "6.png")).convert()
    elif local in lis7:
        return pygame.image.load(os.path.join(sprite_sheet_folder, "7.png")).convert()
    elif local in lis8:
        return pygame.image.load(os.path.join(sprite_sheet_folder, "8.png")).convert()
    elif local in lis9:
        return pygame.image.load(os.path.join(sprite_sheet_folder, "9.png")).convert()
    elif local in lis10:
        return pygame.image.load(os.path.join(sprite_sheet_folder, "10.png")).convert()
