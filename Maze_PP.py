import pygame
from random import choice, randrange
RES = WIDTH, HEIGHT = 900, 600
TILE0= 100
TILE1= 50
TILE2= 30
TILE3= 20 
TILE=None
#self.rect.topleft = (800, 508)
#player_speed = 5
#TILE = 50

#TILE = 30

screen = pygame.display.set_mode((900, 600))
pygame.display.set_caption("Maze Finding Game")
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
GREEN = (0, 255, 0)
button_width = 100
button_height = 50
button_margin = 20

button1_rect = pygame.Rect(WIDTH/2 + button_margin, 30, button_width, button_height)
button2_rect = pygame.Rect(WIDTH/2 + button_margin, 90, button_width, button_height)
button3_rect = pygame.Rect(WIDTH/2 + button_margin, 150, button_width, button_height)
button4_rect = pygame.Rect(WIDTH/2 + button_margin, 210, button_width, button_height)
class Cell:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
        self.visited = False
        self.thickness = 4

    def draw(self, sc):
        x, y = self.x * TILE, self.y * TILE

        if self.walls['top']:
            pygame.draw.line(sc, pygame.Color('darkorange'), (x, y), (x + TILE, y), self.thickness)
        if self.walls['right']:
            pygame.draw.line(sc, pygame.Color('darkorange'), (x + TILE, y), (x + TILE, y + TILE), self.thickness)
        if self.walls['bottom']:
            pygame.draw.line(sc, pygame.Color('darkorange'), (x + TILE, y + TILE), (x , y + TILE), self.thickness)
        if self.walls['left']:
            pygame.draw.line(sc, pygame.Color('darkorange'), (x, y + TILE), (x, y), self.thickness)

    def get_rects(self):
        rects = []
        x, y = self.x * TILE, self.y * TILE
        if self.walls['top']:
            rects.append(pygame.Rect( (x, y), (TILE, self.thickness) ))
        if self.walls['right']:
            rects.append(pygame.Rect( (x + TILE, y), (self.thickness, TILE) ))
        if self.walls['bottom']:
            rects.append(pygame.Rect( (x, y + TILE), (TILE , self.thickness) ))
        if self.walls['left']:
            rects.append(pygame.Rect( (x, y), (self.thickness, TILE) ))
        return rects

    def check_cell(self, x, y):
        find_index = lambda x, y: x + y * cols
        if x < 0 or x > cols - 1 or y < 0 or y > rows - 1:
            return False
        return self.grid_cells[find_index(x, y)]

    def check_neighbors(self, grid_cells):
        self.grid_cells = grid_cells
        neighbors = []
        top = self.check_cell(self.x, self.y - 1)
        right = self.check_cell(self.x + 1, self.y)
        bottom = self.check_cell(self.x, self.y + 1)
        left = self.check_cell(self.x - 1, self.y)
        if top and not top.visited:
            neighbors.append(top)
        if right and not right.visited:
            neighbors.append(right)
        if bottom and not bottom.visited:
            neighbors.append(bottom)
        if left and not left.visited:
            neighbors.append(left)
        return choice(neighbors) if neighbors else False


def remove_walls(current, next):
    dx = current.x - next.x
    if dx == 1:
        current.walls['left'] = False
        next.walls['right'] = False
    elif dx == -1:
        current.walls['right'] = False
        next.walls['left'] = False
    dy = current.y - next.y
    if dy == 1:
        current.walls['top'] = False
        next.walls['bottom'] = False
    elif dy == -1:
        current.walls['bottom'] = False
        next.walls['top'] = False

def generate_maze():
    grid_cells = [Cell(col, row) for row in range(rows) for col in range(cols)]
    current_cell = grid_cells[0]
    array = []
    break_count = 1

    while break_count != len(grid_cells):
        current_cell.visited = True
        next_cell = current_cell.check_neighbors(grid_cells)
        if next_cell:
            next_cell.visited = True
            break_count += 1
            array.append(current_cell)
            remove_walls(current_cell, next_cell)
            current_cell = next_cell
        elif array:
            current_cell = array.pop()
    return grid_cells

class Food:
    def __init__(self):
        self.img = pygame.image.load('img/food.png').convert_alpha()
        self.img = pygame.transform.scale(self.img, (TILE - 10, TILE - 10))
        self.rect = self.img.get_rect()
        self.set_pos()

    def set_pos(self):
        self.rect.topleft = (900 - self.rect.width - 5, 600 - self.rect.height - 5)

    def draw(self):
        game_surface.blit(self.img, self.rect)


def is_collide(x, y):
    tmp_rect = player_rect.move(x, y)
    if tmp_rect.collidelist(walls_collide_list) == -1:
        return False
    return True


def eat_food():
    for food in food_list:
        if player_rect.collidepoint(food.rect.center):
            # food.set_pos()
            return True
    return False


# def is_game_over():
#     global time, score, record, FPS
#     if time < 0:
#         pygame.time.wait(700)
#         player_rect.center = TILE // 2, TILE // 2
#         [food.set_pos() for food in food_list]
#         set_record(record, score)
#         record = get_record()
#         time, score, FPS = 60, 0, 60


def get_record():
    try:
        with open('record') as f:
            return f.readline()
    except FileNotFoundError:
        with open('record', 'w') as f:
            f.write('0')
            return 0


def set_record(record, score):
    rec = max(int(record), score)
    with open('record', 'w') as f:
        f.write(str(rec))


FPS = 60
pygame.init()
game_surface = pygame.Surface(RES)
surface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.draw.rect(surface, pygame.Color('blue'), button1_rect)
pygame.draw.rect(surface, pygame.Color('green'), button2_rect)
pygame.draw.rect(surface, pygame.Color('red'), button3_rect)
pygame.draw.rect(surface, pygame.Color('purple'), button4_rect)

# Add text labels to the buttons
font = pygame.font.Font(None, 24)
button1_text = font.render("Button 1", True, pygame.Color('white'))
button2_text = font.render("Button 2", True, pygame.Color('white'))
button3_text = font.render("Button 3", True, pygame.Color('white'))
button4_text = font.render("Button 4", True, pygame.Color('white'))
surface.blit(button1_text, (button1_rect.x + button_width/2 - button1_text.get_width()/2, button1_rect.y + button_height/2 - button1_text.get_height()/2))
surface.blit(button2_text, (button2_rect.x + button_width/2 - button2_text.get_width()/2, button2_rect.y + button_height/2 - button2_text.get_height()/2))
surface.blit(button3_text, (button3_rect.x + button_width/2 - button3_text.get_width()/2, button3_rect.y + button_height/2 - button3_text.get_height()/2))
surface.blit(button4_text, (button4_rect.x + button_width/2 - button4_text.get_width()/2, button4_rect.y + button_height/2 - button4_text.get_height()/2))
pygame.display.flip()
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    mouse_pos = pygame.mouse.get_pos()
                    if button1_rect.collidepoint(mouse_pos):
                        print("Button 1 clicked")
                        TILE=TILE0
                        running = False
                    elif button2_rect.collidepoint(mouse_pos):
                        print("Button 2 clicked")
                        TILE=TILE1
                        running = False
                        # Add your button 2 functionality here
                    elif button3_rect.collidepoint(mouse_pos):
                        print("Button 3 clicked")
                        TILE=TILE2
                        running = False
                        # Add your button 3 functionality here
                    elif button4_rect.collidepoint(mouse_pos):
                        print("Button 4 clicked")
                        TILE=TILE3
                        running = False
                        # Add your button 4 functionality here
cols, rows = WIDTH // TILE, HEIGHT // TILE
surface = pygame.display.set_mode((WIDTH+300, HEIGHT))
# images
bg_game = pygame.image.load('img/bg_1.jpg').convert()
bg = pygame.image.load('img/bg_main.jpg').convert()

# get maze
maze = generate_maze()

# player settings
if TILE==TILE0:
    player_speed = 100
elif TILE==TILE1:
    player_speed = 50
elif TILE==TILE2:
    player_speed = 30
elif TILE==TILE3:
    player_speed = 20
player_img = pygame.image.load('img/0.png').convert_alpha()
player_img = pygame.transform.scale(player_img, (TILE - 2 * maze[0].thickness, TILE - 2 * maze[0].thickness))
player_rect = player_img.get_rect()
player_rect.center = TILE // 2, TILE // 2
directions = {'a': (-player_speed, 0), 'd': (player_speed, 0), 'w': (0, -player_speed), 's': (0, player_speed)}
temp_directions = {'a': (-player_speed/2, 0), 'd': (player_speed/2, 0), 'w': (0, -player_speed/2), 's': (0, player_speed/2)}
keys = {'a': pygame.K_a, 'd': pygame.K_d, 'w': pygame.K_w, 's': pygame.K_s}
direction = (0, 0)

# food settings
food_list = [Food() for i in range(3)]

# collision list
walls_collide_list = sum([cell.get_rects() for cell in maze], [])

# timer, score, record
# pygame.time.set_timer(pygame.USEREVENT, 1000)
# time = 60
# score = 0
# record = get_record()

# fonts
font = pygame.font.SysFont('Impact', 150)
text_font = pygame.font.SysFont('Impact', 80)

while True:   
    surface.blit(bg, (WIDTH, 0))
    surface.blit(game_surface, (0, 0))
    game_surface.blit(bg_game, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        # if event.type == pygame.USEREVENT:
        #     time -= 1

    # controls and movement
    if pygame.key.get_pressed():
        pressed_key = pygame.key.get_pressed()
        for key, key_value in keys.items():
            if pressed_key[key_value] and not is_collide(*directions[key]):# and not is_collide(*temp_directions[key]):
                if not key_pressed:
                    direction = directions[key]
                    key_pressed = True
                else:
                    direction = (0, 0)
                break
        else:
            key_pressed = False
        if not is_collide(*direction) and not is_collide(*temp_directions[key]):
            player_rect.move_ip(direction)

    # draw maze
    [cell.draw(game_surface) for cell in maze]

    # gameplay
    if eat_food():

        text_surface = font.render("You win", True, pygame.Color('white'))
        text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        game_surface.blit(text_surface, text_rect)
        pygame.display.flip()
        pygame.time.delay(1000)
        break
    #     FPS += 10
    #     score += 1d
    # is_game_over()

    # draw player
    game_surface.blit(player_img, player_rect)

    # draw food
    [food.draw() for food in food_list]

    # draw stats
    # surface.blit(text_font.render('TIME', True, pygame.Color('cyan'), True), (WIDTH + 70, 30))
    # surface.blit(font.render(f'{time}', True, pygame.Color('cyan')), (WIDTH + 70, 130))
    # surface.blit(text_font.render('score:', True, pygame.Color('forestgreen'), True), (WIDTH + 50, 350))
    # surface.blit(font.render(f'{score}', True, pygame.Color('forestgreen')), (WIDTH + 70, 430))
    # surface.blit(text_font.render('record:', True, pygame.Color('magenta'), True), (WIDTH + 30, 620))
    # surface.blit(font.render(f'{record}', True, pygame.Color('magenta')), (WIDTH + 70, 700))

    # print(clock.get_fps())
    pygame.display.flip()
    clock.tick(FPS)