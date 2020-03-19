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
boss_folder = os.path.join(img_folder, "boss")
boss_magic_absorption = os.path.join(boss_folder, "boss_magic_absorption")

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

def sprite_shield_deteriorarion_animation(local1=0):
    lis1_ = [200, 199, 198, 197, 196, 195, 194, 193, 192, 191, 190, 189, 188, 187, 186, 185, 184, 183, 182, 181, 180, 179, 178, 177, 176, 175, 174, 173, 172, 171, 170, 169, 168, 167, 166, 165, 164, 163, 162, 161]
    lis2_ = [160, 159, 158, 157, 156, 155, 154, 153, 152, 151, 150, 149, 148, 147, 146, 145, 144, 143, 142, 141, 140, 139, 138, 137, 136, 135, 134, 133, 132, 131, 130, 129, 128, 127, 126, 125, 124, 123, 122, 121]
    lis3_ = [120, 119, 118, 117, 116, 115, 114, 113, 112, 111, 110, 109, 108, 107, 106, 105, 104, 103, 102, 101, 100, 99, 98, 97, 96, 95, 94, 93, 92, 91, 90, 89, 88, 87, 86, 85, 84, 83, 82, 81]
    lis4_ = [80, 79, 78, 77, 76, 75, 74, 73, 72, 71, 70, 69, 68, 67, 66, 65, 64, 63, 62, 61, 60, 59, 58, 57, 56, 55, 54, 53, 52, 51, 50, 49, 48, 47, 46, 45, 44, 43, 42, 41]
    lis5_ = [40, 39, 38, 37, 36, 35, 34, 33, 32, 31, 30, 29, 28, 27, 26, 25, 24, 23, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
    if local1 <= 0 and not local1 > 200:
        return pygame.image.load(os.path.join(boss_folder, "shield0.png")).convert()
    elif local1 in lis1_:
        return pygame.image.load(os.path.join(boss_folder, "shield.png")).convert()
    elif local1 in lis2_:
        return pygame.image.load(os.path.join(boss_folder, "shield1.png")).convert()
    elif local1 in lis3_:
        return pygame.image.load(os.path.join(boss_folder, "shield2.png")).convert()
    elif local1 in lis4_:
        return pygame.image.load(os.path.join(boss_folder, "shield3.png")).convert()
    elif local1 in lis5_:
        return pygame.image.load(os.path.join(boss_folder, "shield4.png")).convert()

def sprite_boss_magic_bullet(local):
    lis1_0 = [150, 149, 148, 147, 146, 145, 144, 143, 142, 141]
    lis1_1 = [140, 139, 138, 137, 136, 135, 134, 133, 132, 131]
    lis1_2 = [130, 129, 128, 127, 126, 125, 124, 123, 122, 121]
    lis1_3 = [120, 119, 118, 117, 116, 115, 114, 113, 112, 111]
    lis1_4 = [110, 109, 108, 107, 106, 105, 104, 103, 102, 101]
    lis1_5 = [100, 99, 98, 97, 96, 95, 94, 93, 92, 91]
    lis2 = [90, 89, 88, 87, 86, 85, 84, 83, 82, 81]
    lis3 = [80, 79, 78, 77, 76, 75, 74, 73, 72, 71]
    lis4 = [70, 69, 68, 67, 66, 65, 64, 63, 62, 61]
    lis5 = [60, 59, 58, 57, 56, 55, 54, 53, 52, 51]
    lis6 = [50, 49, 48, 47, 46, 45, 44, 43, 42, 41]
    lis7 = [40, 39, 38, 37, 36, 35, 34, 33, 32, 31]
    lis8 = [30, 29, 28, 27, 26, 25, 24, 23, 22, 21]
    lis9 = [20, 19, 18, 17, 16, 15, 14, 13, 12, 11]
    lis10 = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
    if local in lis1_0:
        return pygame.image.load(os.path.join(boss_magic_absorption, "15.png")).convert()
    elif local in lis1_1:
        return pygame.image.load(os.path.join(boss_magic_absorption, "14.png")).convert()
    elif local in lis1_2:
        return pygame.image.load(os.path.join(boss_magic_absorption, "13.png")).convert()
    elif local in lis1_3:
        return pygame.image.load(os.path.join(boss_magic_absorption, "12.png")).convert()
    elif local in lis1_4:
        return pygame.image.load(os.path.join(boss_magic_absorption, "11.png")).convert()
    elif local in lis1_5:
        return pygame.image.load(os.path.join(boss_magic_absorption, "10.png")).convert()
    elif local in lis2:
        return pygame.image.load(os.path.join(boss_magic_absorption, "00.png")).convert()
    elif local in lis3:
        return pygame.image.load(os.path.join(boss_magic_absorption, "01.png")).convert()
    elif local in lis4:
        return pygame.image.load(os.path.join(boss_magic_absorption, "02.png")).convert()
    elif local in lis5:
        return pygame.image.load(os.path.join(boss_magic_absorption, "03.png")).convert()
    elif local in lis6:
        return pygame.image.load(os.path.join(boss_magic_absorption, "04.png")).convert()
    elif local in lis7:
        return pygame.image.load(os.path.join(boss_magic_absorption, "05.png")).convert()
    elif local in lis8:
        return pygame.image.load(os.path.join(boss_magic_absorption, "06.png")).convert()
    elif local in lis9:
        return pygame.image.load(os.path.join(boss_magic_absorption, "07.png")).convert()
    elif local in lis10:
        return pygame.image.load(os.path.join(boss_magic_absorption, "08.png")).convert()

list_for_enemy1_inkolking = []