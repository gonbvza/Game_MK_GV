import pygame
import sys
import random
import socket


pygame.init()

def displayTxt(obj, dst):
    textRect = obj.get_rect()
    textRect.center = (screen_width // 2, 0 + dst)
    screen.blit(obj, textRect)

fontOptions = pygame.font.Font('freesansbold.ttf', 18)

def ballAnimation():
    global ball_speed_x, ball_speed_y

    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if ball.top <= 0 or ball.bottom >= screen_height:
        #ball_speed_y *= -1
        pass
    elif ball.left <= 0 or ball.right >= screen_width:
        ball_speed_x *= -1

    if ball.colliderect(player) or ball.colliderect(opponent):
        ball_speed_x *= -1
    elif ball.colliderect(playerTop) or ball.colliderect(playerBot):
        ball_speed_y *= -1

def playerAnimation():
    player.y += player_speed
    if player.top <= 0:
        player.top = 0
    elif player.bottom >= screen_height:
        player.bottom = screen_height

def opponentMove():
    opponent.y += opponent_speed
    if  opponent.top <= 0:
        opponent.top = 0
    elif opponent.bottom >= screen_height:
        opponent.bottom = screen_height 

def playerTopMovement():
    playerTop.x += playerTop_speed
    if playerTop.right >= screen_width:
        playerTop.right = screen_width
    elif playerTop.left <= 0:
        playerTop.left = 0

def playerBotMovement():
    playerBot.x += playerBot_speed
    if playerTop.right >= screen_width:
        playerTop.right = screen_width
    elif playerTop.left <= 0:
        playerTop.left = 0


clock = pygame.time.Clock()

screen_width = 1280
screen_height = 960
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("My pong")

## Game rectangles ##
ball = pygame.Rect(screen_width/2 - 15,screen_height/2 - 15,30,30)
playerTop = pygame.Rect(screen_width/2 - 70,20, 140,10)
playerBot = pygame.Rect(screen_width/2 - 70,screen_height - 20, 140,10)
opponent = pygame.Rect(screen_width - 20,screen_height/2 - 70, 10,140)
player = pygame.Rect(10,screen_height/2 - 70, 10,140)

bg_color = pygame.Color('grey12')
light_grey = (200,200,200)
green = (0,255,0)
blue = (0,0,255)

choose_difficulty = True
player_speed = 0
opponent_speed = 0
playerTop_speed = 0
playerBot_speed = 0


scoreA = 0
scoreB = 0
scoreTop = 0
scoreBot = 0

while choose_difficulty:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                ball_speed_x = 5
                ball_speed_y = 7
                player_speed = 0
                opponent_speed = 0
                choose_difficulty = False
            if event.key == pygame.K_2:
                ball_speed_x = 8
                ball_speed_y = 10
                player_speed = 0
                opponent_speed = 0
                choose_difficulty = False
            if event.key == pygame.K_3:
                ball_speed_x = 11
                ball_speed_y = 13
                player_speed = 0
                opponent_speed = 0
                choose_difficulty = False

    # Display the difficulty options
    screen.fill(bg_color)
    textOption1 = fontOptions.render('[1] -- Easy', True, pygame.Color("white"))
    textOption2 = fontOptions.render('[2] -- Medium', True, pygame.Color("white"))
    textOption3 = fontOptions.render('[3] -- Hard', True, pygame.Color("white"))
    displayTxt(textOption1, 120)
    displayTxt(textOption2, 150)
    displayTxt(textOption3, 180)

    pygame.display.flip()
    clock.tick(60)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                player_speed += 7
            if event.key == pygame.K_w:
                player_speed -= 7
            if event.key == pygame.K_k:
                opponent_speed += 7
            if event.key == pygame.K_i:
                opponent_speed -= 7
            if event.key == pygame.K_d:
                playerTop_speed += 7
            if event.key == pygame.K_a:
                playerTop_speed -= 7
            if event.key == pygame.K_l:
                playerBot_speed += 7
            if event.key == pygame.K_j:
                playerBot_speed -= 7

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_s:
                player_speed -= 7
            if event.key == pygame.K_w:
                player_speed += 7
            if event.key == pygame.K_k:
                opponent_speed -= 7
            if event.key == pygame.K_i:
                opponent_speed += 7
            if event.key == pygame.K_d:
                playerTop_speed -= 7
            if event.key == pygame.K_a:
                playerTop_speed += 7
            if event.key == pygame.K_l:
                playerBot_speed -= 7
            if event.key == pygame.K_j:
                playerBot_speed += 7
    
    ballAnimation()
    playerAnimation()
    opponentMove()
    playerTopMovement()
    playerBotMovement()


    ## Draw ##
    screen.fill(bg_color)
    pygame.draw.aaline(screen, light_grey, (screen_width/2, 0), (screen_width/2, screen_height))
    pygame.draw.rect(screen, light_grey, player)
    pygame.draw.rect(screen, light_grey, opponent)
    pygame.draw.rect(screen, light_grey, playerTop)
    pygame.draw.rect(screen, light_grey, playerBot)
    pygame.draw.ellipse(screen, light_grey, ball)

    ## score for A ##

    ScoreAT = fontOptions.render(str(f"Player 1: {scoreA}"), True, pygame.Color("white"))
    textRect = ScoreAT.get_rect()
    textRect.center = (50, 0 + 50)
    screen.blit(ScoreAT, textRect)
    if ball.right >= screen_width:
        scoreA += 1
        scoreTop += 1
        scoreBot += 1
        ball.left = screen_width / 2
        ball.top = screen_height / 2
        player.top = screen_height / 2
        opponent.top = screen_height / 2

    ## Score for B ##
    ScoreBT = fontOptions.render(f"Player 2: {scoreB}", True, pygame.Color("white"))
    textRect = ScoreBT.get_rect()
    textRect.center = (50, 0 + 70)
    screen.blit(ScoreBT, textRect)
    if ball.left <= 0:
        scoreB += 1
        scoreTop += 1
        scoreBot += 1
        ball.left = screen_width / 2
        ball.top = screen_height / 2
        player.top = screen_height / 2
        opponent.top = screen_height / 2

    ScoreTop = fontOptions.render(str(f"Player 3: {scoreTop}"), True, pygame.Color("white"))
    textRect = ScoreTop.get_rect()
    textRect.center = (50, 0 + 100)
    screen.blit(ScoreTop, textRect)
    if ball.top < 0:
        scoreA += 1
        scoreB += 1
        scoreBot += 1
        ball.left = screen_width / 2
        ball.top = screen_height / 2
        player.top = screen_height / 2
        opponent.top = screen_height / 2

    ## Score for B ##
    ScoreBot = fontOptions.render(f"Player 4: {scoreBot}", True, pygame.Color("white"))
    textRect = ScoreBot.get_rect()
    textRect.center = (50, 0 + 120)
    screen.blit(ScoreBot, textRect)
    if ball.bottom >=screen_height:
        scoreB += 1
        scoreA += 1
        scoreTop += 1
        ball.left = screen_width / 2
        ball.top = screen_height / 2
        # player.top = screen_height / 2
        # opponent.top = screen_height / 2

    if scoreA > 3 or scoreB > 3:
        break
    
    pygame.display.flip()
    clock.tick(60)