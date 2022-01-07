import sys
from random import randint

import pygame

Enemy_sprites = pygame.sprite.Group()
hero_sprites = pygame.sprite.Group()
bullets_sprites = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
stars_sprites = pygame.sprite.Group()
menu_sprites = pygame.sprite.Group()
pygame.init()
size = width, height = 500, 700
v = 50
fps = 60
tic = 0
screen = pygame.display.set_mode(size)


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
        self.effect_bullet = 1

    def update(self, fly):
        self.rect = pygame.Rect(self.x, self.y, self.size_square, self.size_square)


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
        self.rect = pygame.Rect(self.x, int(self.y), self.just_size[0], self.just_size[1])
        self.y -= 10


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
        self.x, self.y = pos[0], pos[1] - 100
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
        pygame.draw.rect(self.image, pygame.Color("red"), (0, 0, self.size_of_enemy[0], self.size_of_enemy[1]))
        self.rect = pygame.Rect(*pos, *self.size_of_enemy)
        self.x, self.y = pos

    def update(self):
        self.rect = self.rect.move(self.x, self.y)
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            self.y = -self.y
        if pygame.sprite.spritecollideany(self, vertical_borders):
            self.x = -self.x


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


def terminate():
    pygame.quit()
    sys.exit()


def start_screen(command='continue'):
    global tic
    start_img = pygame.image.load('Game.png').convert_alpha()
    exit_img = pygame.image.load('Exit.png').convert_alpha()
    credit_img = pygame.image.load('Credit.png').convert_alpha()
    us_img = pygame.image.load('Us.png').convert_alpha()
    reit_img = pygame.image.load('Reit.png').convert_alpha()
    # create button instances
    start_button = Button(100, 200, start_img, 0.8)
    exit_button = Button(100, 250, exit_img, 0.8)
    credit_button = Button(100, 300, credit_img, 0.8)
    reit_button = Button(100, 350, reit_img, 0.8)
    us_button = Button(100, 400, us_img, 0.8)

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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and command != 'start':
                    return
        if start_button.draw(screen):
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


def main():
    tic = 0
    start_screen('start')
    clock = pygame.time.Clock()
    running = True
    Hero((250, 600))
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
                    Enemy_type_1((10, 10))
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
                if spr.x < 480:
                    spr.x += 10
        if directions['up']:
            for spr in hero_sprites:
                if spr.y > 10:
                    spr.y -= 10
        if directions['down']:
            for spr in hero_sprites:
                if spr.y < 600:
                    spr.y += 10
        if directions['mouse']:
            if tic % 10 == 0:
                for spr in hero_sprites:
                    if spr.effect_bullet == 1:
                        Bullet((spr.x + 7, spr.y - 20))
                    elif spr.effect_bullet == 2:
                        Bullet((spr.x - 3, spr.y - 20))
                        Bullet((spr.x + 7, spr.y - 25))
                        Bullet((spr.x + 17, spr.y - 21))
        for spr in hero_sprites:
            if spr.y > 800:
                spr.kill()
        for spr in bullets_sprites:
            if spr.y < 0:
                spr.kill()

        if tic % 2 == 0:
            stars_sprites.update()
        if tic % 500 == 0:
            for i in range(50):
                Stars((randint(0, 500), randint(-700, 0)))
            tic = 0
        tic += 1
        stars_sprites.draw(screen)
        hero_sprites.draw(screen)
        Enemy_sprites.draw(screen)
        bullets_sprites.draw(screen)

        bullets_sprites.update()
        hero_sprites.update(directions['down'] or directions['up'])
        if tic % 2 == 0:
            Enemy_sprites.update()
        pygame.display.flip()
        clock.tick(fps)


if __name__ == '__main__':
    main()
    pygame.quit()
