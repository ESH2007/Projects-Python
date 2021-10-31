import sys
import pygame as pg
import random

WIDTH = 800
HEIGHT = 600
BLACK = (0, 0, 0)
WHITE = ( 255, 255, 255)
GREEN = (0, 255, 0)

pg.init()
pg.mixer.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Wabe_Same")
clock = pg.time.Clock()

def draw_text(surface, text, size, x, y):
    font = pg.font.SysFont("serif", size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)

def draw_shield_bar(surface, x, y, percentage):
    BAR_LENGHT = 100
    BAR_HEIGHT = 10
    fill = (percentage / 100) * BAR_LENGHT
    border = pg.Rect(x, y, BAR_LENGHT, BAR_HEIGHT)
    fill = pg.Rect(x, y, fill, BAR_HEIGHT)
    pg.draw.rect(surface, GREEN, fill)
    pg.draw.rect(surface, WHITE, border, 2)

class Player(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.image.load("assets/simbolo_paz.png").convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10
        self.speed_x = 0
        self.shield = 100

    def update(self):
        self.speed_x = 0
        keystate = pg.key.get_pressed()
        if keystate[pg.K_a]:
            self.speed_x = -5
        if keystate[pg.K_d]:
            self.speed_x = 5
        self.rect.x += self.speed_x
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
        laser_sound.play()

class Meteor(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = random.choice(meteor_images)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-140, -100)
        self.speedy = random.randrange(1, 10)
        self.speedx = random.randrange(-5, 5)

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT + 10 or self.rect.left < -40 or self.rect.right > WIDTH + 40:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-140, - 100)
            self.speedy = random.randrange(1, 10)

class Bullet(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pg.image.load("assets/planta.png")
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

class Explosion(pg.sprite.Sprite):
    def __init__(self, center):
        super().__init__()
        self.image = explosion_anim[0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pg.time.get_ticks()
        self.frame_rate = 50 # VELOCIDAD DE LA EXPLOSION

    def update(self):
        now = pg.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

def show_go_screen():
    screen.blit(background, [0,0])
    draw_text(screen, "Wabe Same", 65, WIDTH // 2, HEIGHT // 4)
    draw_text(screen, "Press Space to win the war!!", 27, WIDTH // 2, HEIGHT // 2)
    draw_text(screen, "Press the W.A.S.D Keys to move the character", 20, WIDTH // 2, HEIGHT * 3/4)
    pg.display.flip()
    waiting = True
    while waiting:
        clock.tick(60)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            if event.type == pg.KEYUP:
                waiting = False


meteor_images = []
meteor_list = ["assets/pistola.png", "assets/arma_2.png", "assets/arma1.png", "assets/bala.png"]
for img in meteor_list:
    meteor_images.append(pg.image.load(img).convert())


####----------------EXPLOSTION IMAGENES --------------
explosion_anim = []
for i in range(9):
    file = "assets/regularExplosion0{}.png".format(i)
    img = pg.image.load(file).convert()
    img.set_colorkey(BLACK)
    img_scale = pg.transform.scale(img, (70,70))
    explosion_anim.append(img_scale)

# Cargar imagen de fondo
background = pg.image.load("assets/flex_3.png").convert()

# Cargar sonidos
laser_sound = pg.mixer.Sound("assets/laser5.ogg")
explosion_sound = pg.mixer.Sound("assets/explosion.wav")
pg.mixer.music.load("assets/music.ogg")
pg.mixer.music.set_volume(0.2)


pg.mixer.music.play(loops=-1)

#### ----------GAME OVER
game_over = True
running = True
while running:
    if game_over:

        show_go_screen()

        game_over = False
        all_sprites = pg.sprite.Group()
        meteor_list = pg.sprite.Group()
        bullets = pg.sprite.Group()

        player = Player()
        all_sprites.add(player)
        for i in range(8):
            meteor = Meteor()
            all_sprites.add(meteor)
            meteor_list.add(meteor)

        score = 0


    clock.tick(60)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                player.shoot()


    all_sprites.update()

    #colisiones - meteoro - laser
    hits = pg.sprite.groupcollide(meteor_list, bullets, True, True)
    for hit in hits:
        score += 10
        explosion_sound.play()
        explosion = Explosion(hit.rect.center)
        all_sprites.add(explosion)
        meteor = Meteor()
        all_sprites.add(meteor)
        meteor_list.add(meteor)

    # Checar colisiones - jugador - meteoro
    hits = pg.sprite.spritecollide(player, meteor_list, True)
    for hit in hits:
        player.shield -= 25
        meteor = Meteor()
        all_sprites.add(meteor)
        meteor_list.add(meteor)
        if player.shield <= 0:
            game_over = True

    screen.blit(background, [0, 0])

    all_sprites.draw(screen)

    #Marcador
    draw_text(screen, str(score), 25, WIDTH // 2, 10)

    # Escudo.
    draw_shield_bar(screen, 5, 5, player.shield)

    pg.display.flip()
pg.quit()

if __name__=='__main__':
    pg.quit()
    sys.exit()