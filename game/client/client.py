import pygame
import sys
import threading
import socket
import json
import time

clock = pygame.time.Clock()
internalGameState = {}

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

    clientSocket.sendto(("HELLO-FROM " + "Mateusz").encode(), ("127.0.0.1", 5378))
    clientSocket.sendto(("CREATE-LOBBY " + "myLobby" + " " + str(2)).encode(), ("127.0.0.1", 5378))

    receiving = threading.Thread(target = receive, args = (clientSocket, ))
    receiving.start()
    
    time.sleep(5)

    screen_width = internalGameState["screenWidth"]
    screen_height = internalGameState["screenHeight"]
    
    ball = pygame.Rect(internalGameState["ball"][0], internalGameState["ball"][1], 30, 30)
    opponent = pygame.Rect(internalGameState["opponent"][0], internalGameState["opponent"][1], 10,140)
    player = pygame.Rect(internalGameState["player"][0], internalGameState["player"][1], 10,140)

    opponent_speed = internalGameState["opponentSpeed"]
    player_speed = internalGameState["playerSpeed"]
  
    screen = pygame.display.set_mode((screen_width, screen_height))

    while(True):
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    print("Key is actively pressed")
                    clientSocket.sendto(("pygame.KEYDOWN " + "playerSpeed" + " " + str(4)).encode(), ("127.0.0.1", 5378))
                    
                if event.key == pygame.K_w:
                    clientSocket.sendto(("pygame.KEYDOWN " + "playerSpeed" + " " + str(-4)).encode(), ("127.0.0.1", 5378))
                    
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_s: 
                    clientSocket.sendto(("pygame.KEYDOWN " + "playerSpeed" + " " + str(4)).encode(), ("127.0.0.1", 5378))
                    
                if event.key == pygame.K_w:
                    clientSocket.sendto(("pygame.KEYDOWN " + "playerSpeed" + " " + str(-4)).encode(), ("127.0.0.1", 5378))
            
        ball.x = internalGameState["ball"][0]
        ball.y = internalGameState["ball"][1]

        player.x = internalGameState["player"][0]
        player.y = internalGameState["player"][1]
        
        opponent.x = internalGameState["opponent"][0]
        opponent.y = internalGameState["opponent"][1]

        screen.fill(pygame.Color('grey12'))
        pygame.draw.aaline(screen, (200,200,200), (screen_width/2, 0), (screen_width/2, screen_height))
        pygame.draw.rect(screen, (200,200,200), player)
        pygame.draw.rect(screen, (200,200,200), opponent)
        pygame.draw.ellipse(screen, (200,200,200), ball)

        pygame.display.flip()
        clock.tick(60)

main()
exit()