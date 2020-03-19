# importing necessary things
import pygame
import random
import os
import math
"""OBS: IT'S important to notice the relation between the time of the real world and the game world =>>> 
1’s == 0.9189331925006573 or 65 of STAGE_TIME from the game"""

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
RED = (236, 0, 6)

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
boss_weak_point_img_folder = os.path.join(boss_folder, "boss_weak_point_sprite_sheet")


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
space_ship_basic_enemy = pygame.image.load(os.path.join(img_folder, "Enemy1.png")).convert()
boss_weak_point_img = pygame.image.load(os.path.join(boss_weak_point_img_folder, "18.png")).convert()
boss_shield_img = pygame.image.load(os.path.join(boss_folder, "shield.png")).convert()
boss_bullet1_img = pygame.image.load(os.path.join(boss_folder, "ball.png")).convert()

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
boss_weakpoint_group = pygame.sprite.Group()
boss_bullets_group = pygame.sprite.Group()
boss_dark_matter_group = pygame.sprite.Group()
player_g = pygame.sprite.Group()

# varialbles to control the respawntime - 1.1.3
colliding = True
tr_controll = 140*4

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
        self.radius = int(self.rect.height/2)
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)


    def update(self):
        if self.lives < 0:
            self.kill()
            self.is_alive = False
            """global running
            running = False"""
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
            #basic_bullet.radius = int(basic_bullet.rect.height / 2)
            #pygame.draw.circle(basic_bullet.image, RED, basic_bullet.rect.center, basic_bullet.radius)
        if int(sum(lis_charge_energy)) >= 200:
            all_sprites.add(advanced_bullet)
            bullets.add(advanced_bullet)
            self.atackdamage = 10
            #advanced_bullet.radius = int(advanced_bullet.rect.height / 2 - 20)
            #pygame.draw.circle(advanced_bullet.image, RED, advanced_bullet.rect.center, advanced_bullet.radius)

# create player_obj and addint it to all_sprites
player = Player()
all_sprites.add(player)
player_g.add(player)

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
            self.rect = self.image.get_rect()
            self.rect.left = y
            self.rect.centery = x
            self.speedx = 15
            #self.radius = int(self.rect.height / 2)
            #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        if 1 <= int(sum(lis_charge_energy)) < 200:
            self.image = space_ship_player_basic_bullet
            self.image.set_colorkey(BLACK)
            # get back
            #self.damage = 1
            self.rect = self.image.get_rect()
            self.rect.left = y
            self.rect.centery = x
            self.speedx = 15
            #self.radius = int(self.rect.height / 2)
            #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)

        self.radius = int(self.rect.height / 2)
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)


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
        self.rect.x = random.randrange(WIDTH + self.rect.width, WIDTH + WIDTH/2)
        self.speedx = -1
        self.score_value = 5
        self.lives = 15
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

        #print(self.rect.centerx, self.rect.centery)

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
            #print(self.timing_to_mine_explosion)


# stalker enemy
class Enemy2(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = enemy_guided_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH*(2/3) + random.randrange(self.rect.width, self.rect.width + 1)
        self.rect.y = (HEIGHT+self.rect.height) #random.randrange(-self.rect.height, HEIGHT + self.rect.height)
        self.lives = 5
        self.speed = 2.5
        self.score_value = 60
        self.timing_to_start_stalking = 195

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
            global enemy2_its_alive
            enemy2_its_alive = False
            global STAGE_TIME
            if STAGE_TIME >= 7410:
                enemies_lis[0] = False

        if self.timing_to_start_stalking > 0:
            self.timing_to_start_stalking -= 1

        if self.timing_to_start_stalking <= 0:
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
        self.rect.y = (-self.rect.height) #random.randrange(-self.rect.height, HEIGHT + self.rect.height)
        self.lives = 17
        self.speed = 1.5
        self.score_value = 50
        self.weapon_delay = 30
        self.shooted = False
        self.timing_to_start_stalking = 195

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
            global enemy3_its_alive
            enemy3_its_alive = False
            global STAGE_TIME
            if STAGE_TIME >= 7410:
                enemies_lis[1] = False
        #self.stalkPlayer(player)

        if self.timing_to_start_stalking > 0:
            self.timing_to_start_stalking -= 1

        if self.timing_to_start_stalking <= 0:
            self.stalkPlayer(player)

        screen.blit(self.image, self.rect)

        if 0 <= abs(player.rect.centery - self.rect.centery) <= 14 and self.weapon_delay >= 30 and player.is_alive == True:
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
        self.radius = int(self.rect.height / 2)

    def update(self):
        self.rect.x += self.speedx
        # delet the bullet if it try to go out of the right of the screen
        if self.rect.right >= WIDTH:
            self.kill()

# beam_things;
"""beam_charge_obj = CanonCharge()
all_sprites.add(beam_charge_obj)"""

# boss classes
boss_speed = -5
boss_x_position_respawn = 1312
boss_y_position_respawn = 40
boss_its_alive = True
class Boss(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = boss_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.height/2 - 70)
        #pygame.draw.circle(self.image, RED, (self.rect.x + int(self.rect.width/2) + 140, self.rect.y + int(self.rect.height/2)), self.radius)
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = boss_x_position_respawn #WIDTH + self.rect.width
        self.rect.y = boss_y_position_respawn #HEIGHT - HEIGHT/(3/2.8)
        self.lives = 1
        self.speedx = boss_speed
        self.score_value = 101654687651
        self.weapon_delay = 30 * 5
        self.shooted = False
        self.can_shoot = False

    def update(self):
        if self.rect.left <= 562:
            self.rect.x = self.rect.x
            self.can_shoot = True
        else:
            self.rect.x += self.speedx

        #detect_collisions_enemy_playerbullets(sprite1=self, its_boss=True)
        global boss_its_alive
        if self.weapon_delay >= 30 * 5 and player.is_alive == True and self.can_shoot == True and boss_its_alive == True:
            self.shoot()
            self.shooted = True

            """ diminuindo o fps"""
            """global FPS
            FPS = 15"""

        if self.shooted == True:
            self.weapon_delay -= 1

        if self.weapon_delay <= 0:
            self.shooted = False
            self.weapon_delay = 30 * 5

        #detect_collisions_enemy_playerbullets(self)

    def shoot(self):
        boss_bullet1 = BossWeakPointBullet2(player.rect.centerx, player.rect.centery)
        all_sprites.add(boss_bullet1)
        boss_bullets_group.add(boss_bullet1)

from enemies import sprite_boss_magic_bullet
class BossWeakPointBullet2(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.timing = 150
        self.image = sprite_boss_magic_bullet(self.timing)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speedx = 1
        self.radius = 128/2#int(self.rect.height / 3.7)
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)

    def update(self):
        #self.rect.x += self.speedx
        #print(self.timing)
        self.timing -= 1
        # delet the bullet if it try to go out of the right of the screen
        if self.rect.right <= 0:
            self.kill()

        if self.timing <= 1:
            self.kill()

        self.image = sprite_boss_magic_bullet(self.timing)
        self.image.set_colorkey(BLACK)

        if self.timing <= 90:
            #print("ta_colidindo", self.timing)
            detect_collisions_BossShield_player("boss_magicbullet")

# boss shield class
from enemies import sprite_shield_deteriorarion_animation
boss_shield_its_on = False
class BossShield(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = boss_shield_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.height / 2 - 20)
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = WIDTH + self.rect.width
        self.rect.y = HEIGHT - HEIGHT/(3/2.8)
        self.lives = 200
        self.speedx = boss_speed
        #self.score_value = 10
        self.timing_to_respawn_back = 200

    def update(self):
        #print(self.lives, self.timing_to_respawn_back)
        #print(self.rect.x, self.rect.y)
        if self.lives >= 1:
            self.image = sprite_shield_deteriorarion_animation(int(self.lives))
            self.image.set_colorkey(BLACK)
            global boss_shield_its_on
            boss_shield_its_on = True
        elif self.lives <= 0:
            #self.kill()
            self.image = sprite_shield_deteriorarion_animation(int(self.lives))
            self.image.set_colorkey(BLACK)
            boss_shield_its_on = False
            self.timing_to_respawn_back -= 1
            if self.timing_to_respawn_back <= 0:
                self.lives = 200
                self.timing_to_respawn_back = 200
        if self.rect.left <= 562:
            self.rect.x = self.rect.x
        else:
            self.rect.x += self.speedx

        if boss_shield_its_on == True:
            detect_collisions_enemy_playerbullets(self, its_boss=True)

class BossWeakPoint1(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = boss_weak_point_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.height / 2 - 3)
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = 1650.5053380782917
        self.rect.y = HEIGHT - HEIGHT / (3 / 2.3)
        self.lives = 30
        self.speedx = boss_speed
        self.score_value = 10000
        self.weapon_delay = 30 * 3
        self.shooted = False
        self.can_shoot = False

    def update(self):
        if self.rect.left <= 707:
            self.rect.x = self.rect.x
            self.can_shoot = True
        else:
            self.rect.x += self.speedx

        if self.lives <= 0:
            self.kill()
            score_lis.append(self.score_value)
            boss_weakpoint_lis[0] = False

        detect_collisions_enemy_playerbullets(self, its_boss=True)

        if 0 <= abs(player.rect.centery - self.rect.centery) <= 30 and self.weapon_delay >= 30 * 3 and player.is_alive == True and self.can_shoot == True:
            self.shoot()
            self.shooted = True

        if self.shooted == True:
            self.weapon_delay -= 1

        if self.weapon_delay <= 0:
            self.shooted = False
            self.weapon_delay = 30 * 3

        detect_collisions_enemy_playerbullets(self)

    def shoot(self):
        bossweakpoint_bullet1 = BossWeakPointBullet1(self.rect.centery, self.rect.left)
        all_sprites.add(bossweakpoint_bullet1)
        enemy3_bullet_g.add(bossweakpoint_bullet1)

class BossWeakPoint2(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = boss_weak_point_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.height / 2 - 3)
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = 1510
        self.rect.y = HEIGHT - HEIGHT / (3 / 1.77)
        self.lives = 30
        self.speedx = boss_speed
        self.score_value = 10000
        self.weapon_delay = 30 * 3
        self.shooted = False
        self.can_shoot = False

    def update(self):
        if self.rect.left <= 647:
            self.rect.x = self.rect.x
            self.can_shoot = True
        else:
            self.rect.x += self.speedx

        if self.lives <= 0:
            self.kill()
            score_lis.append(self.score_value)
            boss_weakpoint_lis[1] = False

        detect_collisions_enemy_playerbullets(self, its_boss=True)

        if 0 <= abs(player.rect.centery - self.rect.centery) <= 14 and self.weapon_delay >= 30 * 3 and player.is_alive == True and self.can_shoot == True:
            self.shoot()
            self.shooted = True

        if self.shooted == True:
            self.weapon_delay -= 1

        if self.weapon_delay <= 0:
            self.shooted = False
            self.weapon_delay = 30 * 3

        detect_collisions_enemy_playerbullets(self)

    def shoot(self):
        bossweakpoint_bullet1 = BossWeakPointBullet1(self.rect.centery, self.rect.left)
        all_sprites.add(bossweakpoint_bullet1)
        enemy3_bullet_g.add(bossweakpoint_bullet1)

class BossWeakPoint3(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = boss_weak_point_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.height / 2 - 3)
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = 1650.5053380782917
        self.rect.y = HEIGHT - HEIGHT / (3 / 1.23)
        self.lives = 30
        self.speedx = boss_speed
        self.score_value = 10000
        self.weapon_delay = 30*3
        self.shooted = False
        self.can_shoot = False

    def update(self):
        if self.rect.left <= 707:
            self.rect.x = self.rect.x
            self.can_shoot = True
        else:
            self.rect.x += self.speedx

        if self.lives <= 0:
            self.kill()
            score_lis.append(self.score_value)
            boss_weakpoint_lis[2] = False

        detect_collisions_enemy_playerbullets(self, its_boss=True)

        if 0 <= abs(player.rect.centery - self.rect.centery) <= 14 and self.weapon_delay >= 30*3 and player.is_alive == True and self.can_shoot == True:
            self.shoot()
            self.shooted = True

        if self.shooted == True:
            self.weapon_delay -= 1

        if self.weapon_delay <= 0:
            self.shooted = False
            self.weapon_delay = 30*3

        detect_collisions_enemy_playerbullets(self)

    def shoot(self):
        bossweakpoint_bullet1 = BossWeakPointBullet1(self.rect.centery, self.rect.left)
        all_sprites.add(bossweakpoint_bullet1)
        enemy3_bullet_g.add(bossweakpoint_bullet1)

class BossWeakPointBullet1(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = boss_bullet1_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.left = y
        self.rect.centery = x
        self.speedx = 10
        self.radius = int(self.rect.height / 3.7)
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)

    def update(self):
        self.rect.x -= self.speedx
        # delet the bullet if it try to go out of the right of the screen
        if self.rect.right <= 0:
            self.kill()

def collisions_obj_group(sprite1, group, its_enemy4_type=False, its_boss=False):
    if its_enemy4_type == False and its_boss == False:
        hits_Bullets10 = pygame.sprite.spritecollide(sprite1, group, True)
        if len(hits_Bullets10) >= 1 and group == bullets:
            sprite1.lives -= player.atackdamage
        if len(hits_Bullets10) >= 1 and group == power_up_1_bullet_g:
            sprite1.lives -= power_up_gun09.atackdamage
        if len(hits_Bullets10) >= 1 and group == power_up_1_1_bullet_g:
            sprite1.lives -= power_up_gun10.atackdamage
    if its_enemy4_type == True:
        hits_Bullets10 = pygame.sprite.spritecollide(sprite1, group, True)
        if len(hits_Bullets10) >= 1 and group == bullets:
            sprite1.lives -= player.atackdamage
            #sprite1.start_timing = True
        if len(hits_Bullets10) >= 1 and group == power_up_1_bullet_g:
            sprite1.lives -= power_up_gun09.atackdamage
            #sprite1.start_timing = True
        if len(hits_Bullets10) >= 1 and group == power_up_1_1_bullet_g:
            sprite1.lives -= power_up_gun10.atackdamage
            #sprite1.start_timing = True
    if its_boss == True:
        hits_Bullets1 = pygame.sprite.spritecollide(sprite1, group, True, pygame.sprite.collide_circle)
        if len(hits_Bullets1) >= 1 and group == bullets:
            sprite1.lives -= player.atackdamage
            #print("COLIDIU WITH BULLETS")
        if len(hits_Bullets1) >= 1 and group == power_up_1_bullet_g:
            sprite1.lives -= power_up_gun09.atackdamage
            #print("COLIDIU COM POWER_UP_09")
        if len(hits_Bullets1) >= 1 and group == power_up_1_1_bullet_g:
            sprite1.lives -= power_up_gun10.atackdamage
            #print("COLIDIU COM POWER_UP_10")

def detect_collisions_enemy_playerbullets(sprite1, its_enemy4_type=False, its_boss=False):
    if its_enemy4_type == False and its_boss == False:
        collisions_obj_group(sprite1, bullets)
        collisions_obj_group(sprite1, power_up_1_bullet_g)
        collisions_obj_group(sprite1, power_up_1_1_bullet_g)
    if its_enemy4_type == True:
        collisions_obj_group(sprite1, bullets, its_enemy4_type=True)
        collisions_obj_group(sprite1, power_up_1_bullet_g, its_enemy4_type=True)
        collisions_obj_group(sprite1, power_up_1_1_bullet_g, its_enemy4_type=True)
    if its_boss == True:
        collisions_obj_group(sprite1, bullets, its_boss=True)
        collisions_obj_group(sprite1, power_up_1_bullet_g, its_boss=True)
        collisions_obj_group(sprite1, power_up_1_1_bullet_g, its_boss=True)

def invoke_enemy(Class, amount=1, its_enemy4_type=False, its_boss_weakpoint=False, its_drak_matter=False, its_boss_shield=False):
    if its_enemy4_type == True:
        for i in range(amount):
            obj = Class()
            all_sprites.add(obj)
    if its_enemy4_type == False and its_boss_weakpoint == False and its_drak_matter == False and its_boss_shield == False:
        for i in range(amount):
            obj = Class()
            mobs.add(obj)
            all_sprites.add(obj)
    if its_boss_weakpoint == True:
        for i in range(amount):
            obj = Class()
            boss_weakpoint_group.add(obj)
            all_sprites.add(obj)
    if its_drak_matter == True:
        for i in range(amount):
            obj = Class()
            boss_dark_matter_group.add(obj)
            all_sprites.add(obj)
    if its_boss_shield == True:
        for i in range(amount):
            obj = Class()
            boss_shield_group.add(obj)
            all_sprites.add(obj)


def detect_collisions_BossShield_player(group):
    if group == "boss_darkmatter" :
        collision = pygame.sprite.spritecollide(player, boss_dark_matter_group, False, pygame.sprite.collide_circle)
    elif group == "boss_shield":
        collision = pygame.sprite.spritecollide(player, boss_shield_group, False, pygame.sprite.collide_circle)
    elif group == "boss_weakpoint":
        collision = pygame.sprite.spritecollide(player, boss_weakpoint_group, False, pygame.sprite.collide_circle)
    elif group == "boss_magicbullet":
        collision = pygame.sprite.spritecollide(player, boss_bullets_group, False, pygame.sprite.collide_circle)
    elif group == "mobs":
        collision = pygame.sprite.spritecollide(player, mobs, False)
    elif group == "enemy3_bullet":
        collision = pygame.sprite.spritecollide(player, enemy3_bullet_g, False)
    #boss_group_hits_player = pygame.sprite.spritecollide(player, boss_group, False, pygame.sprite.collide_circle)
    global colliding
    if collision and colliding == True:
        #print("usou a colisão correta")
        player.lives -= 1
        if sum(live_lis) > 0:
            live_lis.append(-1)
        colliding = False
    if colliding == False:
        global tr_controll
        tr_controll -= 1
        player.image = space_ship_player_respawn
        player.image.set_colorkey(BLACK)
    if tr_controll <= 0:
        colliding = True
        tr_controll = 140*4
        player.image = space_ship_player

# vars for the enemy1 get involked
enemy1_get_involked = 650

# vars for the enemy2 get involked
enemy2_its_alive = False

# vars for the enemy3 get involked
enemy3_its_alive = False

# vars for the enemy4 get involked
enemy3_get_involked = 3250

# it's a list to check if there are any enemy alive
enemies_lis = [True, True]

# it's a list to check if there are any boss weakpoint alive
boss_weakpoint_lis = [True, True, True]

# Game loop;
running = True
cadenciamento = 7
can_call_boss = False
while running == True:

    if boss_weakpoint_lis[0] == False and boss_weakpoint_lis[1] == False and boss_weakpoint_lis[2] == False:
        boss_its_alive = False # var to make the boss stop shooting at the player after the player wins


    # bliting background
    relative_background_x_position = background_x_position % background.get_rect().width
    screen.blit(background, (relative_background_x_position - background.get_rect().width, background_y_position))
    screen.blit(background, (relative_background_x_position, background_y_position))
    background_x_position -= 1

    # stage time
    STAGE_TIME += 1
    #print("STAGE_TIME=", STAGE_TIME)

#_______________________________________________________________________________________________________________________

    # Creating power_ups and invoking them
    if STAGE_TIME == 1950: # do not forget to adjust it to the correct time

        power_up_1_icon_obj = power_up_1_icon()
        player_power_up_1_g.add(power_up_1_icon_obj)
        all_sprites.add(power_up_1_icon_obj)

    if STAGE_TIME == 3900: # second power up
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

    # Creating Enemies and invoking enemies type, obs == 7410 should be equivalent to 1min and 54s
    if STAGE_TIME == enemy1_get_involked and enemy1_get_involked <= 7410:  # enemy1_get_involked == 650 should be equivalent to 10 seconds
        invoke_enemy(Enemy1, 3)
        enemy1_get_involked += 195 # this should be equivalent to sum 3 seconds more


    if STAGE_TIME >= 1950 and enemy2_its_alive == False and STAGE_TIME <= 7410: # 1950 should be equivalent to 20 seconds
        invoke_enemy(Enemy2, 1)
        enemy2_its_alive = True

    if STAGE_TIME >= 2600 and enemy3_its_alive == False and STAGE_TIME <= 7410: # 2600 should be equivalent to 30 seconds
        invoke_enemy(Enemy3, 1)
        enemy3_its_alive = True

    if STAGE_TIME == enemy3_get_involked and enemy3_get_involked <= 7410: # enemy1_get_involked == 3250 should be equivalent to 40 seconds
        invoke_enemy(Enemy4, 1)
        enemy3_get_involked += 195  # this should be equivalent to sum 3 seconds more

    if enemies_lis[0] == False and enemies_lis[1] == False and STAGE_TIME == 7860:
        invoke_enemy(Boss, 1, its_drak_matter=True)
        invoke_enemy(BossShield, 1, its_boss_shield=True)
        invoke_enemy(BossWeakPoint1, 1, its_boss_weakpoint=True)
        invoke_enemy(BossWeakPoint2, 1, its_boss_weakpoint=True)
        invoke_enemy(BossWeakPoint3, 1, its_boss_weakpoint=True)

    #if STAGE_TIME >=

    """if 8 <= STAGE_TIME <= 8.02:
        invoke_enemy(Enemy2, 1)
        invoke_enemy(Enemy1, 50)
        invoke_enemy(Enemy3, 2)
        invoke_enemy(Enemy4, 2)"""

    """if 1 <= cadenciamento <= 7:
        cadenciamento -= 1/FPS

    if cadenciamento < 1:
        cadenciamento = 7
        STAGE_TIME = 8"""

    """if 0 <= STAGE_TIME <= 0.02:
        can_call_boss = True
    if can_call_boss == True:
        invoke_enemy(Boss, 1, its_drak_matter=True)
        invoke_enemy(BossShield, 1, its_boss_shield=True)
        invoke_enemy(BossWeakPoint1, 1, its_boss_weakpoint=True)
        invoke_enemy(BossWeakPoint2, 1, its_boss_weakpoint=True)
        invoke_enemy(BossWeakPoint3, 1, its_boss_weakpoint=True)
        can_call_boss = False"""




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

    detect_collisions_BossShield_player(group="mobs")
    detect_collisions_BossShield_player(group="enemy3_bullet")
    detect_collisions_BossShield_player(group="boss_darkmatter")
    detect_collisions_BossShield_player(group="boss_weakpoint")
    if boss_shield_its_on == True:
        detect_collisions_BossShield_player(group="boss_shield")

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