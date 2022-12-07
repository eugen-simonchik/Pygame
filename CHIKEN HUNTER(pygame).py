import pygame
import random
import sys

WIDTH = 1300
HEIGHT = 800
FPS = 60

BLUE = (0, 0, 255)
bird_img = pygame.image.load('chiken.png')
bird_img = pygame.transform.scale(bird_img, (70, 70))

bg = pygame.image.load('nature.png')
bg = pygame.transform.scale(bg, (1300, 800))
bg_rect = bg.get_rect()

stroka = pygame.image.load('pngwing.com.png')
stroka = pygame.transform.scale(stroka, (1300, 100))
stroka_rect = stroka.get_rect()
stroka_rect.x = 0
stroka_rect.y = 0

counter_score = 0
counter_patroni = 5

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("CHIKEN TIME")
pygame.display.set_icon(pygame.image.load('sniper.png'))
clock = pygame.time.Clock()

key = pygame.key.get_pressed()

if pygame.mouse.get_focused():
    pos = pygame.mouse.get_pos()
    pricel_x = pos[0]
    pricel_y = pos[1]


class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('pricel.png')
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = pricel_x
        self.rect.y = pricel_y

    def update(self):
        key = pygame.key.get_pressed()
        if pygame.mouse.get_focused():
            pos = pygame.mouse.get_pos()
            self.rect.x = pos[0]
            self.rect.y = pos[1]


class Bird(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = bird_img
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = random.randrange(100, 700)
        self.speedx = random.randrange(2, 10)
        self.speedy = random.randrange(-4, 8)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy  # движение по оси Y
        if self.rect.left > WIDTH or self.rect.top > HEIGHT + 10:
            self.rect.right = 0
            self.rect.x = 0
            self.rect.y = random.randrange(100, 700)
            self.speedx = random.randrange(4, 10)


all_sprites = pygame.sprite.Group()

birds = pygame.sprite.Group()
bullets = Bullet()
all_sprites.add(bullets)

for i in range(5):
    m = Bird()
    all_sprites.add(m)
    birds.add(m)

fly = True
pygame.mouse.set_visible(False)

while fly:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:
                counter_patroni = 5
            if event.button == 1 and counter_patroni > 0:
                counter_patroni -= 1
                hits = pygame.sprite.spritecollide(bullets, birds, True)
                if hits:
                    for hit in hits:
                        counter_score += 100
                        m = Bird()
                        all_sprites.add(m)
                        birds.add(m)

    t1 = pygame.font.Font(None, 45)
    score = t1.render(f'SCORE:{counter_score}', True, (255, 255, 53))
    t2 = pygame.font.Font(None, 45)
    patroni = t2.render(f'SHOT:{counter_patroni}', True, (255, 255, 53))
    all_sprites.update()

    screen.fill(BLUE)
    screen.blit(bg, (0, 0))
    all_sprites.draw(screen)
    screen.blit(stroka, stroka_rect)
    screen.blit(patroni, (50, 50))
    screen.blit(score, (1100, 50))

    pygame.display.flip()

pygame.quit()
