import pygame
import sys
import random
from pygame.locals import*

pygame.init()
screen = pygame.display.set_mode((1080, 720))
screen.fill((0, 0, 0))
pygame.display.set_caption("Pong")
font = pygame.font.SysFont(None, 36, bold = 5, italic = 5)

main_clock = pygame.time.Clock()
player_score = 0
computer_score = 0

#Player and CPU values
player = pygame.Rect(5, 300, 10, 200)
player_speed = 7
computer = pygame.Rect(1065, 300, 10, 200)
computer_speed = 8
alive = True

move_up = False
move_down = False

upwall = pygame.Rect(0, 0, 1080, 10)
downwall = pygame.Rect(0, 710, 1080, 10)


def draw_screen():
    screen.fill((0, 0, 0))
def draw_player():
    pygame.draw.rect(screen, (255, 255, 255), player)
def draw_computer():
    pygame.draw.rect(screen, (255, 255, 255), computer)
def draw_ball():
    ball = pygame.draw.circle(screen, (255, 255, 255), (x_position, y_position), ball_radius, ball_edge)
    return ball

def draw_upwall():
    pygame.draw.rect(screen, (255, 255, 255), upwall)
def draw_downwall():
    pygame.draw.rect(screen, (255, 255, 255), downwall)
def draw_text(display_string, font, surface, x, y):
    text_display = font.render(display_string, 1, (255, 255, 255))
    text_rect = text_display.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_display, text_rect)
def moveBall(ball, x_position, y_position):
    ball.x = x_position
    ball.y = y_position
    return ball

#CPU
def CPU(ball, y_position, computer):
    #If ball is moving away from computer, center computer
    if y_position >= 360:
            computer.y += 8
    #If ball moving towards computer, track its movement
    elif y_position <= 360:
            computer.y -= 8
    if computer.centery < ball.centery:
        computer.y += 8
    else:
        computer.y -= 8
    return computer

x_position = 30
y_position = 400
last_x = x_position
last_y = y_position

#Ball values
ball_radius = 5
ball_edge = 0
ball_can_move = False
speed = [6, -6]

while True:
    #Check for events
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        #Keyboard input for players
        if event.type == KEYDOWN:
            if event.key == K_w:
                move_down = False
                move_up = True
            if event.key == K_s:
                move_up = False
                move_down = True
        if event.type == KEYUP:
            if event.key == K_w:
                move_up = False
            if event.key == K_s:
                move_down = False
            if alive:
                if event.key == K_SPACE:
                    ball_can_move = True
            if player_score == 7:
                alive = False
                if event.key == K_RETURN:
                    alive = True
                    player_score = 0
            if computer_score == 7:
                alive = False
                if event.key == K_RETURN:
                    alive = True
                    computer_score = 0

    #Consistent FPS
    main_clock.tick(50)

    #Moving
    if move_up and player.top > 0:
        player.y -= player_speed
    if move_down and player.bottom < 720:
        player.y += player_speed
    if computer.top > 0:
        computer.y -= computer_speed
    if computer.bottom < 720:
        computer.y += computer_speed

    #Ball
    if ball_can_move:
        last_x = x_position
        last_y = y_position

        x_position += speed[0]
        y_position += speed[1]
        if ball.y <= 0:
            y_position += random.randint(15, 30)
            speed[1] = -speed[1]
        if ball.y >= 720:
            y_position -= random.randint(15, 30)
            speed[1] = -speed[1]
        if ball.x <= 0:
            computer_score += 1
            x_position = 30
            y_position = 400
            ball_can_move = False
            speed[0] = -speed[0]
        if ball.x >= 1080:
            player_score += 1
            x_position = 1050
            y_position = 400
            ball_can_move = False
            speed[0] = -speed[0]

        #Move direction vector
        move_direction = ((x_position - last_x), (y_position - last_y))

    draw_screen()
    draw_player()
    draw_computer()
    ball1 = pygame.draw.circle(screen, (255, 255, 255), (x_position, y_position), 5, 0)
    draw_upwall()
    draw_downwall()

    ball = moveBall(ball1, x_position, y_position)
    computer = CPU(ball1, y_position, computer)

    #Collisions
    if ball1.colliderect(player):
        speed[0] = -speed[0]
        x_position += random.randint(15, 30)
        y_position += random.randint(15, 30)

    if ball1.colliderect(computer):
        speed[0] = -speed[0]
        x_position -= random.randint(15, 30)
        y_position -= random.randint(15, 30)

    if player_score == 7:
        draw_text("Congratulations! You win!", font, screen, 340, 50)
        draw_text("Press enter to play again!", font, screen, 340, 125)
        ball_can_move = False
        alive = False
        x_position = 30
        y_position = 400
    elif computer_score == 7:
        draw_text("Game over!", font, screen, 440, 50)
        draw_text("Press enter to play again!", font, screen, 340, 125)
        ball_can_move = False
        alive = False
        x_position = 30
        y_position = 400

    if alive:
        draw_text("%s" % player_score, font, screen, 135, 50)
        draw_text("%s" % computer_score, font, screen, 945, 50)

    pygame.display.update()

