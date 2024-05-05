import pygame
import sys
import threading
import socket
import json
import time

pygame.font.init()
fontOptions = pygame.font.Font('freesansbold.ttf', 18)
clock = pygame.time.Clock()
internalGameState = {}

IP = "127.0.0.1"

def receive(clientSocket):
    global internalGameState
    while(True):

        response, address = clientSocket.recvfrom(1024)
        response = response.decode()

        if("DATA" in response):
            response = response.replace("DATA ", "")
            internalGameState = json.loads(response)
        else:
            pass
        
def main():
    global internalGameState
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    pygame.init()

    username = input("Enter your username: ")
    choice = input("Create lobby (Y/N): ")

    if(choice == "Y"):
        clientSocket.sendto(("HELLO-FROM " + username).encode(), (IP, 5378))
        clientSocket.sendto(("CREATE-LOBBY " + "myLobby" + " " + str(2)).encode(), (IP, 5378))
    
    else:
        clientSocket.sendto(("HELLO-FROM " + username).encode(), (IP, 5378))
        clientSocket.sendto(("JOIN " + "myLobby").encode(), (IP, 5378))

    while(True):
        response, address = clientSocket.recvfrom(1024)
        response = response.decode()
    
        if("GAME-START" in response):
            print("I'm here!")
            break

    receiving = threading.Thread(target = receive, args = (clientSocket, ))
    receiving.start()
    
    time.sleep(5)

    screen_width = internalGameState["screenWidth"]
    screen_height = internalGameState["screenHeight"]

    playerName = str(internalGameState["usernames"][0])
    opponentName = str(internalGameState["usernames"][1])
    
    ball = pygame.Rect(internalGameState["ball"][0], internalGameState["ball"][1], 30, 30)
    opponent = pygame.Rect(internalGameState[opponentName][0], internalGameState[opponentName][1], 10,140)
    player = pygame.Rect(internalGameState[playerName][0], internalGameState[playerName][1], 10,140)

    screen = pygame.display.set_mode((screen_width, screen_height))

    while(True):

        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    print("Key is actively pressed")
                    clientSocket.sendto(("pygame.KEYDOWN " + username + "Speed" + " " + str(4)).encode(), (IP, 5378))
                    
                if event.key == pygame.K_w:
                    clientSocket.sendto(("pygame.KEYDOWN " + username + "Speed" + " " + str(-4)).encode(), (IP, 5378))
                    
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_s: 
                    clientSocket.sendto(("pygame.KEYDOWN " + username + "Speed" + " " + str(4)).encode(), (IP, 5378))
                    
                if event.key == pygame.K_w:
                    clientSocket.sendto(("pygame.KEYDOWN " + username + "Speed" + " " + str(-4)).encode(), (IP, 5378))
            
        ball.x = internalGameState["ball"][0]
        ball.y = internalGameState["ball"][1]

        player.x = internalGameState[playerName][0]
        player.y = internalGameState[playerName][1]
        
        opponent.x = internalGameState[opponentName][0]
        opponent.y = internalGameState[opponentName][1]

        screen.fill(pygame.Color('grey12'))
        pygame.draw.aaline(screen, (200,200,200), (screen_width/2, 0), (screen_width/2, screen_height))
        pygame.draw.rect(screen, (200,200,200), player)
        pygame.draw.rect(screen, (200,200,200), opponent)
        pygame.draw.ellipse(screen, (200,200,200), ball)

        scorePosition = 20
        for item in internalGameState["usernames"]:
            ScoreTop = fontOptions.render((item + ": " + str(internalGameState["scoreboard"][item])), True, pygame.Color("white"))
            textRect = ScoreTop.get_rect()
            textRect.center = (len(item) + 50, 0 + scorePosition)
            scorePosition += 20
            screen.blit(ScoreTop, textRect)

        pygame.display.flip()
        clock.tick(60)

main()
exit()