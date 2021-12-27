from random import randint

import pygame

Enemy_sprites = pygame.sprite.Group()
square_sprites = pygame.sprite.Group()
platform_sprites = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
stars_sprites = pygame.sprite.Group()
size = width, height = 500, 700
v = 50
fps = 60
screen = pygame.display.set_mode(size)


class Heroe(pygame.sprite.Sprite):
    size_square = 20

    def __init__(self, pos):
        for spr in square_sprites:
            spr.kill()
        super().__init__(square_sprites)
        self.image = pygame.Surface((self.size_square, self.size_square),
                                    pygame.SRCALPHA)
        pygame.draw.rect(self.image, pygame.Color("blue"),
                         (0, 0, self.size_square, self.size_square))
        self.rect = pygame.Rect(*pos,
                                self.size_square, self.size_square)
        self.x, self.y = pos
        self.swim = self.y + 10
        self.flag_swim = 1

    def update(self, fly):
        if not fly:
            if self.flag_swim:
                self.y += 1
            else:
                self.y -= 1
            if self.swim == self.y:
                self.flag_swim += 1
                self.flag_swim %= 2
                if self.flag_swim:
                    self.swim = self.y + 10
                else:
                    self.swim = self.y - 10
        else:
            if self.flag_swim:
                self.swim = self.y + 10
            else:
                self.swim = self.y - 10
        self.rect = pygame.Rect(self.x, self.y, self.size_square, self.size_square)


class Bullet(pygame.sprite.Sprite):
    size_platform = 5, 20

    def __init__(self, pos):
        super().__init__(platform_sprites)
        self.just_size = self.size_platform
        self.image = pygame.Surface((self.just_size[0], self.just_size[1]),
                                    pygame.SRCALPHA)
        pygame.draw.rect(self.image, pygame.Color("yellow"),
                         (0, 0, self.just_size[0], self.just_size[1]))
        self.rect = pygame.Rect(*pos, self.just_size[0], self.just_size[1])
        self.x, self.y = pos[0], pos[1] - 100

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

    def update(self):
        self.rect = pygame.Rect(self.x, int(self.y), self.just_size[0], self.just_size[1])
        self.y += 1
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
        self.rect = pygame.Rect(*pos, self.size_of_enemy[0], self.size_of_enemy[1])
        self.x, self.y = pos

    def update(self):
        self.rect = self.rect.move(self.x, self.y)
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            self.y = -self.y
        if pygame.sprite.spritecollideany(self, vertical_borders):
            self.x = -self.x


def main():
    clock = pygame.time.Clock()
    for i in range(100):
        Stars((randint(0, 500), randint(-700, 700)))
    running = True
    Heroe((250, 600))
    directions = {"right": False, "left": False, 'mouse': False, 'down': False, 'up': False}
    tic = 10
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
            for spr in square_sprites:
                if spr.x > 0:
                    spr.x -= 10
        if directions['right']:
            for spr in square_sprites:
                if spr.x < 480:
                    spr.x += 10
        if directions['up']:
            for spr in square_sprites:
                if spr.y > 10:
                    spr.y -= 10
        if directions['down']:
            for spr in square_sprites:
                if spr.y < 600:
                    spr.y += 10
        if tic % 6 == 0:
            if directions['mouse']:
                for spr in square_sprites:
                    Bullet((spr.x + 7, spr.y - 20))
        for spr in square_sprites:
            if spr.y > 800:
                spr.kill()
        for spr in platform_sprites:
            if spr.y < 0:
                spr.kill()
        tic += 1
        if tic % 2 == 0:
            stars_sprites.update()
        if tic % 500 == 0:
            for i in range(50):
                Stars((randint(0, 500), randint(-700, 0)))
            tic = 0
        stars_sprites.draw(screen)
        square_sprites.draw(screen)
        Enemy_sprites.draw(screen)
        platform_sprites.draw(screen)

        platform_sprites.update()
        square_sprites.update(directions['down'] or directions['up'])

        Enemy_sprites.update()
        clock.tick(fps)
        pygame.display.flip()
        clock.tick(fps)


if __name__ == '__main__':
    main()
    pygame.quit()