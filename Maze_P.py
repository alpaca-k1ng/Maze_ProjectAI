import sys
import pygame
from random import choice, randrange
ez_button_width = 100
ez_button_height = 50
ez_button_x = 910
ez_button_y = 10
goal_position=(800, 508)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
RES = WIDTH, HEIGHT = 900, 600
GREEN = (0, 255, 0)
TILE0= 100
TILE1= 50
TILE2= 30
TILE3= 20 
TILE=TILE3
#tạo màn hình chọn độ khó
button_width = 100
button_height = 50
button_padding = 20
button_x = (WIDTH - button_width * 3 - button_padding * 2) / 2
button_y = (HEIGHT - button_height) / 2
pygame.init()
screen = pygame.display.set_mode((900, 600))
pygame.display.set_caption("Maze Finding Game")
#self.rect.topleft = (800, 508)
#player_speed = 5
#TILE = 50
#TILE = 30


cols, rows = WIDTH // TILE, HEIGHT // TILE
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
        self.img = pygame.transform.scale(self.img, (TILE - 15, TILE - 15))
        self.rect = self.img.get_rect()
        self.set_pos()
    def set_pos(self):
        self.rect.topleft = goal_position
    def draw(self):
        game_surface.blit(self.img, self.rect)
def is_collide(x, y):
    tmp_rect = player_rect.move(x, y)
    if tmp_rect.collidelist(walls_collide_list) == -1:
        return False
    return True
def is_win():
    for food in food_list:
        if player_rect.collidepoint(food.rect.center):
            food.set_pos()
            return True
    return False
# def handle_events():
#     global direction, key_pressed, TILE
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             sys.exit()
#         if event.type == pygame.MOUSEBUTTONDOWN:
#             mouse_x, mouse_y = pygame.mouse.get_pos()
#             if ez_button_x <= mouse_x <= ez_button_x + ez_button_width and ez_button_y <= mouse_y <= ez_button_y + ez_button_height:
#                 print("Button clicked!")
#                 TILE=100      
#         if pygame.key.get_pressed():
#             pressed_key = pygame.key.get_pressed()
#             for key, key_value in keys.items():
#                 if pressed_key[key_value] and not is_collide(*directions[key]):# and not is_collide(*temp_directions[key]):
#                     if not key_pressed:
#                         direction = directions[key]
#                         key_pressed = True
#                     else:
#                         direction = (0, 0)
#                     break
#             else:
#                 key_pressed = False
#             if not is_collide(*direction) and not is_collide(*temp_directions[key]):
#                 player_rect.move_ip(direction) 
def Maze_Setup(TILE):
    # get maze
    maze = generate_maze()
    # player settings
    player_speed = 100
    player_img = pygame.image.load('img/0.png').convert_alpha()
    player_img = pygame.transform.scale(player_img, (TILE - 2 * maze[0].thickness, TILE - 2 * maze[0].thickness))
    player_rect = player_img.get_rect()
    player_rect.center = TILE // 2, TILE // 2
    
FPS = 60
pygame.init()
screen = pygame.display.set_mode((900, 600))
pygame.display.set_caption("Maze Finding Game")
game_surface = pygame.Surface(RES)
surface = pygame.display.set_mode((WIDTH + 300, HEIGHT))
clock = pygame.time.Clock()
# images
maze = generate_maze()
player_speed=10
bg_game = pygame.image.load('img/bg_1.jpg').convert()
bg = pygame.image.load('img/bg_main.jpg').convert()
directions = {'a': (-player_speed, 0), 'd': (player_speed, 0), 'w': (0, -player_speed), 's': (0, player_speed)}
temp_directions = {'a': (-player_speed/2, 0), 'd': (player_speed/2, 0), 'w': (0, -player_speed/2), 's': (0, player_speed/2)}
keys = {'a': pygame.K_a, 'd': pygame.K_d, 'w': pygame.K_w, 's': pygame.K_s}
direction = (0, 0)
# food settings
food_list = [Food() for i in range(3)]
# collision list
walls_collide_list = sum([cell.get_rects() for cell in maze], [])
surface.blit(bg, (WIDTH, 0))
surface.blit(game_surface, (0, 0))
game_surface.blit(bg_game, (0, 0))
button_rect = pygame.Rect(910, 10, 100, 50)
pygame.draw.rect(screen, GREEN, button_rect)
# fonts
font = pygame.font.SysFont('Impact', 150)
text_font = pygame.font.SysFont('Impact', 80)
    # button
while True:
    pygame.draw.rect(screen, GREEN, button_rect)
    pygame.draw.rect(screen, WHITE, (button_x, button_y, button_width, button_height))
    pygame.draw.rect(screen, GREEN, (button_x + button_width + button_padding, button_y, button_width, button_height))
    pygame.draw.rect(screen, GRAY, (button_x + button_width * 2 + button_padding * 2, button_y, button_width, button_height))
    pygame.display.update() 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if button_x <= mouse_pos[0] <= button_x + button_width and button_y <= mouse_pos[1] <= button_y + button_height:
                print("Button clicked!")
                TILE=TILE1
                Maze_Setup(TILE)              
                break
    

    surface.blit(bg, (WIDTH, 0))                
    surface.blit(game_surface, (0, 0))
    game_surface.blit(bg_game, (0, 0))
    button_rect = pygame.Rect(910, 10, 100, 50)
    is_pressed = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Kiểm tra xem chuột có nhấn vào nút không
            if event.type == pygame.MOUSEBUTTONDOWN:
            # Kiểm tra xem chuột có nhấn vào nút không
                if button_rect.collidepoint(event.pos):
                    is_pressed = True
        if event.type == pygame.MOUSEBUTTONUP:
            # Kiểm tra xem chuột có nhả nút không
            if button_rect.collidepoint(event.pos):
                is_pressed = False
    if is_pressed:
        pygame.draw.rect(screen, BLACK, button_rect)
        TILE=30
    else:
        pygame.draw.rect(screen, GREEN, button_rect)
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


    # draw player
    game_surface.blit(player_img, player_rect)

    # draw food
    [food.draw() for food in food_list]
    # print(clock.get_fps())
    pygame.display.flip()
    clock.tick(FPS)