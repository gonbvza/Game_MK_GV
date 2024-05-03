import pygame 
import sys 
import socket

#<=== Server properties ===>#
PORT = 5378
SERVER = '127.0.0.1'
ADDR = (SERVER, PORT)
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
FORMAT = 'utf-8'
#<=== End server properties ===>#

pygame.init() 

clock = pygame.time.Clock() 
#<=== Helper functions ===>#

def displayTxt(obj, dst):
    textRect = obj.get_rect()
    textRect.center = (screen_width // 2, 0 + dst)
    screen.blit(obj, textRect)

def sendLogin(ms):
    msg_to_send = f"HELLO-FROM {ms}"
    string_bytes = msg_to_send.encode("utf-8")
    client.sendto(string_bytes, ADDR)

def openGame():

    print("Receiving")
    data = client.recv(4096)
    received = data.decode(FORMAT)
    splitted = received.split()

    print("Received")
    if splitted[0] == "HELLO":
        exec(open("mainMenu.py").read())

#<=== End of helper functions ===>#

#<=== Screen properties ===>#
screen_width = 1280
screen_height = 960
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("My pong")
bg_color = pygame.Color('grey12')
#<=== Screen properties ===>#


#<=== Username textbox properties ===>#
base_font = pygame.font.Font(None, 32) 
user_text = '' 

input_rect = pygame.Rect(screen_width / 2 - 70, 140, 140, 32) 
finish_rect = pygame.Rect(screen_width / 2 + 40, 140, 40, 32) 

color_active = pygame.Color('lightskyblue3') 
color_passive = pygame.Color('grey30') 
color = color_passive 
color2 = pygame.Color('black') 
border_color = pygame.Color('grey40')

active = False
#<=== End of username textbox properties ===># 

#<=== Helper Functions ===>#

#<=== End of helper functions ===>#

#<=== Titles properties ===>#
fontTitle = pygame.font.Font('freesansbold.ttf', 42)
fontSubTitle = pygame.font.Font('freesansbold.ttf', 22)
fontOptions = pygame.font.Font('freesansbold.ttf', 18)
#<=== End of Titles properties ===>#

def getting():
    while(True):
                print("Receiving")
                data = client.recv(4096)
                received = data.decode(FORMAT)
                splitted = received.split()
                
                print("Received")
                if splitted[0] == "GAME-START":
                    exec(open("pong_fourPlayers.py").read())


while True: 

    screen.fill(bg_color) 
    #<=== Render the main title and subtitle ===>#
    text = fontTitle.render('Please wait while other players connect', True, pygame.Color("white"))
    displayTxt(text, screen_height / 2)
    #<=== End of rendering the main title and subtitle ===>#
    
    for event in pygame.event.get():

        if event.type == pygame.QUIT: 
            pygame.quit() 
            sys.exit()
        
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                getting()

    
    listenStart()

    pygame.display.flip() 
    clock.tick(60)
