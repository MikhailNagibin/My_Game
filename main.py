import pygame
import os
import random
import sys
import time

FPS = 50
WIDTH, HEIGHT = 550, 550
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
wall_group = pygame.sprite.Group()
flor_group = pygame.sprite.Group()
door_group = pygame.sprite.Group()
ghost_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
box_group = pygame.sprite.Group()
key_group = pygame.sprite.Group()
golden_door_group = pygame.sprite.Group()
global_pos = [2, 2]
player_pos = [5, 5]
portal_pos = [random.randint(0, 5), random.randint(0, 5)]
tile_width = tile_height = 50
pos_level = {
    '00': "00.txt",
    '01': "стена1.txt",
    '02': "стена1.txt",
    '03': "стена1.txt",
    '04': "011.txt",
    '10': "стена2.txt",
    '11': "середина.txt",
    '12': "середина.txt",
    '13': "середина.txt",
    '14': "стена4.txt",
    '20': "стена2.txt",
    '21': "середина.txt",
    '22': "середина.txt",
    '23': "середина.txt",
    '24': "стена4.txt",
    '30': "стена2.txt",
    '31': "середина.txt",
    '32': "середина.txt",
    '33': "середина.txt",
    '34': "стена4.txt",
    '40': "110.txt",
    '41': "стена3.txt",
    '42': "стена3.txt",
    '43': "стена3.txt",
    '44': "1111.txt",
}

posible_global_pos_golden_door = [[0, 0], [0, 1], [0, 2], [0, 3], [0, 4], [0, 4], [1, 4], [2, 4], [3, 4], [4, 4],
                                  [4, 4], [4, 3], [4, 2], [4, 1], [4, 0], [4, 0], [3, 0], [2, 0], [1, 0], [0, 0]]
posible_local_pos_golden_door = [[0, 5]] * 5 + [[5, 10]] * 5 + [[10, 5]] * 5 + [[5, 0]] * 5
pos_golden_door = random.randint(0, len(posible_global_pos_golden_door) - 1)
print(posible_global_pos_golden_door[pos_golden_door], posible_local_pos_golden_door[pos_golden_door])
filling_boxes = []
aftomat_pos = random.randint(0, 100)
key_global_pos = []
key_local_pos = []
posible_local_pos = [[1, 1], [9, 1], [9, 1], [9, 9]]
for i in range(15):
    a = random.randint(0, 24 - i)
    while [a // 5, a - (a // 5) * 5] in key_global_pos:
        a += 1
    key_global_pos.append([a // 5, a - (a // 5) * 5])
    key_local_pos.append(posible_local_pos[random.randint(0, 3)])

golden_door_pos = random.randint(0, 24)


def load_image(name, colorkey=None):
    fullname = os.path.join('sprites', name)
    fullname = os.path.join('data', fullname)
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
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


tile_images = {
    "flor": load_image("flor.jpg"),
    "wall": load_image("wall.jpg"),
    "door": load_image("door.jpg"),
    # "ghost": load_image("ghost.jpg"),
    "player": load_image("player.png"),
    "box0": load_image("box.jpg"),
    "key": load_image("key.jpg"),
    "golden_door": load_image("golden_door.jpg"),
    "start": load_image("start.jpg"),
    "end": load_image("end.jpg")
}

def start_end_screen(tile):
    fon = pygame.transform.scale(tile_images[tile], (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


def generate_level(level):
    new_player, x, y = None, None, None
    print(global_pos)
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '*':
                Flor('flor', x, y)
            elif (level[y][x] == '#' and
                  (global_pos != posible_global_pos_golden_door[pos_golden_door] or
                   [y, x] != posible_local_pos_golden_door[pos_golden_door])):
                Wall('wall', x, y)
            elif level[y][x] == '@':
                Flor('flor', x, y)
            elif level[y][x] == 'D':
                Flor('flor', x, y)
                Door('door', x, y)
    if global_pos == posible_global_pos_golden_door[pos_golden_door]:
        Flor('flor', *posible_local_pos_golden_door[pos_golden_door])
        Golden_door(posible_local_pos_golden_door[pos_golden_door])
    return x, y


class Golden_door(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__(golden_door_group, all_sprites)
        self.image = tile_images['golden_door']
        if pos[0] != 5:
            self.image = pygame.transform.rotate(self.image, 90)
        self.rect = self.image.get_rect().move(
            tile_width * pos[0], tile_height * pos[1])


class Keys(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__(key_group, all_sprites)
        self.image = tile_images['key']

        self.rect = self.image.get_rect().move(
            tile_width * pos[0], tile_height * pos[1])


class Flor(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(flor_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Wall(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(wall_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Door(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(door_group, all_sprites)
        self.image = tile_images[tile_type]
        if pos_x != 5:
            self.image = pygame.transform.rotate(self.image, 90)
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 30 * (pos_x == 10), tile_height * pos_y + 30 * (pos_y == 10))


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(player_group, all_sprites)
        self.image = tile_images['player']
        self.direction = "Right"
        self.rect = self.image.get_rect().move(player_pos[0] * 50 + 7, player_pos[1] * 50)

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
        if (pygame.sprite.spritecollideany(self, wall_group) or pygame.sprite.spritecollideany(self, box_group) or
                self.rect.x <= 0 or self.rect.x >= WIDTH or self.rect.y <= 0 or self.rect.y >= HEIGHT):
            self.rect.x, self.rect.y = self.rect.x - delta[0], self.rect.y - delta[1]

    def check(self):
        for delta in [[10, 10], [10, -10], [-10, 10], [-10, -10]]:
            self.rect.x, self.rect.y = self.rect.x + delta[0], self.rect.y + delta[1]
            if pygame.sprite.spritecollideany(self, golden_door_group):
                return False, True
            self.rect.x, self.rect.y = self.rect.x - delta[0], self.rect.y - delta[1]
        return True, False


class Box(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__(box_group, all_sprites)
        self.image = tile_images['box0']
        self.rect = self.image.get_rect().move(
            tile_width * pos[0], tile_height * pos[1])


start_end_screen('start')
start_of_game = time.time()
level_x, level_y = generate_level(load_level(pos_level[str(global_pos[0]) + str(global_pos[1])]))
box_pos = [[1, 1], [9, 9], [1, 9], [9, 1]]
boxes = []
for i in range(4):
    boxes = Box(box_pos[i])
end = False
player = Player()
running = True
screen.fill((0, 0, 0))
while running:
    for event in pygame.event.get():
        f = False
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if player.update((-10, 0), "Left"):
                    global_pos[0] -= 1
                    player_pos[0], player_pos[1] = 9, 5
                    f = True
            elif event.key == pygame.K_RIGHT:
                if player.update((10, 0), "Right"):
                    global_pos[0] += 1
                    player_pos[0], player_pos[1] = 1, 5
                    f = True
            elif event.key == pygame.K_UP:
                if player.update((0, -10)):
                    global_pos[1] -= 1
                    player_pos[0], player_pos[1] = 5, 9
                    f = True
            elif event.key == pygame.K_DOWN:
                if player.update((0, 10)):
                    global_pos[1] += 1
                    player_pos[0], player_pos[1] = 5, 1
                    f = True
            elif event.key == pygame.K_SPACE:
                w = player.check()
                running, end = w[0], w[1]
            if f:
                all_sprites = pygame.sprite.Group()
                wall_group = pygame.sprite.Group()
                flor_group = pygame.sprite.Group()
                door_group = pygame.sprite.Group()
                level_x, level_y = generate_level(
                    load_level(pos_level[str(global_pos[0]) + str(global_pos[1])]))
                player.kill()
                player = Player()
    all_sprites.draw(screen)
    door_group.draw(screen)
    player_group.draw(screen)
    box_group.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)
end_of_game = time.time()
if end:
    print(round(end_of_game - start_of_game, 2))
    start_end_screen('end')