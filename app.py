import pygame
import random
import os

FPS = 60
windowRunning = True
Width = 500
Height = 600

RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

score = 0
fontStyle = pygame.font.match_font('fantasy')

# Initialize game and create window
pygame.init()
# Initialize music
pygame.mixer.init()
window = pygame.display.set_mode((Width, Height))
clock = pygame.time.Clock()
pygame.display.set_caption("Space Survival")


# load image
bg_img = pygame.image.load(os.path.join("img", "bg.png")).convert()
player_img = pygame.image.load(os.path.join("player.png")).convert()
bullet_img = pygame.image.load(os.path.join("img", "bullet.png")).convert()

rockImgs = []
for i in range(1, 5):
    rockImgs.append(pygame.image.load(
        os.path.join("img", f"rock{i}.png")).convert())

expl_animation = {}
expl_animation['large'] = []
expl_animation['small'] = []
for i in range(9):
    expl_img = pygame.image.load(
        os.path.join("img", f"expl{i}.png")).convert()
    expl_img.set_colorkey(BLACK)
    expl_animation['large'].append(pygame.transform.scale(expl_img, (75, 75)))
    expl_animation['small'].append(pygame.transform.scale(expl_img, (30, 30)))

######################################################################################

# load music
shoot_sound = pygame.mixer.Sound(os.path.join("sound", "shoot.wav"))
rock_expl_sound = [pygame.mixer.Sound(os.path.join(
    "sound", "expl0.wav")), pygame.mixer.Sound(os.path.join("sound", "expl1.wav"))]

pygame.mixer.Sound.set_volume(shoot_sound, 0.1)

# background music
pygame.mixer.music.load(os.path.join("sound", "background.ogg"))
pygame.mixer.music.play(-1)

pygame.mixer.music.set_volume(0.05)

######################################################################################


def draw_health(surf, hp, x, y):
    if hp < 0:
        hp = 0
    barLen = 200
    barHeight = 12
    fill = (hp/100) * barLen
    outline_rect = pygame.Rect(x, y, barLen, barHeight)
    fill_rect = pygame.Rect(x, y, fill, barHeight)
    pygame.draw.rect(surf, RED, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)


def draw_score(surf, text, size, x, y):
    font = pygame.font.Font(fontStyle, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)


def new_rock():
    newRock = Rock()
    all_sprites.add(newRock)
    rocksGroup.add(newRock)

######################################################################################


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (50, 38))
        self.image.set_colorkey(((255, 255, 255)))
        self.radius = 19
        # get the player position
        self.rect = self.image.get_rect()

        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)

        self.rect.centerx = Width/2
        self.rect.bottom = Height - 10
        self.speed = 6

        self.health = 100

    def update(self):
        # set all the key on keyboard to False
        key_pressed = pygame.key.get_pressed()

        # if key pressed, then update the player's position
        if key_pressed[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if key_pressed[pygame.K_LEFT]:
            self.rect.x -= self.speed

        # make sure the sprite doesn't go out the window
        if self.rect.right > Width:
            self.rect.right = Width
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bulletsGroup.add(bullet)
        # play shoot sound when shoot
        shoot_sound.play()


class Rock(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.oriImage = random.choice(rockImgs)
        self.oriImage.set_colorkey(BLACK)
        self.image = self.oriImage.copy()

        # get the rock position
        self.rect = self.image.get_rect()

        self.radius = int(self.rect.width * 0.8 / 2)
        # pygame.draw.circle(self.image, (255, 0, 0), self.rect.center, self.radius)

        # random rock position and speed
        self.rect.x = random.randrange(0, Width - self.rect.width)
        self.rect.y = random.randrange(-120, -80)
        self.speedx = random.randrange(-3, 3)
        self.speedy = random.randrange(2, 7)
        self.totDeg = 0
        self.rotateDeg = random.randrange(-2, 3)

    def rotate(self):
        # prevent rotation exceed 360 degree
        self.totDeg += self.rotateDeg
        self.totDeg = self.totDeg % 360
        self.image = pygame.transform.rotate(self.oriImage, self.totDeg)

        center = self.rect.center
        # reset the position
        self.rect = self.image.get_rect()
        self.rect.center = center

    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        # reset the rock if the condition satisfy
        if self.rect.top > Height or self.rect.left > Width or self.rect.right < 0:
            self.rect.x = random.randrange(0, Width - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedx = random.randrange(-3, 3)
            self.speedy = random.randrange(2, 5)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(bullet_img, (10, 40))
        self.image.set_colorkey((0, 0, 0))
        # get the bullet position
        self.rect = self.image.get_rect()

        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = -10

    def update(self):
        self.rect.y += self.speed
        # if bullet is outside the window, kill it.
        if self.rect.bottom < 0:
            self.kill()


class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(bullet_img, (10, 40))
        self.image.set_colorkey((0, 0, 0))
        # get the bullet position
        self.rect = self.image.get_rect()

        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = -10

    def update(self):
        self.rect.y += self.speed
        # if bullet is outside the window, kill it.
        if self.rect.bottom < 0:
            self.kill()


all_sprites = pygame.sprite.Group()
rocksGroup = pygame.sprite.Group()
bulletsGroup = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

for i in range(8):
    new_rock()


######################################################################################

while windowRunning:
    # FPS in game
    clock.tick(FPS)
    for event in pygame.event.get():
        # Player hit the close window button
        if event.type == pygame.QUIT:
            windowRunning = False
        # Player hit the keyboard key
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    # check if the rocks and bullets are collide
    hits1 = pygame.sprite.groupcollide(rocksGroup, bulletsGroup, True, True)
    for hit in hits1:
        random.choice(rock_expl_sound).play()
        score += hit.radius
        new_rock()

    # check if the rock hits the player
    hits2 = pygame.sprite.spritecollide(
        player, rocksGroup, True, pygame.sprite.collide_circle)
    for hit in hits2:
        new_rock()
        player.health -= hit.radius
        if player.health <= 0:
            windowRunning = False

    ######################################################################################

    # fill up background with picture at position (0,0)
    window.blit(bg_img, (0, 0))
    # draw out all the objects in the list all_sprites
    all_sprites.draw(window)
    draw_score(window, str(score), 28, Width*0.9, 10)
    draw_health(window, player.health, 10, 12)
    pygame.display.update()
    all_sprites.update()


pygame.quit()
