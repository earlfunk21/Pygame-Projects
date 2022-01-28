import random
import sys

import pygame

pygame.init()
window_screen = pygame.display.set_mode((1200, 800))
window_screen_rect = window_screen.get_rect()
clock = pygame.time.Clock()
game_pause = False
won = False
won_text = None
settings = False
pygame.mixer.music.load("assets/bg_sound.mp3")
pygame.mixer.music.play(-1)

screen = pygame.Surface((1200, 600))
screen_rect = screen.get_rect()
screen_rect.centery = window_screen_rect.centery

# Creating a ball
ball = pygame.Rect(0, 0, 30, 30)
ball.center = screen_rect.center
ball_x = 3
ball_y = 5

""" Creating a paddle """
paddle_speed = 10
paddle_height = 70
paddle_width = 30

# Right Paddle
paddle_right = pygame.Rect(0, 0, paddle_width, paddle_height)
paddle_right.midright = screen_rect.midright
paddle_right.x -= paddle_width
paddle_right_score = 0

# Left Paddle
paddle_left = pygame.Rect(0, 0, paddle_width, paddle_height)
paddle_left.midleft = screen_rect.midleft
paddle_left.x += paddle_width
paddle_left_score = 0

# Sound effects
ball_bounce1 = pygame.mixer.Sound("assets/bounce_paddle.wav")
game_over_sound = pygame.mixer.Sound("assets/game_over.wav")
game_over_sound.set_volume(10)
lost = pygame.mixer.Sound("assets/lost.wav")


font = pygame.font.Font("assets/BodoniflfBold-MVZx.ttf", 50)

# Behavior
bot_enable = False
bot_levels = [random.randrange(10, 50, 10), random.randrange(30, 100, 20), random.randrange(50, 100, 50), 300]
bot_level = bot_levels[0]
change_randrange = pygame.USEREVENT + 0
pygame.time.set_timer(change_randrange, 5000)

speed_ctr = pygame.USEREVENT + 0
pygame.time.set_timer(speed_ctr, 10000)


# Curser on settings
cursor = pygame.Rect(0, 0, 30, 30)
cursor.center = (500, 454)

player1 = font.render("Easy", False, "red")
player2 = font.render("2Player", False, "red")


def bot():
    if ball_x < 0 and abs(ball.x - paddle_left.x) < bot_level:
        if random.randint(ball.y - paddle_speed, ball.y) < paddle_left.y:
            paddle_left.y -= paddle_speed
        else:
            paddle_left.y += paddle_speed


while True:
    window_screen.fill("black")
    screen.fill("grey")
    window_screen.blit(screen, screen_rect)
    if not game_pause:
        pause_text = font.render("Game Pause!", False, "red")
        window_screen.blit(pause_text, (window_screen_rect.midtop[0] - 200, window_screen_rect.midtop[1]))
        message_text = font.render("Press SPACE key to continue", False, "red")
        window_screen.blit(message_text, (window_screen_rect.midbottom[0] - 250, window_screen_rect.midbottom[1] - 70))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                game_pause = False if game_pause else True
            if event.key == pygame.K_ESCAPE:
                settings = True
                game_pause = True

        if event.type == speed_ctr:
            if ball_y < 0:
                ball_y -= 1
            if ball_y > 0:
                ball_y += 1
            if ball_x < 0:
                ball_x -= 1
            if ball_x > 0:
                ball_x += 1

        if event.type == change_randrange:
            bot_levels = [random.randrange(10, 100, 10), random.randrange(30, 150, 20), random.randrange(50, 200, 50),
                          300]

    # If key pressed !
    if game_pause:
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_UP]:
            paddle_right.y -= paddle_speed
        if key_pressed[pygame.K_DOWN]:
            paddle_right.y += paddle_speed

        if bot_enable:
            bot()
        else:
            if key_pressed[pygame.K_w]:
                paddle_left.y -= paddle_speed
            if key_pressed[pygame.K_s]:
                paddle_left.y += paddle_speed

    # Settings Screen
    while settings:
        window_screen.fill("green")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    cursor.center = (500, 454)
                    bot_enable = False
                if event.key == pygame.K_UP:
                    cursor.center = (500, 400)
                    bot_enable = True
                if event.key == pygame.K_1 and cursor.center == (500, 400):
                    player1 = font.render("Easy", False, "red")
                    bot_level = bot_levels[0]
                if event.key == pygame.K_2 and cursor.center == (500, 400):
                    player1 = font.render("Medium", False, "red")
                    bot_level = bot_levels[1]
                if event.key == pygame.K_3 and cursor.center == (500, 400):
                    player1 = font.render("Hard", False, "red")
                    bot_level = bot_levels[2]
                if event.key == pygame.K_4 and cursor.center == (500, 400):
                    player1 = font.render("Impossible", False, "red")
                    bot_level = bot_levels[3]
                if event.key == pygame.K_ESCAPE:
                    settings = False
        window_screen.blit(player1, (window_screen_rect.centerx, window_screen_rect.centery - 25))
        window_screen.blit(player2, (window_screen_rect.centerx, window_screen_rect.centery + 25))
        pygame.draw.rect(window_screen, "yellow", cursor)
        pygame.display.flip()

    """ collision paddle and ball """

    # Paddle Right
    if paddle_right.bottom >= screen_rect.bottom:
        paddle_right.bottom = screen_rect.bottom
    if paddle_right.top <= screen_rect.top:
        paddle_right.top = screen_rect.top

    # Paddle Left
    if paddle_left.bottom >= screen_rect.bottom:
        paddle_left.bottom = screen_rect.bottom
    if paddle_left.top <= screen_rect.top:
        paddle_left.top = screen_rect.top

    # Ball Top and Bottom border collision
    if ball.top <= screen_rect.top or ball.bottom >= screen_rect.bottom:
        ball_y *= -1

    # Paddle Scored
    if ball.x >= screen_rect.width or ball.x <= 0:
        if ball.x >= screen_rect.width:
            paddle_left_score += 1
        if ball.x <= 0:
            paddle_right_score += 1
        ball_x *= -1
        ball.center = screen_rect.center
        pygame.mixer.Sound.play(lost)
        if ball_y < 0:
            ball_y = -5
        if ball_y > 0:
            ball_y = 5
        if ball_x < 0:
            ball_x = -5
        if ball_x > 0:
            ball_x = 5

        # Winner
        if paddle_left_score == 7:
            won_text = font.render("Player Left won!!", False, "green")
            won = True
            pygame.mixer.music.pause()
            pygame.mixer.Sound.play(game_over_sound)
        if paddle_right_score == 7:
            won_text = font.render("Player Right won!!", False, "green")
            won = True
            pygame.mixer.music.pause()
            pygame.mixer.Sound.play(game_over_sound)

    while won:
        window_screen.fill("black")
        window_screen.blit(won_text, (window_screen_rect.centerx - 250, window_screen_rect.centery))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    won = False
                    ball_x = 5
                    ball_y = 5
                    paddle_right_score = 0
                    paddle_left_score = 0
                    pygame.mixer.music.unpause()

        pygame.display.flip()

    # Ball and Paddle Right collision
    abs_x = 10
    abs_y = 10

    if ball.colliderect(paddle_right):
        """ Paddle right collide to ball """
        if abs(paddle_right.top - ball.bottom) < abs_y and ball_y > 0 or abs(paddle_right.bottom - ball.top) < abs_y and ball_y < 0:
            ball_y *= -1
        if abs(paddle_right.left - ball.right) < abs_x and ball_x > 0 or abs(paddle_right.right - ball.left) < abs_x and ball_x < 0:
            ball_x *= -1
        pygame.mixer.Sound.play(ball_bounce1)

    # Ball and Paddle Left collision
    if ball.colliderect(paddle_left):
        if abs(paddle_left.top - ball.bottom) < abs_y and ball_y > 0:
            ball_y *= -1
        if abs(paddle_left.bottom - ball.top) < abs_y and ball_y < 0:
            ball_y *= -1
        if abs(paddle_left.left - ball.right) < abs_x and ball_x > 0:
            ball_x *= -1
        if abs(paddle_left.right - ball.left) < abs_x and ball_x < 0:
            ball_x *= -1
        pygame.mixer.Sound.play(ball_bounce1)

    # Moving ball
    if game_pause:
        ball.x += ball_x
        ball.y += ball_y

    # Draw all Block
    pygame.draw.ellipse(window_screen, "red", ball)
    pygame.draw.rect(window_screen, "black", paddle_right)
    pygame.draw.rect(window_screen, "black", paddle_left)

    paddle_left_text = font.render(f'{paddle_left_score}', False, "blue")
    window_screen.blit(paddle_left_text, window_screen_rect.topleft)

    paddle_right_text = font.render(f'{paddle_right_score}', False, "blue")
    window_screen.blit(paddle_right_text, (window_screen_rect.topright[0] - 30, window_screen_rect.topright[1]))

    pygame.display.flip()
    clock.tick(120)
