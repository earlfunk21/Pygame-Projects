import sys

import pygame

pygame.init()
window_screen = pygame.display.set_mode((1200, 800))
window_screen_rect = window_screen.get_rect()

screen = pygame.Surface((1200, 600))
screen_rect = screen.get_rect()
screen_rect.centery = window_screen_rect.centery

# Creating a ball
ball = pygame.Rect(0, 0, 30, 30)
ball.center = screen_rect.center
ball_x = 1
ball_y = 1
ball_move = False

""" Creating a paddle """
paddle_speed = 2
paddle_height = 60
paddle_width = 5

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


font = pygame.font.Font("BodoniflfBold-MVZx.ttf", 50)


while True:
    window_screen.fill("black")
    screen.fill("grey")
    window_screen.blit(screen, screen_rect)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                ball_move = False if ball_move else True

    # If key pressed !
    key_pressed = pygame.key.get_pressed()
    if key_pressed[pygame.K_UP]:
        paddle_right.y -= paddle_speed
    if key_pressed[pygame.K_DOWN]:
        paddle_right.y += paddle_speed
    if key_pressed[pygame.K_w]:
        paddle_left.y -= paddle_speed
    if key_pressed[pygame.K_s]:
        paddle_left.y += paddle_speed

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
    if ball.x < 0:
        ball_x *= -1
    if ball.y >= screen_rect.bottom - ball.height or ball.y < screen_rect.y:
        ball_y *= -1

    # Paddle Scored
    if ball.x >= screen_rect.width or ball.x <= 0:
        if ball.x >= screen_rect.width:
            paddle_left_score += 1
        if ball.x <= 0:
            paddle_right_score += 1
        ball.center = screen_rect.center
        ball_x *= -1
        ball_y *= -1
        ball_move = False

    # Ball and Paddle Right collision
    abs_value = paddle_width / 2
    if ball.colliderect(paddle_right):
        if abs(paddle_right.top - ball.bottom) < abs_value and ball_y > 0:
            ball_y *= -1
        if abs(paddle_right.bottom - ball.top) < abs_value and ball_y > 0:
            ball_y *= -1
        if abs(paddle_right.left - ball.right) < abs_value and ball_x > 0:
            ball_x *= -1
        if abs(paddle_right.right - ball.left) < abs_value and ball_x > 0:
            ball_x *= -1

    # Ball and Paddle Left collision
    if ball.colliderect(paddle_left):
        if abs(paddle_left.top - ball.bottom) < abs_value and ball_y > 0:
            ball_y *= -1
        if abs(paddle_left.bottom - ball.top) < abs_value and ball_y > 0:
            ball_y *= -1
        if abs(paddle_left.left - ball.right) < abs_value and ball_x < 0:
            ball_x *= -1
        if abs(paddle_left.right - ball.left) < abs_value and ball_x < 0:
            ball_x *= -1

    # Moving ball
    if ball_move:
        ball.x += ball_x
        ball.y += ball_y

    # Draw all Block
    pygame.draw.ellipse(window_screen, "black", ball)
    pygame.draw.rect(window_screen, "black", paddle_right)
    pygame.draw.rect(window_screen, "black", paddle_left)

    paddle_left_text = font.render(f'{paddle_left_score}', False, "blue")
    window_screen.blit(paddle_left_text, window_screen_rect.topleft)

    paddle_right_text = font.render(f'{paddle_right_score}', False, "blue")
    window_screen.blit(paddle_right_text, (window_screen_rect.topright[0] - 30, window_screen_rect.topright[1]))

    pygame.display.flip()
