# importing necessary things
import pygame
import random
import os
import math

# dimensions
WIDTH = 800
HEIGHT = 600
FPS = 70

# Colors;
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (1, 1, 232)
BEAM_COLOR = (13, 24, 164)
GREEN = (55, 238, 2)

# initializate pygame and create the window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("CODING GAME...")
clock = pygame.time.Clock()

# set up assets folders
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, "images")
boss_folder = os.path.join(img_folder, "boss")

# Load all game grafhics
space_ship_player = pygame.image.load(os.path.join(img_folder, "player_space_ship.png")).convert()
space_ship_player_respawn = pygame.image.load(os.path.join(img_folder, "testing.png")).convert()
background = pygame.image.load(os.path.join(img_folder, "r-type_2_background.png")).convert()
space_ship_player_basic_bullet = pygame.image.load(os.path.join(img_folder, "P_bullet.png")).convert()
advanced_bullet_img = pygame.image.load(os.path.join(img_folder, "P_special_bullet1.png")).convert()
enemy_guided_img = pygame.image.load(os.path.join(img_folder, "alien_spaceship_invasion_mine.png")).convert()
enemy_guided_byycord_img = pygame.image.load(os.path.join(img_folder, "alien_spaceship_invasion_10.png")).convert()
enemy3_bullet_img = pygame.image.load(os.path.join(img_folder, "enemy3bullet.png")).convert()
power_up1_img = pygame.image.load(os.path.join(img_folder, "gun09.png")).convert()
power_up1_1_img = pygame.image.load(os.path.join(img_folder, "gun10.png")).convert()
power_up_1_icon_img = pygame.image.load(os.path.join(img_folder, "power_up_1_icon.png")).convert()
power_up_1_basic_bullet_img = pygame.image.load(os.path.join(img_folder, "power_up_1_basic_bullet_img.png")).convert()
enemy4_off_img = pygame.image.load(os.path.join(img_folder, "enemy_exploding_off.png")).convert()
enemy4_on_img = pygame.image.load(os.path.join(img_folder, "enemy_exploding_on.png")).convert()
enemy4_exploding_img = pygame.image.load(os.path.join(img_folder, "explosion3 - Copia.png")).convert()
laser_beam_charging_img = pygame.image.load(os.path.join(img_folder, "laser_beam_charging_img.png")).convert()
boss_img = pygame.image.load(os.path.join(boss_folder, "dark_matter.png")).convert()
boss_shield_img = pygame.image.load(os.path.join(boss_folder, "shield5.png")).convert()
space_ship_basic_enemy = pygame.image.load(os.path.join(img_folder, "Enemy1.png")).convert()

# Groups of the sprites;
all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
mobs = pygame.sprite.Group()
enemy3_bullet_g = pygame.sprite.Group()
player_power_up_1_g = pygame.sprite.Group()
player_power_up_1_1_g = pygame.sprite.Group()
power_up_1_bullet_g = pygame.sprite.Group()
power_up_1_1_bullet_g = pygame.sprite.Group()
boss_group = pygame.sprite.Group()
boss_shield_group = pygame.sprite.Group()

# varialbles to control the respawntime - 1.1.3
colliding = True
tr_controll = 140

# these variables works with - 1.1.3
activated = False
loading = False
release = False

# this lis acumulates one`s (1) to charge energy to the advanced_shoot
lis_charge_energy = []

# Things releated with the player;
class Player(pygame.sprite.Sprite):
    # sprite for the player
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = space_ship_player
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centery = (HEIGHT/2)
        self.rect.centerx = (WIDTH/2)
        self.speedx = 0
        self.speedy = 0
        self.lives = 3
        self.is_alive = True

    def update(self):
        if self.lives < 0:
            self.kill()
            self.is_alive = False
        self.speedx = 0
        self.speedy = 0
        Keystate = pygame.key.get_pressed()
        if Keystate[pygame.K_a]:
            self.speedx -= 5
        if Keystate[pygame.K_d]:
            self.speedx += 5
        if Keystate[pygame.K_w]:
            self.speedy -= 5
        if Keystate[pygame.K_s]:
            self.speedy += 5
        if Keystate[pygame.K_9] and sum(lis_charge_energy) <= 200:
            lis_charge_energy.append(1.5*2)
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

    def shoot(self):
        basic_bullet = Bullet(self.rect.centery, self.rect.right)
        advanced_bullet = Bullet(self.rect.centery, self.rect.right)
        if 1 <= int(sum(lis_charge_energy)) < 200:
            all_sprites.add(basic_bullet)
            bullets.add(basic_bullet)
            self.atackdamage = 1
        if int(sum(lis_charge_energy)) >= 200:
            all_sprites.add(advanced_bullet)
            bullets.add(advanced_bullet)
            self.atackdamage = 10

# create player_obj and addint it to all_sprites
player = Player()
all_sprites.add(player)

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
        self.center = [self.rect.x + self.rect.width/2,self.rect.y + self.rect.height/2]

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

        detect_collisions_enemy_playerbullets(self)

# bullet class for player shoot
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        if int(sum(lis_charge_energy)) >= 200:
            self.image = advanced_bullet_img
            self.image.set_colorkey(BLACK)
            #self.damage = 10
        if 1 <= int(sum(lis_charge_energy)) < 200:
            self.image = space_ship_player_basic_bullet
            self.image.set_colorkey(BLACK)
            #self.damage = 1
        self.rect = self.image.get_rect()
        self.rect.left = y
        self.rect.centery = x
        self.speedx = 15

    def update(self):
        self.rect.x += self.speedx
        # delet the bullet if it try to go out of the right of the screen
        if self.rect.right >= WIDTH:
            self.kill()

# bullet class for Enemy3 shoot
class Enemy3Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = enemy3_bullet_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.left = y
        self.rect.centery = x
        self.speedx = 10

    def update(self):
        self.rect.x -= self.speedx
        # delet the bullet if it try to go out of the right of the screen
        if self.rect.right <= 0:
            self.kill()

# Score things;
font_name = pygame.font.match_font('Cooper Black')
from enemies import score_lis
score = str(sum(score_lis))
def draw_score(surf=screen, text="HI - 0", size=30, x=(WIDTH - 100), y=(HEIGHT-60)):
    # this function was made to show the score on the screen
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

# Live things;
font_name_live = pygame.font.match_font('Cooper Black')
live_lis = [1, 1, 1]
lives = str(sum(live_lis))
def draw_lives(surf=screen, text="LIVES - " + lives, size=30, x=(100), y=(HEIGHT-60)):
    # this function was made to show the lives of the player left on the screen
    font = pygame.font.Font(font_name_live, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

# Canon charge things;
font_name_beam_charget = pygame.font.match_font('Cooper Black')
def draw_beam_charge(surf=screen, text="BEAM", size=30, x=(WIDTH/2 - 170), y=(HEIGHT-47)):
    # this function was made to show the percentage of the beam
    font = pygame.font.Font(font_name_beam_charget, size)
    text_surface = font.render(text, True, BLUE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

# laser beam img class
class CanonCharge(pygame.sprite.Sprite):
    def __init__(self):
        self.w_size = int(sum(lis_charge_energy))
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((self.w_size, 14))
        self.image.fill(BEAM_COLOR)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2 - 100, HEIGHT - self.rect.height*2)

    def update(self):
        self.w_size = int(sum(lis_charge_energy))
        self.image = pygame.Surface((self.w_size, 14))
        self.image.fill(BEAM_COLOR)

# beam_things;
beam_charge_obj = CanonCharge()
all_sprites.add(beam_charge_obj)

# Background;
background_x_position = 0
background_x_position_boss = 0
background_y_position = 0
background_y_position_boss = 0
background_boss_position = +3*3
STAGE_TIME = 0

# explosive mine;
from enemies import sprite_explosion_mine_animation
class Enemy4(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = enemy4_off_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.y = random.randrange(0 + self.rect.height, HEIGHT - self.rect.height)
        self.rect.x = random.randrange(WIDTH + self.rect.width, WIDTH + self.rect.width*2)
        self.speedx = -1
        self.score_value = 5
        self.lives = 2
        self.timing_to_mine_explosion = 100
        self.start_timing = False
        self.exploding_animation_timing = 100
        self.start_exploding_timing = False
        self.count = 0

        self.its_off_lis = [100, 99, 98, 97, 96, 95, 94, 93, 92, 91,
                            80, 79, 78, 77, 76, 75, 74, 73, 72, 71,
                            60, 59, 58, 57, 56, 55, 54, 53, 52, 51,
                            40, 39, 38, 37, 36, 35, 34, 33, 32, 31,
                            20, 19, 18, 17, 16, 15, 14, 13, 12, 11]

        self.its_on_lis = [90, 89, 88, 87, 86, 85, 84, 83, 82, 81,
                           70, 69, 68, 67, 66, 65, 64, 63, 62, 61,
                           50, 49, 48, 47, 46, 45, 44, 43, 42, 41,
                           30, 29, 28, 27, 26, 25, 24, 23, 22, 21,
                           10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0]

    def explode(self):
        #print("mudou de imagem")
        #get into spritesheet
        if self.count == 0:
            self.rect.y -= abs(self.rect.y - self.rect.centery)
            self.rect.x -= abs(self.rect.x - self.rect.centerx)
            mobs.add(self)
            self.count = 1
        self.image = sprite_explosion_mine_animation(local=self.exploding_animation_timing)
        self.image.set_colorkey(BLACK)

    def update(self):

        print(self.rect.centerx, self.rect.centery)

        self.rect.x += self.speedx
        if self.rect.left < (0 - self.rect.width):
            self.kill()
            #print("morreu")
        if self.lives <= 0:
            self.kill()
            score_lis.append(self.score_value)

        if 0 <= abs(player.rect.center[0] - self.rect.center[0]) <= self.rect.width*4 and 0 <= abs(player.rect.center[1] - self.rect.center[1]) <= self.rect.height*3:
            self.start_timing = True

        if self.timing_to_mine_explosion <= 0:
            self.start_timing = False
            self.start_exploding_timing = True
            if self.start_exploding_timing == True:
                self.exploding_animation_timing -= 2
                self.explode()
                if self.exploding_animation_timing <= 0:
                    self.kill()
            #print("explodiu")

        detect_collisions_enemy_playerbullets(sprite1=self, its_enemy4_type=True)

        if self.start_timing == True:
            self.timing_to_mine_explosion -= 1
            if self.timing_to_mine_explosion in self.its_on_lis:
                self.image = enemy4_on_img
                self.image.set_colorkey(BLACK)
            elif self.timing_to_mine_explosion in self.its_off_lis:
                self.image = enemy4_off_img
            print(self.timing_to_mine_explosion)


# stalker enemy
class Enemy2(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = enemy_guided_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH*(2/3) + random.randrange(self.rect.width, self.rect.width + 1)
        self.rect.y = (HEIGHT+self.rect.height) #random.randrange(-self.rect.height, HEIGHT + self.rect.height)
        self.lives = 3
        self.speed = 2.5
        self.score_value = 30

    def stalkPlayer(self, player=player):
        xdiff = (player.rect.x + player.rect.width/2) - self.rect.x - self.rect.width/2
        ydiff = (player.rect.y + 41/2) - self.rect.y - 55/2

        magnitude = math.sqrt(float(xdiff ** 2 + ydiff ** 2))
        numFrames = int(magnitude/self.speed)

        # it prevents that xmove or ymove get a division by zero
        if numFrames == 0:
            numFrames = 1

        xmove = xdiff/numFrames
        ymove = ydiff/numFrames

        self.rect.x += xmove
        self.rect.y += ymove

    def update(self, screen=screen, player=player):
        if self.lives < 0:
            self.kill()
            score_lis.append(self.score_value)
        self.stalkPlayer(player)

        screen.blit(self.image, self.rect)

        detect_collisions_enemy_playerbullets(self)

# stalker_y enemy shooter
class Enemy3(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = enemy_guided_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH - self.rect.width #WIDTH*(2.5/3) + random.randrange(self.rect.width, self.rect.width + 1)
        self.rect.y = (HEIGHT+self.rect.height) #random.randrange(-self.rect.height, HEIGHT + self.rect.height)
        self.lives = 17
        self.speed = 1.5
        self.score_value = 50
        self.weapon_delay = 30
        self.shooted = False

    def stalkPlayer(self, player=player):
        ydiff = (player.rect.y + 41/2) - self.rect.y - 55/2

        magnitude = math.sqrt(float(ydiff ** 2))
        numFrames = int(magnitude/self.speed)

        # it prevents that ymove get a division by zero
        if numFrames == 0:
            numFrames = 1

        ymove = ydiff/numFrames

        self.rect.y += ymove

    def update(self, screen=screen, player=player):
        if self.lives < 0:
            self.kill()
            score_lis.append(self.score_value)
        self.stalkPlayer(player)

        screen.blit(self.image, self.rect)

        if 0 <= abs(player.rect[1] - self.rect[1]) <= 14 and self.weapon_delay >= 30 and player.is_alive == True:
            self.shoot()
            self.shooted = True

        if self.shooted == True:
            self.weapon_delay -= 1

        if self.weapon_delay <= 0:
            self.shooted = False
            self.weapon_delay = 30

        detect_collisions_enemy_playerbullets(self)

    def shoot(self):
        enemy3_bullet = Enemy3Bullet(self.rect.centery, self.rect.left)
        all_sprites.add(enemy3_bullet)
        enemy3_bullet_g.add(enemy3_bullet)

# Power_ups;
class power_up_1_icon(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = power_up_1_icon_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centery = random.randrange(0 + self.rect.height, HEIGHT - self.rect.height)
        self.rect.centerx = random.randrange(WIDTH + self.rect.width, WIDTH + (WIDTH/2))
        self.speedx = -1

    def update(self):
        self.rect.x += self.speedx

class power_up_1_1_icon(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = power_up_1_icon_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centery = random.randrange(0 + self.rect.height, HEIGHT - self.rect.height)
        self.rect.centerx = random.randrange(WIDTH + self.rect.width, WIDTH + (WIDTH/2))
        self.speedx = -1

    def update(self):
        self.rect.x += self.speedx

power_up_1_delay_lis = []
class power_up_1(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = power_up1_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = player.rect.x + player.rect.width #WIDTH * (2 / 3) + random.randrange(self.rect.width, self.rect.width + 1)
        self.rect.y = player.rect.y #(HEIGHT + self.rect.height)  # random.randrange(-self.rect.height, HEIGHT + self.rect.height)
        self.speed = 4.5

    def power_up_stalk(self, player=player):
        if player.is_alive == False:
            self.kill()
        xdiff = (player.rect.x + player.rect.width/2) - self.rect.x - self.rect.width/2
        ydiff = (player.rect.y + 41) - self.rect.y + 5

        magnitude = math.sqrt(float(xdiff ** 2 + ydiff ** 2))
        numFrames = int(magnitude/self.speed)

        # it prevents that xmove or ymove get a division by zero
        if numFrames == 0:
            numFrames = 1

        xmove = xdiff/numFrames
        ymove = ydiff/numFrames

        self.rect.x += xmove
        self.rect.y += ymove

    def shoot(self):
        power_up_1_basic_bullet = power_up_1_Bullet(self.rect.centery, self.rect.right)
        all_sprites.add(power_up_1_basic_bullet)
        power_up_1_bullet_g.add(power_up_1_basic_bullet)
        self.atackdamage = 1.5

    def update(self, screen=screen, player=player):
        self.power_up_stalk(player)

        screen.blit(self.image, self.rect)

        Keystate = pygame.key.get_pressed()
        if Keystate[pygame.K_9]:
            power_up_1_delay_lis.append(1)
            if sum(power_up_1_delay_lis) >= 10:
                self.shoot()
                power_up_1_delay_lis.clear()

power_up_1_1_delay_lis = []
class power_up_1_1(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = power_up1_1_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = player.rect.x + player.rect.width #WIDTH * (2 / 3) + random.randrange(self.rect.width, self.rect.width + 1)
        self.rect.y = player.rect.y #(HEIGHT + self.rect.height)  # random.randrange(-self.rect.height, HEIGHT + self.rect.height)
        self.speed = 4.5

    def power_up_stalk(self, player=player):
        if player.is_alive == False:
            self.kill()
        xdiff = (player.rect.x + player.rect.width/2) - self.rect.x - self.rect.width/2
        ydiff = (player.rect.y + 41) - self.rect.y - 66

        magnitude = math.sqrt(float(xdiff ** 2 + ydiff ** 2))
        numFrames = int(magnitude/self.speed)

        # it prevents that xmove or ymove get a division by zero
        if numFrames == 0:
            numFrames = 1

        xmove = xdiff/numFrames
        ymove = ydiff/numFrames

        self.rect.x += xmove
        self.rect.y += ymove

    def shoot(self):
        power_up_1_1_basic_bullet = power_up_1_Bullet(self.rect.centery, self.rect.right)
        all_sprites.add(power_up_1_1_basic_bullet)
        power_up_1_1_bullet_g.add(power_up_1_1_basic_bullet)
        self.atackdamage = 1.5

    def update(self, screen=screen, player=player):
        self.power_up_stalk(player)

        screen.blit(self.image, self.rect)

        Keystate = pygame.key.get_pressed()
        if Keystate[pygame.K_9]:
            power_up_1_1_delay_lis.append(1)
            if sum(power_up_1_1_delay_lis) >= 10:
                self.shoot()
                power_up_1_1_delay_lis.clear()

# bullet class from the power_up_1;
class power_up_1_Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = power_up_1_basic_bullet_img
        self.image.set_colorkey(BLACK)
        #self.damage = 1.5
        self.rect = self.image.get_rect()
        self.rect.left = y
        self.rect.centery = x
        self.speedx = 15

    def update(self):
        self.rect.x += self.speedx
        # delet the bullet if it try to go out of the right of the screen
        if self.rect.right >= WIDTH:
            self.kill()

# beam_things;
"""beam_charge_obj = CanonCharge()
all_sprites.add(beam_charge_obj)"""

# boss classes
class Boss(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = boss_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH + self.rect.width
        self.rect.y = HEIGHT - HEIGHT/(3/2.8)
        self.lives = 1
        self.speedx = -30
        self.score_value = 10

    def update(self):
        if self.rect.right <= WIDTH + 12:
            self.rect.x = self.rect.x
        else:
            self.rect.x += self.speedx

# boss shield class
class BossShield(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = boss_shield_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH + self.rect.width
        self.rect.y = HEIGHT - HEIGHT/(3/2.8)
        self.lives = 1
        self.speedx = -30
        self.score_value = 10

    def update(self):
        if self.rect.right <= WIDTH + 12:
            self.rect.x = self.rect.x
        else:
            self.rect.x += self.speedx

#creating boss objects
boss = Boss()
boss_shield = BossShield()

def collisions_obj_group(sprite1, group, its_enemy4_type=False):
    hits_Bullets10 = pygame.sprite.spritecollide(sprite1, group, True)
    if its_enemy4_type == False:
        if len(hits_Bullets10) >= 1 and group == bullets:
            sprite1.lives -= player.atackdamage
        if len(hits_Bullets10) >= 1 and group == power_up_1_bullet_g:
            sprite1.lives -= power_up_gun09.atackdamage
        if len(hits_Bullets10) >= 1 and group == power_up_1_1_bullet_g:
            sprite1.lives -= power_up_gun10.atackdamage
    else:
        if len(hits_Bullets10) >= 1 and group == bullets:
            sprite1.lives -= player.atackdamage
            sprite1.start_timing = True
        if len(hits_Bullets10) >= 1 and group == power_up_1_bullet_g:
            sprite1.lives -= power_up_gun09.atackdamage
            sprite1.start_timing = True
        if len(hits_Bullets10) >= 1 and group == power_up_1_1_bullet_g:
            sprite1.lives -= power_up_gun10.atackdamage
            sprite1.start_timing = True
def detect_collisions_enemy_playerbullets(sprite1, its_enemy4_type=False):
    if its_enemy4_type == False:
        collisions_obj_group(sprite1, bullets)
        collisions_obj_group(sprite1, power_up_1_bullet_g)
        collisions_obj_group(sprite1, power_up_1_1_bullet_g)
    else:
        collisions_obj_group(sprite1, bullets, its_enemy4_type=True)
        collisions_obj_group(sprite1, power_up_1_bullet_g, its_enemy4_type=True)
        collisions_obj_group(sprite1, power_up_1_1_bullet_g, its_enemy4_type=True)

def invoke_enemy(Class, amount, its_enemy4_type=False):
    if its_enemy4_type == True:
        for i in range(amount):
            obj = Class()
            all_sprites.add(obj)
    if its_enemy4_type == False:
        for i in range(amount):
            obj = Class()
            mobs.add(obj)
            all_sprites.add(obj)


# Game loop;
running = True
while running == True:

    # bliting background
    relative_background_x_position = background_x_position % background.get_rect().width
    screen.blit(background, (relative_background_x_position - background.get_rect().width, background_y_position))
    screen.blit(background, (relative_background_x_position, background_y_position))
    background_x_position -= 1

    # stage time
    STAGE_TIME += 1/FPS

#_______________________________________________________________________________________________________________________

    # Creating power_ups and invoking them
    if 0 <= STAGE_TIME <= 0.02: # do not forget to adjust it to the correct time

        power_up_1_icon_obj = power_up_1_icon()
        player_power_up_1_g.add(power_up_1_icon_obj)
        all_sprites.add(power_up_1_icon_obj)

        power_up_1_1_icon_obj = power_up_1_1_icon()
        player_power_up_1_1_g.add(power_up_1_1_icon_obj)
        all_sprites.add(power_up_1_1_icon_obj)

    # Colision of player with power_ups icons
    power_ups_hits_player = pygame.sprite.spritecollide(player, player_power_up_1_g, True)
    if power_ups_hits_player:
        power_up_gun09 = power_up_1()
        all_sprites.add(power_up_gun09)

    power_ups_hits_player = pygame.sprite.spritecollide(player, player_power_up_1_1_g, True)
    if power_ups_hits_player:
        power_up_gun10 = power_up_1_1()
        all_sprites.add(power_up_gun10)

#_______________________________________________________________________________________________________________________

    # Creating Enemies and invoking them
    """if 3 <= STAGE_TIME <= 3.02:
        invoke_enemy(Enemy2, 1)"""


#_______________________________________________________________________________________________________________________

    # keep this runnig at the right speed
    clock.tick(FPS)

    # Process input (events)
    for event in pygame.event.get():
        # check for closing the window
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_9:
                activated = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_9:
                release = True
                loading = False
        if activated == True and loading == False and release == True and int(sum(lis_charge_energy)) >= 4:
            player.shoot()
            lis_charge_energy.clear()
            release = False
            activated = False


    # Updade
    all_sprites.update()

#_______________________________________________________________________________________________________________________

    # Check if the mob hits the player; Checking if Enemy bullet coliddes with the player
    # returns a list that recive True when a sprite(player) collides with anything from a group(mobs)
    mobs_hits_player = pygame.sprite.spritecollide(player, mobs, False)
    mobs_bullets_hits_player = pygame.sprite.spritecollide(player, enemy3_bullet_g, False)
    #print(bool(hits_player), "BEFORE")
    if (mobs_hits_player or mobs_bullets_hits_player) and colliding == True: # that means if a mob hit the player the list hits will recive True
        #print(bool(hits_player), "AFTER")
        player.lives -= 1
        if sum(live_lis) > 0:
            live_lis.append(-1)
        colliding = False
        #print("VIDAS = ", player.lives)
    if colliding == False:
        tr_controll -= 1
        player.image = space_ship_player_respawn
        player.image.set_colorkey(BLACK)
        #print("TEMPO = ", tr_controll)
    if tr_controll <= 0:
        colliding = True
        tr_controll = 140
        player.image = space_ship_player
        #print("TEMPO = ", tr_controll)

#_______________________________________________________________________________________________________________________

    # Draw / render
    all_sprites.draw(screen)
    score = str(sum(score_lis))
    lives = str(sum(live_lis))
    beam_charge = str(int(sum(lis_charge_energy)))
    draw_score(text=("HI - " + score))
    draw_lives(text=("LIVES - " + lives))
    draw_beam_charge(text=("BEAM"))

    # *after* drawing everything, flip the display
    pygame.display.flip()

# close everything up
pygame.quit()