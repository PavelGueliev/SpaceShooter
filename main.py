import sys
from random import randint
from datetime import datetime
import pygame

Enemy_sprites = pygame.sprite.Group()
Enemy_sprites_2 = pygame.sprite.Group()
enemy_bullet_sprites = pygame.sprite.Group()
hero_sprites = pygame.sprite.Group()
bullets_sprites = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
stars_sprites = pygame.sprite.Group()
menu_sprites = pygame.sprite.Group()
pygame.init()
size = width, height = 1280, 720
running = True
v = 50
fps = 60
tic = 10
score = 0
buf_of_level = []
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Space shooter')
count = 0


class Hero(pygame.sprite.Sprite):
    size_square = 20

    def __init__(self, pos):
        for spr in hero_sprites:
            spr.kill()
        super().__init__(hero_sprites)
        self.image = pygame.Surface((self.size_square, self.size_square),
                                    pygame.SRCALPHA)
        pygame.draw.rect(self.image, pygame.Color("blue"),
                         (0, 0, self.size_square, self.size_square))
        self.rect = pygame.Rect(*pos,
                                self.size_square, self.size_square)
        self.x, self.y = pos
        self.swim = self.y + 10
        self.flag_swim = 1
        self.effect_bullet = 2
        self.hp = 30

    def update(self, fly):
        self.rect = pygame.Rect(self.x, self.y, self.size_square, self.size_square)
        if tic % 15 == 0:
            if pygame.sprite.spritecollideany(self, Enemy_sprites):
                self.hp -= 1
                print('hp', self.hp)
            if pygame.sprite.spritecollideany(self, Enemy_sprites_2):
                self.hp -= 1
                print('hp', self.hp)
        if pygame.sprite.spritecollideany(self, enemy_bullet_sprites):
            self.hp -= 1
            print('hp', self.hp)

    def get_hp(self):
        return self.hp


class Bullet(pygame.sprite.Sprite):
    size_platform = 5, 20

    def __init__(self, pos):
        super().__init__(bullets_sprites)
        self.just_size = self.size_platform
        self.image = pygame.Surface((self.just_size[0], self.just_size[1]),
                                    pygame.SRCALPHA)
        pygame.draw.rect(self.image, pygame.Color("yellow"),
                         (0, 0, self.just_size[0], self.just_size[1]))
        self.rect = pygame.Rect(*pos, self.just_size[0], self.just_size[1])
        self.x, self.y = pos[0], pos[1]

    def update(self):
        if pygame.sprite.spritecollideany(self, Enemy_sprites):
            self.kill()
            return
        elif pygame.sprite.spritecollideany(self, Enemy_sprites_2):
            self.kill()
            return

        self.rect = pygame.Rect(self.x, int(self.y), self.just_size[0], self.just_size[1])
        self.y -= 10


class Bullet_2(pygame.sprite.Sprite):
    size_platform = 5, 20

    def __init__(self, pos):
        super().__init__(bullets_sprites)
        self.just_size = self.size_platform
        self.image = pygame.Surface((self.just_size[0], self.just_size[1]),
                                    pygame.SRCALPHA)
        pygame.draw.rect(self.image, pygame.Color("yellow"),
                         (0, 0, self.just_size[0], self.just_size[1]))
        self.rect = pygame.Rect(*pos, self.just_size[0], self.just_size[1])
        self.x, self.y = pos[0], pos[1]

    def update(self):
        if pygame.sprite.spritecollideany(self, Enemy_sprites):
            self.kill()
            return
        elif pygame.sprite.spritecollideany(self, Enemy_sprites_2):
            self.kill()
            return

        self.rect = pygame.Rect(self.x, int(self.y), self.just_size[0], self.just_size[1])
        self.y -= 10


class Bullet_of_Enemy(pygame.sprite.Sprite):
    size_platform = 5, 20

    def __init__(self, pos):
        super().__init__(enemy_bullet_sprites)
        self.just_size = self.size_platform
        self.image = pygame.Surface((self.just_size[0], self.just_size[1]),
                                    pygame.SRCALPHA)
        pygame.draw.rect(self.image, pygame.Color("red"),
                         (0, 0, self.just_size[0], self.just_size[1]))
        self.rect = pygame.Rect(*pos, self.just_size[0], self.just_size[1])
        self.x, self.y = pos[0], pos[1]

    def update(self):
        if pygame.sprite.spritecollideany(self, hero_sprites):
            self.kill()
            return
        self.rect = pygame.Rect(self.x, int(self.y), self.just_size[0], self.just_size[1])
        self.y += 10


class Stars(pygame.sprite.DirtySprite):
    size_platform = 5, 5

    def __init__(self, pos):
        super().__init__(stars_sprites)
        self.just_size = self.size_platform
        self.image = pygame.Surface((self.just_size[0], self.just_size[1]),
                                    pygame.SRCALPHA)
        pygame.draw.rect(self.image, pygame.Color("white"),
                         (0, 0, self.just_size[0], self.just_size[1]))
        self.rect = pygame.Rect(*pos, self.just_size[0], self.just_size[1])
        self.x, self.y = pos[0], pos[1]
        self.u = randint(1, 8)

    def update(self):
        self.rect = pygame.Rect(self.x, int(self.y), self.just_size[0], self.just_size[1])
        self.y += self.u
        if self.rect.y > height:
            self.kill()


class Border(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2:
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


class Enemy_type_1(pygame.sprite.Sprite):
    size_platform = 25, 25

    def __init__(self, pos):
        super().__init__(Enemy_sprites)
        self.size_of_enemy = self.size_platform
        self.image = pygame.Surface((self.size_of_enemy[0], self.size_of_enemy[1]),
                                    pygame.SRCALPHA)
        pygame.draw.rect(self.image, pygame.Color("pink"), (0, 0, self.size_of_enemy[0], self.size_of_enemy[1]))
        self.rect = pygame.Rect(*pos, *self.size_of_enemy)
        self.x, self.y = pos
        self.ux = 30
        self.uy = 30

    def update(self):
        global score
        if pygame.sprite.spritecollideany(self, bullets_sprites):
            score += 25
            self.kill()
            return
        if tic % 2 == 0:
            self.rect = self.rect.move(self.ux * 0.5, self.uy * 0.15)
            if pygame.sprite.spritecollideany(self, horizontal_borders):
                self.uy = -self.uy
            if pygame.sprite.spritecollideany(self, vertical_borders):
                self.ux = -self.ux


class Enemy_type_2(pygame.sprite.Sprite):
    size_platform = 25, 25

    def __init__(self, pos):
        super().__init__(Enemy_sprites_2)
        self.size_of_enemy = self.size_platform
        self.image = pygame.Surface((self.size_of_enemy[0], self.size_of_enemy[1]),
                                    pygame.SRCALPHA)
        pygame.draw.rect(self.image, pygame.Color("#DC143C"), (0, 0, self.size_of_enemy[0], self.size_of_enemy[1]))
        self.rect = pygame.Rect(*pos, self.size_of_enemy[0], self.size_of_enemy[1])
        self.x, self.y = pos
        self.ux = 15
        self.uy = 1

    def update(self):
        global score
        if tic % 15 == 0:
            Bullet_of_Enemy((self.rect.x, self.rect.y + 10))

        if pygame.sprite.spritecollideany(self, bullets_sprites):
            self.kill()
            score += 50
            return

        self.rect = self.rect.move(self.ux * 0.15, self.uy)
        if pygame.sprite.spritecollideany(self, vertical_borders):
            self.ux = -self.ux


class Enemy_type_3(pygame.sprite.Sprite):
    size_platform = 150, 150

    def __init__(self, pos):
        self.count = count
        super().__init__(Enemy_sprites)
        self.size_of_enemy = self.size_platform
        self.image = pygame.Surface((self.size_of_enemy[0], self.size_of_enemy[1]),
                                    pygame.SRCALPHA)
        pygame.draw.rect(self.image, pygame.Color("DarkMagenta"), (0, 0, self.size_of_enemy[0], self.size_of_enemy[1]))
        self.rect = pygame.Rect(*pos, self.size_of_enemy[0], self.size_of_enemy[1])
        self.x, self.y = pos

    def update(self):
        global score
        if pygame.sprite.spritecollideany(self, bullets_sprites):
            self.count += 1
            if self.count == 150:
                score += 500
                self.kill()
                return


class Button(pygame.sprite.DirtySprite):
    def __init__(self, x, y, image, scale):
        super().__init__(menu_sprites)
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self, surface):
        action = False
        # get mouse position
        pos = pygame.mouse.get_pos()

        # check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked is False:
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # draw button on screen
        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action


def start_screen(command='continue'):
    global tic, start_time, buf_of_level
    start_img = pygame.image.load('Game.png').convert_alpha()
    exit_img = pygame.image.load('Exit.png').convert_alpha()
    credit_img = pygame.image.load('Credit.png').convert_alpha()
    reit_img = pygame.image.load('Reit.png').convert_alpha()
    splashscreen_img = pygame.image.load('SplashScreen.png').convert_alpha()
    # create button instances
    start_button = Button(width * 0.4, height * 0.4, start_img, 1.5)
    reit_button = Button(width * 0.4, height * 0.5, reit_img, 1.5)
    credit_button = Button(width * 0.4, height * 0.6, credit_img, 1.5)
    exit_button = Button(width * 0.4, height * 0.7, exit_img, 1.5)
    Button(width * 0.26, height * 0.13, splashscreen_img, 2)

    # game loop
    if command == 'start':
        for i in range(50):
            Stars((randint(0, width), randint(-height, height)))
    run = True
    clock = pygame.time.Clock()
    while run:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and command != 'start':
                    return
        if start_button.draw(screen):
            start_time = datetime.now()
            return
        if reit_button.draw(screen):
            start_time = datetime.now()
            return
        if credit_button.draw(screen):
            start_time = datetime.now()
            return
        if exit_button.draw(screen):
            terminate()
            break
        if tic % 500 == 0:
            for i in range(50):
                Stars((randint(0, width), randint(-height, 0)))
            tic = 0
        tic += 1
        stars_sprites.draw(screen)
        menu_sprites.draw(screen)
        menu_sprites.update()

        stars_sprites.update()

        pygame.display.flip()
        clock.tick(60)
    pygame.quit()


def terminate():
    pygame.quit()
    sys.exit()


def load_level(txt_file):
    lst = []
    with open(f'levels/{txt_file}', 'r', encoding='UTF-8') as f:
        for line in f.readlines():
            if line[0].isdigit():
                line = line.split(';')
                for x in range(3):
                    line[x] = int(line[x])
                line[3] = line[3].strip()
                k = []
                for coord in line[3].split(','):
                    k.append([int(x) for x in coord.split()])
                line[3] = k
                lst.append(line)
    return lst


def main():
    global tic, start_time
    buf_of_level = load_level('1.txt')
    start_screen('start')
    clock = pygame.time.Clock()
    running = True
    Hero((int(width * 0.5), int(height * 0.75)))

    directions = {"right": False, "left": False, 'mouse': False, 'down': False, 'up': False}
    Border(5, 5, width - 5, 5)
    Border(5, height - 5, width - 5, height - 5)
    Border(5, 5, 5, height - 5)
    Border(width - 5, 5, width - 5, height - 5)
    while running:
        screen.fill(pygame.Color("black"))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    directions['mouse'] = True
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    directions['mouse'] = False
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 3:
                    Enemy_type_1((20, 20))
                    Enemy_type_2((30, 30))
                    Enemy_type_3((180, 150))
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    directions['right'] = True
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    directions['left'] = True
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    directions['up'] = True
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    directions['down'] = True
                if event.key == pygame.K_SPACE:
                    directions['mouse'] = True
                if event.key == pygame.K_ESCAPE:
                    start_screen()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    directions['right'] = False
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    directions['left'] = False
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    directions['up'] = False
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    directions['down'] = False
                if event.key == pygame.K_SPACE:
                    directions['mouse'] = False
        if directions['left']:
            for spr in hero_sprites:
                if spr.x > 0:
                    spr.x -= 10
        if directions['right']:
            for spr in hero_sprites:
                if spr.x < width - 20:
                    spr.x += 10
        if directions['up']:
            for spr in hero_sprites:
                if spr.y > 10:
                    spr.y -= 10
        if directions['down']:
            for spr in hero_sprites:
                if spr.y < height - 25:
                    spr.y += 10
        if directions['mouse']:
            if tic % 15 == 0:
                for spr in hero_sprites:
                    if spr.effect_bullet == 1:
                        Bullet((spr.x + 7, spr.y - 20))
                    elif spr.effect_bullet == 2:
                        Bullet((spr.x - 3, spr.y - 17))
                        Bullet((spr.x + 7, spr.y - 28))
                        Bullet((spr.x + 17, spr.y - 23))
        for spr in bullets_sprites:
            if spr.y < 0:
                spr.kill()
        for bul in enemy_bullet_sprites:
            if bul.y > height:
                bul.kill()
        if tic % 2 == 0:
            stars_sprites.update()
        if tic % 500 == 0:
            for i in range(50):
                Stars((randint(0, width), randint(-height, 0)))
            tic = 0
        tic += 1
        try:
            if int((datetime.now() - start_time).total_seconds()) >= buf_of_level[0][0] and\
                    0 <= int((datetime.now() - start_time).total_seconds() * 100) % 100 < 2:
                for i in range(buf_of_level[0][2]):
                    if buf_of_level[0][1] == 1:
                        Enemy_type_1(buf_of_level[0][3][i])
                    elif buf_of_level[0][1] == 2:
                        Enemy_type_2(buf_of_level[0][3][i])
                    elif buf_of_level[0][1] == 3:
                        Enemy_type_3(buf_of_level[0][3][i])
                start_time = datetime.now()
                del buf_of_level[0]
        except:
            pass

        font = pygame.font.SysFont('serif', 24)
        img = font.render(f'Score: {score}', True, 'green')
        for i in hero_sprites:
            img2 = font.render('HP:' + ''.join(['|' for i in range(i.get_hp())]), True, 'green')


        stars_sprites.draw(screen)
        hero_sprites.draw(screen)
        Enemy_sprites.draw(screen)
        Enemy_sprites_2.draw(screen)
        bullets_sprites.draw(screen)
        enemy_bullet_sprites.draw(screen)

        bullets_sprites.update()
        if tic % 2 == 0:
            stars_sprites.update()
        Enemy_sprites_2.update()
        enemy_bullet_sprites.update()
        hero_sprites.update(directions['down'] or directions['up'])
        Enemy_sprites.update()

        screen.blit(img, (width * 0.9, height * 0.1))
        screen.blit(img2, (width * 0.1, height * 0.1))
        pygame.display.flip()
        clock.tick(fps)


if __name__ == '__main__':
    main()
    pygame.quit()
