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