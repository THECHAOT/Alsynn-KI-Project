import pygame
import numpy as np
import network
import snake
import time

gamesize = [16, 9]
pygame.init()
display_width = pygame.display.Info().current_w * 3 // 4
display_height = pygame.display.Info().current_h * 3 // 4
display_width = display_width // gamesize[0]
display_height = display_height // gamesize[1]
rec_size = min(display_width, display_height)
screen = pygame.display.set_mode((rec_size * gamesize[0], rec_size * gamesize[1]))
last_apple_position = None
last_head_position = None
pygame.display.set_caption("Snake")
running = True
game = snake.Snake(gamesize[0], gamesize[1])
N = network.Network()
N.load_from_file(r"C:\Users\Marcel\Desktop\für präsentation\new octo\3")
vision = game.get_octo_vision
print(N.size)
gamespeed = 10
debug = False


def draw_pixel(i,j,color):
    pygame.draw.rect(screen, color, (j * rec_size, i * rec_size, rec_size, rec_size))
    
def get_color(i,j):
    return screen.get_at((j * rec_size, i * rec_size))
    

def print_field():
    global last_apple_position
    global last_head_position
    green = (50, 150, 50)
    red = (150, 25, 25)
    blue = (0, 0, 255)
    black = (0, 0, 0)
    directions = [[0, 1], [-1, 0], [0, -1], [1, 0]]
    if last_apple_position == None:
        screen.fill(black)
        draw_pixel(game.apple_position[0],game.apple_position[1],red)
        draw_pixel(game.snake[-1][0],game.snake[-1][1],blue)
        last_apple_position = game.apple_position.copy()
    
    if game.field[last_apple_position[0]][last_apple_position[1]] != 3:
        draw_pixel(last_apple_position[0],last_apple_position[1],black)
        draw_pixel(game.apple_position[0],game.apple_position[1],red)
    
    last_apple_position = game.apple_position.copy()
    head = game.snake[-1].copy()
    draw_pixel(head[0],head[1],blue)
    
    for dir in directions:
        head = game.snake[-1].copy()
        head[0]+=dir[0]
        head[1]+=dir[1]
        if 0<=head[0]<game.height and 0<=head[1]<game.width:
            if game.field[head[0], head[1]] == 1 and get_color(head[0], head[1]) != green:
                draw_pixel(head[0],head[1],green)
            elif game.field[head[0], head[1]] == 0:
                draw_pixel(head[0],head[1],black)
    
    for dir in directions:
        head = game.snake[0].copy()
        head[0]+=dir[0]
        head[1]+=dir[1]
        if 0<=head[0]<game.height and 0<=head[1]<game.width:
            if game.field[head[0], head[1]] == 1 and get_color(head[0], head[1]) != green:
                draw_pixel(head[0],head[1],green)
            elif game.field[head[0], head[1]] == 0:
                draw_pixel(head[0],head[1],black)
        

print_field()
pygame.display.update()

start = time.time()
while running:
    if not debug:
        while time.time() - start < gamespeed/100:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_g:
                        gamespeed-=1
                        print("New gamespeed:",gamespeed)
                    if event.key == pygame.K_h:
                        gamespeed+=1
                        print("New gamespeed:",gamespeed)
                    if event.key == pygame.K_SPACE:
                        #N.load_from_file("test6")
                        game.reset_game()
                        last_apple_position = None
                        continue
        start = time.time()
        #print(game.get__vision())
        action = np.argmax(N.feed_forward(vision()))
        game.move(action)
        if game.round_over:
            print("Score:",len(game.snake)-1,"\n")
            #N.load_from_file("test6")
            game.reset_game()
            last_apple_position = None
        print_field()
        pygame.display.update()
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    game.move(0)
                if event.key == pygame.K_w:
                    game.move(1)
                if event.key == pygame.K_a:
                    game.move(2)
                if event.key == pygame.K_s:
                    game.move(3)
                #game.get_octo_vision()
                print(game.apple_position)
                print_field()
                pygame.display.update()
            if game.round_over:
                game.reset_game()
                last_apple_position = None