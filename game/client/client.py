import pygame
import sys
import random
import socket

pygame.init()
fontOptions = pygame.font.Font('freesansbold.ttf', 18)
clock = pygame.time.Clock()
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
bg_color = pygame.Color('grey12')
light_grey = (200,200,200)
green = (0,255,0)
blue = (0,0,255)

clientSocket.sendto(("HELLO-FROM " + "Mateusz").encode(), ("127.0.0.1", 5378))
clientSocket.sendto(("CREATE-LOBBY " + "myLobby" + " " + str(4)).encode(), ("127.0.0.1", 5378))

while(True):
    parameters, address = clientSocket.recvfrom(1280)
    parameters = parameters.decode()
    splittedParameters = parameters.split()
    
    if("SETUP" in parameters):
        for parameter in splittedParameters:
            if(parameter[:-1] == "width"):
                screen_width = int(splittedParameters[splittedParameters.index(parameter) + 1])
            
            elif(parameter[:-1] == "height"):
                screen_height = int(splittedParameters[splittedParameters.index(parameter) + 1])

            elif(parameter[:-1] == "ball"):
                ball = pygame.Rect(float(splittedParameters[splittedParameters.index(parameter) + 1]), float(splittedParameters[splittedParameters.index(parameter) + 2]), 30, 30)

            elif(parameter[:-1] == "opponent"):
                opponent = pygame.Rect(float(splittedParameters[splittedParameters.index(parameter) + 1]), float(splittedParameters[splittedParameters.index(parameter) + 2]), 10,140)
            
            elif(parameter[:-1] == "player"):
                player = pygame.Rect(float(splittedParameters[splittedParameters.index(parameter) + 1]), float(splittedParameters[splittedParameters.index(parameter) + 2]), 10,140)

        screen = pygame.display.set_mode((screen_width, screen_height))
    
    elif("SCORE" in parameters):
        scoreA = int(splittedParameters[1])
        scoreB = int(splittedParameters[2])

    elif("VELOCITY" in parameters):
        for parameter in splittedParameters:
            if(parameter[:-1] == "player"):
                player_speed = int(splittedParameters[splittedParameters.index(parameter) + 1])
            
            elif(parameter[:-1] == "opponent"):
                opponent_speed = int(splittedParameters[splittedParameters.index(parameter) + 1])

            elif(parameter[:-1] == "ball"):
                ball_speed_x = int(splittedParameters[splittedParameters.index(parameter) + 1])
                ball_speed_y = int(splittedParameters[splittedParameters.index(parameter) + 2])
        break
    else:
        pass

def ballAnimation():
    global ball_speed_x, ball_speed_y

    clientSocket.sendto(("GET-BALL-POS").encode(), ("127.0.0.1", 5378))

    clientSocket.setblocking(False)
    try:
        response, address = clientSocket.recvfrom(1280)
        response = response.decode()
        splittedResponse = response.split()

        if(response):
            if("BALL-POSITION " in response):
                print(response)
                ball.x = float(splittedResponse[1])
                ball.y = float(splittedResponse[2])
    except:
        pass
    
    if ball.colliderect(player) or ball.colliderect(opponent):
        clientSocket.sendto(("-1").encode(), ("127.0.0.1", 5378))

    return

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

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_s:
                player_speed -= 7
            if event.key == pygame.K_w:
                player_speed += 7
            if event.key == pygame.K_k:
                opponent_speed -= 7
            if event.key == pygame.K_i:
                opponent_speed += 7
    
    ballAnimation()
    playerAnimation()
    opponentMove()

    screen.fill(bg_color)
    pygame.draw.aaline(screen, light_grey, (screen_width/2, 0), (screen_width/2, screen_height))
    pygame.draw.rect(screen, light_grey, player)
    pygame.draw.rect(screen, light_grey, opponent)
    pygame.draw.ellipse(screen, light_grey, ball)

    ScoreAT = fontOptions.render(str(f"Player 1: {scoreA}"), True, pygame.Color("white"))
    textRect = ScoreAT.get_rect()
    textRect.center = (50, 0 + 50)
    screen.blit(ScoreAT, textRect)
    if ball.right >= screen_width:
        scoreA += 1
        ball.left = screen_width / 2
        ball.top = screen_height / 2
        player.top = screen_height / 2
        opponent.top = screen_height / 2

    ScoreBT = fontOptions.render(f"Player 2: {scoreB}", True, pygame.Color("white"))
    textRect = ScoreBT.get_rect()
    textRect.center = (50, 0 + 70)
    screen.blit(ScoreBT, textRect)
    if ball.left <= 0:
        scoreB += 1
        ball.left = screen_width / 2
        ball.top = screen_height / 2
        player.top = screen_height / 2
        opponent.top = screen_height / 2

    if scoreA > 3 or scoreB > 3:
        break
    
    pygame.display.flip()
    clock.tick(60)