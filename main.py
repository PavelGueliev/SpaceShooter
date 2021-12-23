import pygame


square_sprites = pygame.sprite.Group()
platform_sprites = pygame.sprite.Group()
size = width, height = 500, 500
v = 50
fps = 60
screen = pygame.display.set_mode(size)


class Bullet(pygame.sprite.Sprite):
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

    def update(self):
        if not pygame.sprite.spritecollideany(self, platform_sprites):
            self.y += v / fps
        self.rect = pygame.Rect(self.x, int(self.y),
                                self.size_square, self.size_square)


class Heroe(pygame.sprite.Sprite):
    size_platform = 50, 10

    def __init__(self, pos):
        super().__init__(platform_sprites)
        self.just_size = self.size_platform
        self.image = pygame.Surface((self.just_size[0], self.just_size[1]),
                                    pygame.SRCALPHA)
        pygame.draw.rect(self.image, pygame.Color("gray"),
                         (0, 0, self.just_size[0], self.just_size[1]))
        self.rect = pygame.Rect(*pos, self.just_size[0], self.just_size[1])


def main():
    clock = pygame.time.Clock()
    running = True
    while running:
        screen.fill(pygame.Color("black"))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    Bullet(event.pos)
                elif event.button == 3:
                    Heroe(event.pos)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    for spr in square_sprites:
                        spr.x -= 10
                elif event.key == pygame.K_RIGHT:
                    for spr in square_sprites:
                        spr.x += 10
            for spr in square_sprites:
                if spr.y > 550:
                    spr.kill()
        square_sprites.draw(screen)
        platform_sprites.draw(screen)
        square_sprites.update()

        clock.tick(fps)
        pygame.display.flip()
        pygame.display.flip()
        clock.tick(fps)


if __name__ == '__main__':
    main()
    pygame.quit()