import pygame
import os
import random
import sys
import time

FPS = 50
WIDTH, HEIGHT = 550, 550
count = 0
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
portal = []
ghost = []
all_sprites = pygame.sprite.Group()
portal_group = pygame.sprite.Group()
wall_group = pygame.sprite.Group()
flor_group = pygame.sprite.Group()
door_group = pygame.sprite.Group()
ghost_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
gan_group = pygame.sprite.Group()
box_group = pygame.sprite.Group()
key_group = pygame.sprite.Group()
vis_group = pygame.sprite.Group()
particle_group = pygame.sprite.Group()
golden_door_group = pygame.sprite.Group()
have_gan = False
is_gan = False
global_pos = [2, 2]
player_pos = [5, 5]
portal_pos = [random.randint(0, 4), random.randint(0, 4)]
tile_width = tile_height = 50
pos_level = {
    "00": "00.txt",
    "01": "стена1.txt",
    "02": "стена1.txt",
    "03": "стена1.txt",
    "04": "011.txt",
    "10": "стена2.txt",
    "11": "середина.txt",
    "12": "середина.txt",
    "13": "середина.txt",
    "14": "стена4.txt",
    "20": "стена2.txt",
    "21": "середина.txt",
    "22": "середина.txt",
    "23": "середина.txt",
    "24": "стена4.txt",
    "30": "стена2.txt",
    "31": "середина.txt",
    "32": "середина.txt",
    "33": "середина.txt",
    "34": "стена4.txt",
    "40": "110.txt",
    "41": "стена3.txt",
    "42": "стена3.txt",
    "43": "стена3.txt",
    "44": "1111.txt",
}
pygame.mouse.set_visible(0)
posible_global_pos_golden_door = [
    [0, 0],
    [0, 1],
    [0, 2],
    [0, 3],
    [0, 4],
    [0, 4],
    [1, 4],
    [2, 4],
    [3, 4],
    [4, 4],
    [4, 4],
    [4, 3],
    [4, 2],
    [4, 1],
    [4, 0],
    [4, 0],
    [3, 0],
    [2, 0],
    [1, 0],
    [0, 0],
]
posible_local_pos_golden_door = (
    [[0, 5]] * 5 + [[5, 10]] * 5 + [[10, 5]] * 5 + [[5, 0]] * 5
)
pos_golden_door = random.randint(0, len(posible_global_pos_golden_door) - 1)
filling_boxes = []
aftomat_pos = random.randint(0, 100)
key_global_pos = []
key_local_pos = []
posible_local_pos = [[1, 1], [1, 9], [9, 1], [9, 9]]
for i in range(15):
    a = random.randint(0, 24 - i)
    while [a // 5, a - (a // 5) * 5] in key_global_pos:
        a += 1
    key_global_pos.append([a // 5, a - (a // 5) * 5])
    key_local_pos.append(posible_local_pos[random.randint(0, 3)])
golden_door_pos = random.randint(0, 24)
screen_rect = (0, 0, 550, 550)
gan_global = [random.randint(0, 4), random.randint(0, 4)]
gan_local = [[1, 1], [1, 9], [9, 1], [9, 9]]
if gan_global in key_global_pos:
    gan_local.remove(key_local_pos[key_global_pos.index(gan_global)])
gan_local = random.choice(gan_local)


def choose(pos):
    if pos == [50, 50]:
        return random.choice(([100, 50], [100, 100], [50, 100]))
    elif pos == [450, 50]:
        return random.choice(([400, 50], [400, 100], [450, 100]))
    elif pos == [50, 450]:
        return random.choice(([50, 400], [100, 400], [100, 450]))
    return random.choice(([400, 450], [400, 400], [450, 400]))


class Map:
    was = []

    def draw(self):
        for el in self.was:
            pygame.draw.rect(screen, (0, 0, 0), (el[0] * 50, el[1] * 50, 51, 51), 1)
        pygame.draw.line(
            screen,
            (0, 0, 0),
            (global_pos[0] * 50 + 3, global_pos[1] * 50 + 3),
            (global_pos[0] * 50 + 50 - 6, global_pos[1] * 50 + 50 - 6),
            1,
        )
        pygame.draw.line(
            screen,
            (0, 0, 0),
            (global_pos[0] * 50 + 3, global_pos[1] * 50 + 50 - 6),
            (global_pos[0] * 50 + 50 - 6, global_pos[1] * 50 + 3),
            1,
        )


def load_image(name, colorkey=None):
    fullname = os.path.join("sprites", name)
    fullname = os.path.join("data", fullname)
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def load_level(filename):
    filename = "data/levels/" + filename
    with open(filename, "r") as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, "."), level_map))


tile_images = {
    "flor": load_image("flor.jpg"),
    "wall": load_image("wall.jpg"),
    "door": load_image("door.jpg"),
    "player": load_image("player.png"),
    "box0": load_image("box.jpg"),
    "key": load_image("new_key.png"),
    "golden_door": load_image("golden_door.jpg"),
    "start": load_image("start.jpg"),
    "end": load_image("end.jpg"),
    "portal1": load_image("portal1.png"),
    "gan": load_image("gan.png"),
    "ghost": load_image("ghost.png"),
    'vision': load_image('vision.png'),
}


def start_end_screen(tile):
    fon = pygame.transform.scale(tile_images[tile], (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


def generate_level(level):
    new_player, x, y = None, None, None
    my_map.was.append(global_pos.copy())
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == "*":
                Flor("flor", x, y)
            elif level[y][x] == "#" and (
                global_pos != posible_global_pos_golden_door[pos_golden_door]
                or [y, x] != posible_local_pos_golden_door[pos_golden_door]
            ):
                Wall("wall", x, y)
            elif level[y][x] == "@":
                Flor("flor", x, y)
            elif level[y][x] == "D":
                Flor("flor", x, y)
                Door("door", x, y)
    if global_pos == posible_global_pos_golden_door[pos_golden_door]:
        Flor("flor", *posible_local_pos_golden_door[pos_golden_door])
        Golden_door(posible_local_pos_golden_door[pos_golden_door])
    if global_pos == portal_pos:
        portal.append(Portal())
    return x, y


class Portal(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites, portal_group)
        self.image = tile_images["portal1"]
        self.pos = 0
        self.f = True
        self.rect = self.image.get_rect().move(5 * 50, 5 * 50)

    def move(self):
        if self.f:
            self.rect.y += 1
            self.pos += 1
            if self.pos == 15:
                self.f = False
        else:
            self.rect.y -= 1
            self.pos -= 1
            if self.pos == -15:
                self.f = True


class Golden_door(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__(golden_door_group, all_sprites)
        self.image = tile_images["golden_door"]
        if pos[0] != 5:
            self.image = pygame.transform.rotate(self.image, 90)
        self.rect = self.image.get_rect().move(
            tile_width * pos[0], tile_height * pos[1]
        )


class Keys(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__(key_group, all_sprites)
        self.image = tile_images["key"]
        self.pos = choose(pos)
        self.rect = self.image.get_rect().move(self.pos)


class Gan(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__(all_sprites, gan_group)
        self.image = tile_images["gan"]
        self.rect = self.image.get_rect()
        self.pos = choose(pos)
        self.rect = self.image.get_rect().move(self.pos)

    def update(self):
        if pygame.sprite.spritecollideany(self, player_group):
            self.kill()
            return True
        return False


class Flor(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(flor_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Wall(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(wall_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Door(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(door_group, all_sprites)
        self.image = tile_images[tile_type]
        if pos_x != 5:
            self.image = pygame.transform.rotate(self.image, 90)
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 30 * (pos_x == 10),
            tile_height * pos_y + 30 * (pos_y == 10),
        )


class Player(pygame.sprite.Sprite):
    def __init__(self, coins, los):
        super().__init__(player_group, all_sprites)
        self.image = tile_images["player"]
        self.direction = "Right"
        self.scale = [36, 50]
        self.was = False
        self.los = los
        self.rect = self.image.get_rect().move(
            player_pos[0] * 50 + 7, player_pos[1] * 50
        )
        self.count = coins

    def update(self, delta, direction=None):
        if direction and direction != self.direction:
            self.image = pygame.transform.flip(self.image, True, False)
            if self.direction == "Right":
                self.direction = "Left"
            else:
                self.direction = "Right"
        self.rect.x, self.rect.y = self.rect.x + delta[0], self.rect.y + delta[1]
        if pygame.sprite.spritecollideany(self, door_group):
            return True
        if (
            pygame.sprite.spritecollideany(self, wall_group)
            or pygame.sprite.spritecollideany(self, box_group)
            or self.rect.x <= 0
            or self.rect.x >= WIDTH
            or self.rect.y <= 0
            or self.rect.y >= HEIGHT
        ):
            self.rect.x, self.rect.y = self.rect.x - delta[0], self.rect.y - delta[1]
        if pygame.sprite.spritecollideany(self, key_group):
            pygame.sprite.spritecollideany(self, key_group).kill()
            self.count += 1
        if pygame.sprite.spritecollideany(self, ghost_group) and not self.was:
            self.los += self.count // 2
            self.count //= 2
            create_particles(self.rect[:2])
            self.was = True
            if self.los >= 1:
                print('Вы потеряли слишком много ключей')
                start_end_screen("end")
                sys.exit()

    def check(self):
        for delta in [[10, 10], [10, -10], [-10, 10], [-10, -10]]:
            self.rect.x, self.rect.y = self.rect.x + delta[0], self.rect.y + delta[1]
            if (
                pygame.sprite.spritecollideany(self, golden_door_group)
                and self.count >= 10
            ):
                return False, True
            if pygame.sprite.spritecollideany(self, box_group):
                box = pygame.sprite.spritecollideany(self, box_group)
                if (
                    global_pos in key_global_pos
                    and [box.rect.x // 50, box.rect.y // 50]
                    == key_local_pos[key_global_pos.index(global_pos)]
                ):
                    create_particles((box.rect.x, box.rect.y))
                    Keys(box.rect[:2])
                    key_global_pos.remove(global_pos)
                    key_local_pos.remove([box.rect.x // 50, box.rect.y // 50])
                if (
                    global_pos == gan_global
                    and [box.rect.x // 50, box.rect.y // 50] == gan_local
                    and not have_gan
                ):
                    Gan(box.rect[:2])
                    is_gan = True
            self.rect.x, self.rect.y = self.rect.x - delta[0], self.rect.y - delta[1]
        return True, False

    def port(self):
        if pygame.sprite.spritecollideany(self, portal_group):
            return True
        return False


class Ghost(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites, ghost_group)
        self.image = tile_images["ghost"]
        # self.vis = tile_images['vision']
        self.rect = self.image.get_rect().move(50 * 5, 50 * 5)
        self.rot = 0

    def rotate(self):
        self.image = pygame.transform.rotate(self.image, 90)
        self.rot += 90
        return self.rot == 450


class Vision(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites, ghost_group)
        self.image = pygame.transform.rotate(tile_images['vision'], 270)
        self.rect = self.image.get_rect().move(50 * 3 + 25, 50 * 6 - 25)
        self.rot = -90
        self.move = [[0, -200], [-100, 100], [100, 100], [100, -100]]

    def rotate(self):
        self.image = pygame.transform.rotate(self.image, 90)
        self.rot += 90
        if self.rot < 360:
            self.rect.x += self.move[self.rot // 90][0]
            self.rect.y += self.move[self.rot // 90][1]
        return self.rot == 360


class Box(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__(box_group, all_sprites)
        self.image = tile_images["box0"]
        self.rect = self.image.get_rect().move(
            tile_width * pos[0], tile_height * pos[1]
        )


class Particle(pygame.sprite.Sprite):
    # сгенерируем частицы разного размера
    fire = [load_image("new_key.png")]
    for scale in (5, 10, 20):
        fire.append(pygame.transform.scale(fire[0], (scale, scale)))

    def __init__(self, pos, dx, dy):

        super().__init__(all_sprites, particle_group)
        self.image = random.choice(self.fire)
        self.rect = self.image.get_rect()

        # у каждой частицы своя скорость - это вектор
        self.velocity = [dx, dy]
        # и свои координаты
        self.rect.x, self.rect.y = pos

        # гравитация будет одинаковой
        self.gravity = 0.25

    def update(self):
        # применяем гравитационный эффект:
        # движение с ускорением под действием гравитации
        self.velocity[1] += self.gravity
        # перемещаем частицу
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        # убиваем, если частица ушла за экран
        if not self.rect.colliderect(screen_rect):
            self.kill()


def create_particles(position):
    # количество создаваемых частиц
    particle_count = 20
    # возможные скорости
    numbers = range(-5, 6)
    for _ in range(particle_count):
        Particle(position, random.choice(numbers), random.choice(numbers))


def teleport():
    player.image = pygame.transform.scale(
        player.image, [player.scale[0] - 1, player.scale[1] - 1]
    )
    player.image = pygame.transform.rotate(player.image, 30)
    player.scale[0] -= 1
    player.scale[1] -= 1
    return player.scale[0] != 0


my_map = Map()
start_end_screen("start")
start_of_game = time.time()
level_x, level_y = generate_level(
    load_level(pos_level[str(global_pos[0]) + str(global_pos[1])])
)
box_pos = [[1, 1], [9, 9], [1, 9], [9, 1]]
boxes = []
for i in range(4):
    boxes = Box(box_pos[i])
end = False
player = Player(0, 0)
running = True
screen.fill((0, 0, 0))
is_map = 0
port = False
f = False
can = False
port_was = 0
is_ghost = pygame.USEREVENT + 1
pygame.time.set_timer(is_ghost, 30000)
rotate = pygame.USEREVENT + 2
pygame.time.set_timer(rotate, 2000)
my_ghost = None
norm = False
vis = None
while running:
    for event in pygame.event.get():
        f = False
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if player.update((-50, 0), "Left"):
                    global_pos[0] -= 1
                    player_pos[0], player_pos[1] = 9, 5
                    f = True
            elif event.key == pygame.K_RIGHT:
                if player.update((50, 0), "Right"):
                    global_pos[0] += 1
                    player_pos[0], player_pos[1] = 1, 5
                    f = True
            elif event.key == pygame.K_UP:
                if player.update((0, -50)):
                    global_pos[1] -= 1
                    player_pos[0], player_pos[1] = 5, 9
                    f = True
            elif event.key == pygame.K_DOWN:
                if player.update((0, 50)):
                    global_pos[1] += 1
                    player_pos[0], player_pos[1] = 5, 1
                    f = True
            elif event.key == pygame.K_SPACE:
                w = player.check()
                running, end = w[0], w[1]
            elif event.key == pygame.K_ESCAPE:
                is_map = (is_map + 1) % 2
            elif event.key == pygame.K_p:
                print(portal_pos)
            elif event.key == pygame.K_g:
                print(gan_global, gan_local)
            elif event.key == pygame.K_k:
                for i in range(len(key_global_pos)):
                    print(key_global_pos[i], key_local_pos[i])
            elif event.key == pygame.K_c:
                print(player.count, '/ 10')
        if event.type == is_ghost:
            ghost.append(1)
            my_ghost = Ghost()
            vis = Vision()
        if event.type == rotate and ghost:
            norm = my_ghost.rotate()
            vis.rotate()
        if norm:
            my_ghost.kill()
            my_ghost = None
            ghost = []
            norm = False
            vis.kill()
            vis = None
            player.was = False
        if player.port():
            player.rect.move(5 * 50 + 7, 5 * 50)
            player_pos = [5, 5]
            for_time = [random.randint(0, 4), random.randint(0, 4)]
            global_pos = (
                for_time
                if for_time != global_pos
                else [random.randint(0, 4), random.randint(0, 4)]
            )
            port = True
    if f or can:
        key_group = pygame.sprite.Group()
        all_sprites = pygame.sprite.Group()
        wall_group = pygame.sprite.Group()
        flor_group = pygame.sprite.Group()
        door_group = pygame.sprite.Group()
        portal_group = pygame.sprite.Group()
        vis_group = pygame.sprite.Group()
        ghost_group = pygame.sprite.Group()
        ghost = []
        portal = []
        level_x, level_y = generate_level(
            load_level(pos_level[str(global_pos[0]) + str(global_pos[1])])
        )
        a = player.count
        s = player.los
        player.kill()
        player = Player(a, s)
        port = False
        can = False
    all_sprites.draw(screen)
    door_group.draw(screen)
    box_group.draw(screen)
    key_group.draw(screen)
    particle_group.update()
    gan_group.update()
    player.update([0, 0])
    portal_group.draw(screen)
    player_group.draw(screen)
    if portal:
        portal[0].move()
    if is_map:
        screen.fill((255, 255, 255))
        my_map.draw()
    if port and port_was % 5 == 0:
        port = teleport()
        can = not port
        port_was += 1
    if port and port_was % 5 != 0:
        port_was += 1
    pygame.display.flip()
    clock.tick(FPS)
end_of_game = time.time()
if end:
    print(round(end_of_game - start_of_game, 2))
    start_end_screen("end")
