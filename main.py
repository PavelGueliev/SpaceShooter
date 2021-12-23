import pygame


square_sprites = pygame.sprite.Group()
platform_sprites = pygame.sprite.Group()
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

    def update(self):
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

        self.rect = pygame.Rect(self.x, int(self.y),
                                self.size_square, self.size_square)


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


def main():
    clock = pygame.time.Clock()
    running = True
    Heroe((250, 600))
    directions = {"right": False, "left": False, 'mouse': False, 'down': False, 'up': False}
    tic = 10
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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_d:
                    directions['right'] = True
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_a:
                    directions['left'] = True
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    directions['up'] = True
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    directions['down'] = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    directions['right'] = False
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    directions['left'] = False
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    directions['up'] = False
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    directions['down'] = False
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
                if spr.y > 0:
                    spr.y -= 10
        if directions['down']:
            for spr in square_sprites:
                if spr.y < 600:
                    spr.y += 10
        if tic == 0:
            if directions['mouse']:
                for spr in square_sprites:
                    Bullet((spr.x, spr.y))
        for spr in square_sprites:
            if spr.y > 800:
                spr.kill()
        for spr in platform_sprites:
            if spr.y < 0:
                spr.kill()
        tic += 1
        tic %= 8
        square_sprites.draw(screen)
        platform_sprites.draw(screen)
        platform_sprites.update()
        square_sprites.update()
        clock.tick(fps)
        pygame.display.flip()
        clock.tick(fps)


if __name__ == '__main__':
    main()
    pygame.quit()