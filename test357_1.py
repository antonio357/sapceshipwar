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
GREEN = (55, 238, 2)

# set up assets folders
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, "images")

# varialbles to control the respawntime - 1.1.3
colliding = True
tr_controll = 140

# these variables works with - 1.1.3
activated = False
loading = False
release = False

# this lis acumulates one`s (1) to charge energy to the advanced_shoot
lis_charge_energy = []

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



    def update(self):
        if self.lives < 0:
            self.kill()
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
        if Keystate[pygame.K_9] and len(lis_charge_energy) <= 60:
            lis_charge_energy.append(1)
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
        advanced_bullet = Bullet(self.rect.centery, self.rect.right-(self.rect.right/2))
        if 1 <= len(lis_charge_energy) < 60:
            all_sprites.add(basic_bullet)
            bullets.add(basic_bullet)
            self.atackdamage = 1
        if len(lis_charge_energy) >= 60:
            all_sprites.add(advanced_bullet)
            bullets.add(advanced_bullet)
            self.atackdamage = 10

# importing enemies from enemies.py
from enemies import Enemy1

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        if len(lis_charge_energy) >= 60:
            self.image = advanced_bullet_img
            self.image.set_colorkey(BLACK)
            self.damage = 10
        if 1 <= len(lis_charge_energy) < 60:
            self.image = space_ship_player_basic_bullet
            self.image.set_colorkey(BLACK)
            self.damage = 1
        self.rect = self.image.get_rect()
        self.rect.left = y
        self.rect.centery = x
        self.speedx = 12

    def update(self):
        self.rect.x += self.speedx
        # delet the bullet if it try to go out of the right of the screen
        if self.rect.right >= WIDTH:
            self.kill()

# initializate pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("CODING GAME...")
clock = pygame.time.Clock()

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

# Load all game grafhics
space_ship_player = pygame.image.load(os.path.join(img_folder, "player_space_ship.png")).convert()
space_ship_player_respawn = pygame.image.load(os.path.join(img_folder, "testing.png")).convert()
space_ship_player_mini_img = pygame.transform.scale(space_ship_player, (25, 19))
space_ship_player_mini_img.set_colorkey(BLACK)
#space_ship_basic_enemy = pygame.image.load(os.path.join(img_folder, "basic_enemy.png")).convert()
background = pygame.image.load(os.path.join(img_folder, "r-type_2_background.png")).convert()
space_ship_player_basic_bullet = pygame.image.load(os.path.join(img_folder, "P_bullet.png")).convert()
advanced_bullet_img = pygame.image.load(os.path.join(img_folder, "P_special_bullet1.png")).convert()
#enemy_explosion = pygame.image.load(os.path.join(img_folder, "enemy_exploding.png")).convert
enemy_guided_img = pygame.image.load(os.path.join(img_folder, "alien_spaceship_invasion_mine.png")).convert()


# Groups and the sprites;
all_sprites = pygame.sprite.Group()
enemy1_group = pygame.sprite.Group()
enemy2_group = pygame.sprite.Group()
enemy3_group = pygame.sprite.Group()
enemy4_group = pygame.sprite.Group()
enemy5_group = pygame.sprite.Group()
enemy6_group = pygame.sprite.Group()
enemy7_group = pygame.sprite.Group()
enemy8_group = pygame.sprite.Group()
enemy9_group = pygame.sprite.Group()
enemy10_group = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
mobs = pygame.sprite.Group()

# Background;
background_x_position = 0
background_x_position_boss = 0
background_y_position = 0
background_y_position_boss = 0
background_boss_position = +3*3
STAGE_TIME = 0

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

# stalker.y enemy shooter
class Enemy3(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = enemy_guided_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH*(2/3) + random.randrange(self.rect.width, self.rect.width + 1)
        self.rect.y = (HEIGHT+self.rect.height) #random.randrange(-self.rect.height, HEIGHT + self.rect.height)
        self.lives = 17
        self.speed = 2.5
        self.score_value = 50

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
    # Creating Enemy1 and invoking them

    if 1 <= STAGE_TIME <= 1.02: #or 8 <= STAGE_TIME <= 8.02:

        enemy10 = Enemy2()
        enemy10_group.add(enemy10)
        all_sprites.add(enemy10_group)
        mobs.add(enemy10_group)

        enemy9 = Enemy3()
        enemy9_group.add(enemy9)
        all_sprites.add(enemy9_group)
        mobs.add(enemy9_group)

        """enemy1 = Enemy1()
        enemy1_group.add(enemy1)
        all_sprites.add(enemy1_group)

        enemy2 = Enemy1()
        enemy2_group.add(enemy2)
        all_sprites.add(enemy2_group)

        enemy3 = Enemy1()
        enemy3_group.add(enemy3)
        all_sprites.add(enemy3_group)

        enemy4 = Enemy1()
        enemy4_group.add(enemy4)
        all_sprites.add(enemy4_group)

        enemy5 = Enemy1()
        enemy5_group.add(enemy5)
        all_sprites.add(enemy5_group)

        enemy6 = Enemy1()
        enemy6_group.add(enemy6)
        all_sprites.add(enemy6_group)

        enemy7 = Enemy1()
        enemy7_group.add(enemy7)
        all_sprites.add(enemy7_group)

        enemy8 = Enemy1()
        enemy8_group.add(enemy8)
        all_sprites.add(enemy8_group)"""
#_______________________________________________________________________________________________________________________

    """img_background_begining_position_on_screen = pygame.draw.line(screen, GREEN, (relative_background_x_position, background_y_position), (relative_background_x_position, HEIGHT), 3)
    img_background_begining_position_on_screen
    print(lis_time_enemy_appear)
    print(STAGE_TIME)"""

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
        if activated == True and loading == False and release == True and len(lis_charge_energy) >= 4:
            player.shoot()
            lis_charge_energy.clear()
            release = False
            activated = False


    # Updade
    all_sprites.update()

#_______________________________________________________________________________________________________________________
#Checking if Enemy1 coliddes with bullets

    hits_Bullets10 = pygame.sprite.groupcollide(enemy10_group, bullets, False, True)
    if len(hits_Bullets10) >= 1:
        enemy10.lives -= player.atackdamage

    hits_Bullets9 = pygame.sprite.groupcollide(enemy9_group, bullets, False, True)
    if len(hits_Bullets9) >= 1:
        enemy9.lives -= player.atackdamage

    """hits_Bullets1 = pygame.sprite.groupcollide(enemy1_group, bullets, False, True)
    if len(hits_Bullets1) >= 1:
        enemy1.lives -= player.atackdamage

    hits_Bullets2 = pygame.sprite.groupcollide(enemy2_group, bullets, False, True)
    if len(hits_Bullets2) >= 1:
        enemy2.lives -= player.atackdamage

    hits_Bullets3 = pygame.sprite.groupcollide(enemy3_group, bullets, False, True)
    if len(hits_Bullets3) >= 1:
        enemy3.lives -= player.atackdamage

    hits_Bullets4 = pygame.sprite.groupcollide(enemy4_group, bullets, False, True)
    if len(hits_Bullets4) >= 1:
        enemy4.lives -= player.atackdamage

    hits_Bullets5 = pygame.sprite.groupcollide(enemy5_group, bullets, False, True)
    if len(hits_Bullets5) >= 1:
        enemy5.lives -= player.atackdamage

    hits_Bullets6 = pygame.sprite.groupcollide(enemy6_group, bullets, False, True)
    if len(hits_Bullets6) >= 1:
        enemy6.lives -= player.atackdamage

    hits_Bullets7 = pygame.sprite.groupcollide(enemy7_group, bullets, False, True)
    if len(hits_Bullets7) >= 1:
        enemy7.lives -= player.atackdamage

    hits_Bullets8 = pygame.sprite.groupcollide(enemy8_group, bullets, False, True)
    if len(hits_Bullets8) >= 1:
        enemy8.lives -= player.atackdamage

    hits_Bullets1 = pygame.sprite.groupcollide(enemy1_group, bullets, False, False)
    if len(hits_Bullets1) >= 1:
        enemy1.lives -= player.atackdamage


    hits_Bullets2 = pygame.sprite.groupcollide(enemy2_group, bullets, False, False)
    if len(hits_Bullets2) >= 1:
        enemy2.lives -= player.atackdamage

    hits_Bullets3 = pygame.sprite.groupcollide(enemy3_group, bullets, False, False)
    if len(hits_Bullets3) >= 1:
        enemy3.lives -= player.atackdamage

    hits_Bullets4 = pygame.sprite.groupcollide(enemy4_group, bullets, False, False)
    if len(hits_Bullets4) >= 1:
        enemy4.lives -= player.atackdamage

    hits_Bullets5 = pygame.sprite.groupcollide(enemy5_group, bullets, False, False)
    if len(hits_Bullets5) >= 1:
        enemy5.lives -= player.atackdamage

    hits_Bullets6 = pygame.sprite.groupcollide(enemy6_group, bullets, False, False)
    if len(hits_Bullets6) >= 1:
        enemy6.lives -= player.atackdamage

    hits_Bullets7 = pygame.sprite.groupcollide(enemy7_group, bullets, False, False)
    if len(hits_Bullets7) >= 1:
        enemy7.lives -= player.atackdamage

    hits_Bullets8 = pygame.sprite.groupcollide(enemy8_group, bullets, False, False)
    if len(hits_Bullets8) >= 1:
        enemy8.lives -= player.atackdamage"""
#_______________________________________________________________________________________________________________________

    # Check if the mob hits the player
    # returns a list that recive True when a sprite(player) collides with anything from a group(mobs)
    hits_player = pygame.sprite.spritecollide(player, mobs, False)
    #print(bool(hits_player), "BEFORE")
    if hits_player and colliding == True: # that means if a mob hit the player the list hits will recive True
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

    # Draw / render
    all_sprites.draw(screen)
    score = str(sum(score_lis))
    lives = str(sum(live_lis))
    draw_score(text=("HI - " + score))
    draw_lives(text=("LIVES - " + lives))

    # *after* drawing everything, flip the display
    pygame.display.flip()

# close everything up
pygame.quit()