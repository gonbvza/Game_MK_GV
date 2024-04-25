import pygame
import sys
import random
import socket
import threading

pygame.init()
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#<=== Server Properties ===>#
FORMAT = 'utf-8'
PORT = 8888
SERVER = '127.0.0.1'
ADDR = (SERVER, PORT)

#<=== End of server properties ===>#

#<=== Game properties ===>#
choose_difficulty = True

diffMult = 0

PaddleSpeeds = {"paddleA":0,}
scoreA = 0
scoreB = 0
scoreTop = 0
scoreBot = 0
#<=== End of game properties ===>#

#<=== Helper functions ===>#
def displayTxt(obj, dst):
    textRect = obj.get_rect()
    textRect.center = (screen_width // 2, 0 + dst)
    screen.blit(obj, textRect)

def playerAnimation():
    player.y += PaddleSpeeds['paddleA']
    if player.top <= 0:
        player.top = 0
    elif player.bottom >= screen_height:
        player.bottom = screen_height

def updateReceivedSpeed():
    while True:
        data = client.recv(2048)
        received = data.decode(FORMAT)
        splitted = received.split()

        if splitted[0] == "newSpeed":
            PaddleSpeeds[splitted[1]] += splitted[2]

def sendNewSpeed(speed):
    msg = f"newSpeed paddelA {speed}\n"
    msg_to_send = msg.encode(FORMAT)
    client.sendto(msg_to_send, ADDR)
#<=== End of helper functions ===>#

#<=== Screen properties ===>#
fontOptions = pygame.font.Font('freesansbold.ttf', 18)

clock = pygame.time.Clock()

screen_width = 1280
screen_height = 960
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("My pong")

bg_color = pygame.Color('grey12')
light_grey = (200,200,200)
green = (0,255,0)
blue = (0,0,255)

#<=== End of screen properties ===>#


#<=== Game rectangles ===>#
player = pygame.Rect(screen_width/2,screen_height/2 - 70, 10,140)
#<=== End of game rectangles ===>#

resend_thread = threading.Thread(target=updateReceivedSpeed, args=(),daemon=True)
resend_thread.start()
speed = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                speed += 7
                sendNewSpeed(speed)
            if event.key == pygame.K_w:
                speed += -7
                sendNewSpeed(speed)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_s:
                speed += -7
                sendNewSpeed(speed)
            if event.key == pygame.K_w:
                speed += 7
                sendNewSpeed(speed)


    playerAnimation()

    ## Draw ##
    screen.fill(bg_color)
    pygame.draw.rect(screen, light_grey, player)
    
    pygame.display.flip()
    clock.tick(60)


    