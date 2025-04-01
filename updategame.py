import pygame
import random

#initializing pygame
pygame.init()
pygame.mixer.init()

#define height and width
screen_width = 300
screen_height = 600
gameareaheight = 550
scoreboardheight = 50
car_width = 60
car_height = 80

#making game window
gamespace = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Tanjim's Car Game")
clock = pygame.time.Clock()

#define colors
white = (255, 255, 255)
black = (0, 0, 0)
fontcolor = (145, 199, 213)
ash = (160, 174, 177)

#loading images
car_img = pygame.image.load('CAR.png')
car_img = pygame.transform.scale(car_img, (car_width, car_height))
road_img = pygame.image.load('road1.png')
road_img = pygame.transform.scale(road_img, (screen_width, screen_height))
obs_img = pygame.image.load('obscar.png')
obs_img = pygame.transform.scale(obs_img, (car_width, car_height))
bg_img = pygame.image.load('bg3.jpg')
bg_img = pygame.transform.scale(bg_img, (screen_width, screen_height))

#usage of text
def draw_text(text, x, y, size=30, color = fontcolor):
    font = pygame.font.Font("gamefont.ttf", size)
    text_surface = font.render(text, True, color)
    gamespace.blit(text_surface, (x, y))

#player's car draw
def draw_car(x, y):
    gamespace.blit(car_img, (x, y))

#print scoreboard
def show_score(score):
    pygame.draw.rect(gamespace, ash, [0, 0, screen_width, scoreboardheight])
    draw_text(f"Score: {score}", screen_width //2 - 60, 10, 35, black)

#game over window
def gameoverscreen(score):
    #gamespace.fill(black)
    running = True
    while running:
        gamespace.blit(bg_img,(0,0))
        draw_text("GAME OVER", screen_width // 2 - 120, screen_height // 2 - 100, 50, fontcolor)
        draw_text(f"Final Score: {score}", screen_width // 2 - 120, screen_height // 2 - 40, 30, fontcolor)
        #pygame.time.delay(3000)
        draw_text("Main Menu", screen_width // 2 - 80, screen_height // 2 + 40, 30, fontcolor)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if screen_width // 2 - 80 <= mouse_x <= screen_width // 2 + 80 and screen_height // 2 + 40 <= mouse_y <= screen_height // 2 + 70:
                    main_menu()
                    return

#main game part
def game_loop():
    pygame.mixer.music.load("cargamemusic.mp3")
    pygame.mixer.music.set_volume(1.0)
    pygame.mixer.music.play(-1)
    
    x = screen_width // 2 - car_width // 2
    y = screen_height - car_height - 10
    x_change = 0
    #y_change = 0
    obstacle_width = 50
    obstacle_height = 60
    obstacle_x = random.randint(0, screen_width - obstacle_width)
    obstacle_y = -50
    obstacle_speed = 10
    score = 0

    game_over = False
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -5
                if event.key == pygame.K_RIGHT:
                    x_change = 5
               # if event.key == pygame.K_UP:
                #    y_change = -2
               # if event.key == pygame.K_DOWN:
                #    y_change = 2
            if event.type == pygame.KEYUP:
               if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0
        
        x += x_change
        #y +=y_change

        if x < 0:
            x = 0
        elif x > screen_width - car_width:
            x = screen_width - car_width

        obstacle_y += obstacle_speed

        if obstacle_y > screen_height:
            obstacle_y = -50
            obstacle_x = random.randint(0, screen_width - obstacle_width)
            score += 1

        if y < obstacle_y + obstacle_height:
            if x > obstacle_x and x < obstacle_x + obstacle_width or \
                x + car_width > obstacle_x and x + car_width < obstacle_x + obstacle_width:
                pygame.mixer.music.stop() 
                gameoverscreen(score)
                return
        
        gamespace.blit(road_img, (0, 0))

        draw_car(x, y)
        gamespace.blit(obs_img, (obstacle_x, obstacle_y))
                
        show_score(score)
        pygame.display.update()
        clock.tick(80)

# menu and instrucstion part 
def show_instructions():
    running = True
    while running:
        #gamespace.fill(white)
        gamespace.blit(bg_img,(0,0))
        draw_text("Instructions:", 30, 80, 40)
        draw_text("1. Use arrow keys", 20, 150, 25)
        draw_text(" to move", 35, 175, 25)
        draw_text("2. Avoid obstacles", 20, 220, 25)
        draw_text("Click anywhere ", 40, 280, 25)
        draw_text("to go back", 40, 310, 25)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                return

def main_menu():
    running = True
    while running:
        #gamespace.fill(black)
        gamespace.blit(bg_img,(0,0))
        start_rect = pygame.Rect(80, 200, 140, 30)
        instructions_rect = pygame.Rect(80, 250, 140, 30)
        exit_rect = pygame.Rect(80, 300, 140, 30)

        draw_text("Car Game", 60, 140, 40)
        draw_text("1. Start Game", 40, 210, 30)
        draw_text("2. Instructions", 40, 260, 30)
        draw_text("3. Exit", 40, 320, 30)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if start_rect.collidepoint(mouse_x, mouse_y):
                    game_loop()
                elif instructions_rect.collidepoint(mouse_x, mouse_y):
                    show_instructions()
                elif exit_rect.collidepoint(mouse_x, mouse_y):
                    pygame.quit()
                    return

main_menu()
