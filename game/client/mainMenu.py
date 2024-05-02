import pygame 
import sys 
import socket

#<=== Server properties ===>#
PORT = 5378
SERVER = '127.0.0.1'
ADDR = (SERVER, PORT)
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
FORMAT = 'utf-8'
Lobbies = []
#<=== End server properties ===>#

pygame.init() 

clock = pygame.time.Clock() 
#<=== Helper functions ===>#
def listenCalls():
    data = client.recv(4096)
    received = data.decode(FORMAT)
    splitted = received.split()
    print(received)

    if splitted[0] == "CREATE-OK" or splitted[0] == "JOIN-OK":
        print("went into ")
        exec(open("waitingScreen.py").read())

def displayTxt(obj, dst, x):
    textRect = obj.get_rect()
    textRect.center = (x, 0 + dst)
    screen.blit(obj, textRect)

def sendLobby(name, users):
    msg_to_send = f"CREATE-LOBBY {name} {users}\n"
    print(msg_to_send)
    string_bytes = msg_to_send.encode("utf-8")
    client.sendto(string_bytes, ADDR)

def sendLogin(name):
    msg_to_send = f"JOIN {name}\n"
    string_bytes = msg_to_send.encode("utf-8")
    client.sendto(string_bytes, ADDR)

def listRefresh():
    global Lobbies
    msg_to_send = f"LIST-LOBBY\n"
    
    string_bytes = msg_to_send.encode("utf-8")
    client.sendto(string_bytes, ADDR)

    data = client.recv(4096)
    received = data.decode(FORMAT)
    splitted = received.split()

    if splitted[0] == "LIST-LOBBY":
        print("Listed")
        try:
            if splitted[1]:
                Lobbies = splitted[1:]
        except IndexError as e:
            print("No lobbies")

listRefresh()
#<=== End of helper functions ===>#

#<=== Screen properties ===>#
screen_width = 1280
screen_height = 960
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("My pong")
bg_color = pygame.Color('grey12')
#<=== Screen properties ===>#


#<=== Username input properties ===>#
base_font = pygame.font.Font(None, 32) 
user_text = ''
name_text = ''
joinName = ''

createLobby_rect = pygame.Rect(screen_width / 2 - 150, 140, 300, 32) 
joinLobby_rect = pygame.Rect(screen_width / 2 - 150, 185, 300, 32) 

lobbyName = pygame.Rect(screen_width / 2 + 180, 140, 300, 32) 
lobbyUsers = pygame.Rect(screen_width / 2 + 490, 140, 50, 32) 

joinLobbyName = pygame.Rect(screen_width / 2 + 180, 185, 300, 32) 

lobbies = pygame.Rect(screen_width / 2 - 250, 280, 500, 200) 
refresh = pygame.Rect(screen_width / 2 + 50, 500, 200, 32) 

color_active = pygame.Color('lightskyblue3') 
color_passive = pygame.Color('grey30') 
color = color_passive 
colorInputName = color_passive
colorInputUser = color_passive
colorJoinName = color_passive
color2 = pygame.Color('black') 
border_color = pygame.Color('grey40')

activeName = False
activeUser = False
activeJoinName = False
#<=== End of username textbox properties ===># 


#<=== Titles properties ===>#
fontTitle = pygame.font.Font('freesansbold.ttf', 42)
fontSubTitle = pygame.font.Font('freesansbold.ttf', 22)
fontOptions = pygame.font.Font('freesansbold.ttf', 18)
#<=== End of Titles properties ===>#

while True: 

    screen.fill(bg_color) 

    #<=== Render the main title and subtitle ===>#
    text = fontTitle.render('Welcome to Pong', True, pygame.Color("white"))
    textSub = fontSubTitle.render('Please choose an option', True, pygame.Color("white"))
    textSub2 = fontSubTitle.render('Available lobbies', True, pygame.Color("white"))
    refreshText = fontSubTitle.render('Refresh lobbies', True, pygame.Color("white"))
    displayTxt(text, 40, screen_width // 2)
    displayTxt(textSub, 90, screen_width // 2)
    displayTxt(textSub2, 260, screen_width // 2)
    
    #<=== End of rendering the main title and subtitle ===>#

    for event in pygame.event.get(): 

        if event.type == pygame.QUIT: 
            pygame.quit() 
            sys.exit() 
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if joinLobby_rect.collidepoint(event.pos): 
                print("Join lobby")
            elif createLobby_rect.collidepoint(event.pos): 
                print("Create lobby")
        
        if event.type == pygame.MOUSEBUTTONDOWN: 
            if lobbyName.collidepoint(event.pos): 
                activeName = True
            elif lobbyUsers.collidepoint(event.pos): 
                activeUser = True
            elif joinLobbyName.collidepoint(event.pos):
                activeJoinName = True
            elif refresh.collidepoint(event.pos):
                listRefresh()
            elif createLobby_rect.collidepoint(event.pos): 
                name_text = name_text[:]
                print(name_text)
                print(user_text)
        
                sendLobby(name_text,user_text)
                listenCalls()
            elif joinLobby_rect.collidepoint(event.pos): 
                print(joinName)
                if joinName == '':
                    print("Something empty")
                else:
                    sendLogin(joinName)
                    listenCalls()
            else:
                activeName = False 
                activeUser = False
                activeJoinName = False

        if event.type == pygame.KEYDOWN:
            if activeName:
                if event.key == pygame.K_RETURN:
                    print(name_text)  # Here you can do whatever you want with the text
                    name_text = ''
                elif event.key == pygame.K_BACKSPACE:
                    name_text = name_text[:-1]
                elif len(name_text) < 10:
                    name_text += event.unicode
            elif activeUser:
                if event.key == pygame.K_RETURN:
                    pass
                elif event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                elif len(user_text) < 1:
                    if event.unicode.isdigit():
                        user_number = int(event.unicode)
                        if 1 < user_number < 4:
                            user_text += event.unicode
            elif activeJoinName:
                if event.key == pygame.K_RETURN:
                    print(joinName)  # Here you can do whatever you want with the text
                    joinName = ''
                elif event.key == pygame.K_BACKSPACE:
                    joinName = name_text[:-1]
                elif len(joinName) < 10:
                    joinName += event.unicode


    if activeName: 
        colorInputName = color_active 
    elif activeUser:
        colorInputUser = color_active
    elif activeJoinName:
        colorJoinName = color_active
    else: 
        colorInputName = color_passive 
        colorInputUser = color_passive 
        colorJoinName = color_passive

    #<=== Join and create lobby buttons ===>#
    pygame.draw.rect(screen, color, createLobby_rect)
    pygame.draw.rect(screen, color, joinLobby_rect)
    pygame.draw.rect(screen, colorInputName, lobbyName)
    pygame.draw.rect(screen, colorInputUser, lobbyUsers)
    pygame.draw.rect(screen, colorJoinName, joinLobbyName)
    pygame.draw.rect(screen, colorJoinName, lobbies)
    pygame.draw.rect(screen, colorJoinName, refresh)
    

    joinLobby_Text = fontSubTitle.render('Join lobby', True, pygame.Color("white"))
    displayTxt(joinLobby_Text, 200, screen_width // 2)
    createLobby_Text = fontSubTitle.render('Create lobby', True, pygame.Color("white"))
    displayTxt(createLobby_Text, 156,  screen_width // 2)
    displayTxt(refreshText, 520, (screen_width // 2) + 150)
    #<=== End of join and create lobby buttons ===>#

    #<=== Display of lobbies ===>#
    i = 0
    for lob in Lobbies:
        name = fontSubTitle.render(lob, True, pygame.Color("white"))
        displayTxt(name, 300 + (i * 30), screen_width // 2)
        i = i + 1



    text_surface = base_font.render(name_text, True, (255, 255, 255)) 
    screen.blit(text_surface, (lobbyName.x+5, lobbyName.y+5)) 
    lobbyName.w = max(300, text_surface.get_width()+10) 

    text_surface = base_font.render(user_text, True, (255, 255, 255)) 
    screen.blit(text_surface, (lobbyUsers.x+5, lobbyUsers.y+5)) 
    lobbyUsers.w = max(30, text_surface.get_width()+10) 

    text_surface = base_font.render(joinName, True, (255, 255, 255)) 
    screen.blit(text_surface, (joinLobbyName.x+5, joinLobbyName.y+5)) 
    joinLobbyName.w = max(300, text_surface.get_width()+10) 

    pygame.display.flip() 
    clock.tick(60)
