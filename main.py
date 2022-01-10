import os
import sys
from random import randint
from datetime import datetime
import pygame

test_group = pygame.sprite.Group()
Enemy_sprites = pygame.sprite.Group()
Enemy_sprites_2 = pygame.sprite.Group()
enemy_bullet_sprites = pygame.sprite.Group()
shield_sprite = pygame.sprite.Group()
hero_sprites = pygame.sprite.Group()
bullets_sprites = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
stars_sprites = pygame.sprite.Group()
menu_sprites = pygame.sprite.Group()
final_screen_sprites = pygame.sprite.Group()
pygame.init()
size = width, height = 1280, 720
running = True
shield_flag = False
v = 50
fps = 60
tic = 10
score = 0
buf_of_level = []
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Space shooter')
pygame.display.set_icon(pygame.image.load('data/ico.png'))
count = 0


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname).convert()
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


class Hero(pygame.sprite.Sprite):
    size_square = 20

    def __init__(self, pos, sheet=load_image("hero.png", -1), columns=4, rows=4):
        for spr in hero_sprites:
            spr.kill()
        super().__init__(hero_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = pygame.Rect(*pos,
                                self.image.get_width(), self.image.get_height())

        self.image = pygame.Surface((self.rect.width, self.rect.height),
                                    pygame.SRCALPHA)

        self.x, self.y = pos
        self.swim = self.y + 10
        self.flag_swim = 1
        self.effect_bullet = 2
        self.hp = 3

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns, sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(frame_location, self.rect.size)))

    def update(self, fly):
        global shield_flag
        self.rect = pygame.Rect(self.x, self.y, self.rect.width, self.rect.width)
        if tic % 15 == 0:
            if pygame.sprite.spritecollideany(self, Enemy_sprites) and not shield_flag:
                self.hp -= 1
                print('hp', self.hp)
            if pygame.sprite.spritecollideany(self, Enemy_sprites_2):
                self.hp -= 1
                print('hp', self.hp)
        if pygame.sprite.spritecollideany(self, enemy_bullet_sprites):
            self.hp -= 1
            print('hp', self.hp)
        if tic % 3 == 0:
            self.cur_frame = (self.cur_frame + 1) % 3
            self.image = self.frames[self.cur_frame]

    def get_hp(self):
        return self.hp


class Bullet(pygame.sprite.Sprite):
    size_platform = 5, 20

    def __init__(self, pos, bullet='data/bullet1.png'):
        super().__init__(bullets_sprites)
        self.image2 = pygame.image.load(bullet).convert_alpha()
        self.image2 = pygame.transform.scale(self.image2, (20, 40))

        self.rect = pygame.Rect(*pos,
                                self.image2.get_width(), self.image2.get_height())

        self.image = pygame.Surface((self.rect.width, self.rect.height),
                                    pygame.SRCALPHA)
        self.image = self.image2
        self.x, self.y = pos[0], pos[1]

    def update(self):
        if pygame.sprite.spritecollideany(self, Enemy_sprites):
            self.kill()
            return
        elif pygame.sprite.spritecollideany(self, Enemy_sprites_2):
            self.kill()
            return
        self.rect = pygame.Rect(self.x, int(self.y), self.rect.width, self.rect.height)
        self.y -= 10


class Bullet_of_Enemy(pygame.sprite.Sprite):
    size_platform = 5, 20

    def __init__(self, pos, bullet='data/enemybullet.png'):
        super().__init__(enemy_bullet_sprites)
        self.image2 = pygame.image.load(bullet).convert_alpha()
        self.image2 = pygame.transform.scale(self.image2, (10, 30))
        self.rect = pygame.Rect(*pos,
                                self.image2.get_width(), self.image2.get_height())

        self.image = pygame.Surface((self.rect.width, self.rect.height),
                                    pygame.SRCALPHA)
        self.image = self.image2
        self.x, self.y = pos[0], pos[1]

    def update(self):
        if pygame.sprite.spritecollideany(self, hero_sprites):
            self.kill()
            return
        self.rect = pygame.Rect(self.x, int(self.y), self.rect.width, self.rect.height)
        self.y += 10
        if pygame.sprite.spritecollideany(self, shield_sprite):
            self.kill()
            return


class Shield(pygame.sprite.Sprite):
    def __init__(self, pos, shield='data/shield.png'):
        for spr in shield_sprite:
            spr.kill()
        super().__init__(shield_sprite)
        self.image2 = pygame.image.load(shield).convert_alpha()
        self.image2 = pygame.transform.scale(self.image2, (72, 72))

        self.rect = pygame.Rect(*pos,
                                self.image2.get_width(), self.image2.get_height())

        self.image = pygame.Surface((self.rect.width, self.rect.height),
                                    pygame.SRCALPHA)
        self.image = self.image2
        self.x, self.y = pos[0], pos[1]

    def update(self):
        global shield_flag
        if tic % 500 == 0:
            self.kill()
            shield_flag = False
        else:
            for spr in hero_sprites:
                Shield((spr.x - 20, spr.y - 20))
                shield_flag = True
        self.rect = pygame.Rect(self.x, int(self.y), self.rect.width, self.rect.height)


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

    def __init__(self, pos, sheet=load_image("enemytype1pix.png", -1), columns=2, rows=1):
        super().__init__(Enemy_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = pygame.Rect(*pos,
                                self.image.get_width(), self.image.get_height())

        self.image = pygame.Surface((self.rect.width, self.rect.height),
                                    pygame.SRCALPHA)
        self.rect = pygame.Rect(*pos, self.rect.width, self.rect.width)
        self.x, self.y = pos
        self.ux = 15
        self.uy = 15

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns, sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(frame_location, self.rect.size)))

    def update(self):
        global score
        if pygame.sprite.spritecollideany(self, bullets_sprites):
            score += 25
            self.kill()
            return
        if pygame.sprite.spritecollideany(self, shield_sprite):
            score += 25
            self.kill()
            return
        if tic % 2 == 0:
            self.rect = self.rect.move(self.ux * 0.5, self.uy * 0.15)
            if pygame.sprite.spritecollideany(self, horizontal_borders):
                self.uy = -self.uy
            if pygame.sprite.spritecollideany(self, vertical_borders):
                self.ux = -self.ux
        if tic % 20 == 0:
            self.cur_frame = (self.cur_frame + 1) % 2
            self.image = self.frames[self.cur_frame]


class Enemy_type_2(pygame.sprite.Sprite):
    size_platform = 25, 25

    def __init__(self, pos, sheet=load_image("enemytype2pix.png", -1), columns=2, rows=2):
        super().__init__(Enemy_sprites_2)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = pygame.Rect(*pos,
                                self.image.get_width(), self.image.get_height())

        self.image = pygame.Surface((self.rect.width, self.rect.height),
                                    pygame.SRCALPHA)
        self.rect = pygame.Rect(*pos, self.rect.width, self.rect.width)
        self.x, self.y = pos
        self.ux = 15
        self.uy = 1

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns, sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(frame_location, self.rect.size)))

    def update(self):
        global score
        if tic % 15 == 0:
            Bullet_of_Enemy((self.rect.x + 15, self.rect.y + 25))

        if pygame.sprite.spritecollideany(self, bullets_sprites):
            self.kill()
            score += 50
            return
        if pygame.sprite.spritecollideany(self, shield_sprite):
            score += 50
            self.kill()
            return

        self.rect = self.rect.move(self.ux * 0.15, self.uy)
        if pygame.sprite.spritecollideany(self, vertical_borders):
            self.ux = -self.ux
        if tic % 5 == 0:
            self.cur_frame = (self.cur_frame + 1) % 3
            self.image = self.frames[self.cur_frame]


class Enemy_type_3(pygame.sprite.Sprite):
    size_platform = 150, 150

    def __init__(self, pos):
        self.count = count
        super().__init__(Enemy_sprites)
        scale = 0.3

        self.image = pygame.transform.scale(load_image('enemytype3.png', -1), (int(width * scale), int(height * scale)))
        self.rect = pygame.Rect(*pos, self.image.get_width(), self.image.get_height())
        self.image = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        self.image = pygame.transform.scale(load_image('enemytype3.png', -1), (int(width * scale), int(height * scale)))

        self.x, self.y = pos
        self.flag_swim = 1
        self.swim = self.y + 25

    def update(self):
        global score
        global shield_flag
        if tic % 4 == 0:
            self.levitation()
        if pygame.sprite.spritecollideany(self, bullets_sprites):
            self.count += 1
            if self.count == 150:
                score += 500
                self.kill()
                return
        if pygame.sprite.spritecollideany(self, shield_sprite):
            shield_flag = True
        self.rect = pygame.Rect(self.x, self.y, self.rect.width, self.rect.height)

    def levitation(self):
        if self.flag_swim:
            self.y += 1
        else:
            self.y -= 1
        if self.swim == self.y:
            self.flag_swim += 1
            self.flag_swim %= 2
            if self.flag_swim:
                self.swim = self.y + 50
            else:
                self.swim = self.y - 50


class Button(pygame.sprite.DirtySprite):
    def __init__(self, x, y, image, scale, sprites):
        super().__init__(sprites)
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
    start_img = pygame.image.load('data/Game.png').convert_alpha()
    exit_img = pygame.image.load('data/Exit.png').convert_alpha()
    credit_img = pygame.image.load('data/Credit.png').convert_alpha()
    reit_img = pygame.image.load('data/Reit.png').convert_alpha()
    splashscreen_img = pygame.image.load('data/SplashScreen.png').convert_alpha()
    # create button instances
    start_button = Button(width * 0.4, height * 0.4, start_img, 1.5, menu_sprites)
    reit_button = Button(width * 0.4, height * 0.5, reit_img, 1.5, menu_sprites)
    credit_button = Button(width * 0.4, height * 0.6, credit_img, 1.5, menu_sprites)
    exit_button = Button(width * 0.4, height * 0.7, exit_img, 1.5, menu_sprites)
    Button(width * 0.26, height * 0.13, splashscreen_img, 2, menu_sprites)

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
            for i in menu_sprites:
                i.kill()
            start_time = datetime.now()
            return
        if reit_button.draw(screen):
            start_time = datetime.now()
            return
        if credit_button.draw(screen):
            for i in menu_sprites:
                i.kill()
            run = False
            credit_screen()
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


def credit_screen():
    global tic, start_time, buf_of_level

    exit_img = pygame.image.load('data/Exit.png').convert_alpha()

    intro_text = '''Название проекта - Space Shooter
Идея создания проекта:
Мы решили испытать свои умения и создать игру - обычный Space Shooter,
которых очень много на просторах интернета.
Описание проекта:
В нашей игре должен быть главный герой которым можно было бы управлять, в нашем случае это - Звёздный корабль.
Как мы знаем в космосе много разных опасностей, и дабы добавить в наш игровой космос одну из опасностей,
с которой мы сможем бороться, мы решили добавить врагов-иннопланетян, которые будут не одного типа,
у кого-то есть способность стрелять, у кого-то способность совершать манёвры,
а кто-то просто как пешка (бесполезные когда одни, но представляют опасность когда их много),
чтобы вам было легче пройти игру Звёздный корабль мы оснастили оружием, которое можно улучшать за убийство врагов,
помимо врагов мы решили добавить конечного босса, одолев которого вы пройдёте игру, однако не всё так легко,
на пути к боссу вы сможете встретится с ещё одной проблемой, такой как пояс астероидов,
где вам придется совершать манёвры чтобы выжить.'''.split('\n')

    # create button instances
    exit_button = Button(width * 0.8, height * 0.8, exit_img, 1.5, menu_sprites)

    # game loop
    run = True
    clock = pygame.time.Clock()
    while run:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
        if exit_button.draw(screen):
            run = False
            for i in menu_sprites:
                i.kill()
            start_screen()
            return

        if tic % 500 == 0:
            for i in range(50):
                Stars((randint(0, width), randint(-height, 0)))
            tic = 0

        font = pygame.font.Font(None, 30)
        text_coord = 50

        tic += 1
        stars_sprites.draw(screen)
        menu_sprites.draw(screen)
        menu_sprites.update()
        for line in intro_text:
            string_rendered = font.render(line, 1, pygame.Color('green'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)

        stars_sprites.update()

        pygame.display.flip()
        clock.tick(60)
    pygame.quit()


def final_screen(status='win', score=0):
    global tic, start_time, buf_of_level

    exit_img = pygame.image.load('data/gameoverscreen.png').convert_alpha()

    intro_text = [f'Ваш счет: {str(score)}']

    splashscreen_img = pygame.image.load('data/SplashScreen.png').convert_alpha()
    # create button instances
    exit_button = Button(width * 0.1, height * 0.1, exit_img, 1.5, final_screen_sprites)

    # game loop
    run = True
    clock = pygame.time.Clock()
    while run:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
        if exit_button.draw(screen):
            run = False
            start_screen()
            return

        if tic % 500 == 0:
            for i in range(50):
                Stars((randint(0, width), randint(-height, 0)))
            tic = 0

        font = pygame.font.Font(None, 30)
        text_coord = 50

        tic += 1
        final_screen_sprites.draw(screen)
        stars_sprites.draw(screen)

        final_screen_sprites.update()
        for line in intro_text:
            string_rendered = font.render(line, 10, pygame.Color('white'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.x = width // 2
            intro_rect.y = height * 0.7
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)

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
    buf_of_level = []  # load_level('1.txt')
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
                if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                    for spr in hero_sprites:
                        Shield((spr.x - 20, spr.y - 20))
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
                        Bullet((spr.x - 10, spr.y - 25))
                        Bullet((spr.x + 5, spr.y - 45))
                        Bullet((spr.x + 20, spr.y - 25))
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
            if int((datetime.now() - start_time).total_seconds()) >= buf_of_level[0][0] and \
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
            img2 = font.render(f'{i.get_hp()}/100 HP:' + ''.join(['|' for i in range(i.get_hp())]), True, 'green')
        for i in hero_sprites:
            if i.get_hp() < 1:
                final_screen()
                i.hp = 3
        stars_sprites.draw(screen)
        hero_sprites.draw(screen)
        Enemy_sprites.draw(screen)
        Enemy_sprites_2.draw(screen)
        bullets_sprites.draw(screen)
        enemy_bullet_sprites.draw(screen)
        shield_sprite.draw(screen)

        bullets_sprites.update()
        if tic % 2 == 0:
            stars_sprites.update()
        Enemy_sprites_2.update()
        enemy_bullet_sprites.update()
        hero_sprites.update(directions['down'] or directions['up'])
        Enemy_sprites.update()
        shield_sprite.update()

        test_group.draw(screen)
        test_group.update()

        screen.blit(img, (width * 0.9, height * 0.1))
        screen.blit(img2, (width * 0.05, height * 0.1))
        pygame.display.flip()
        clock.tick(fps)
    pygame.quit()


if __name__ == '__main__':
    main()
    pygame.quit()
