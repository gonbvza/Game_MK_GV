import pygame 
import sys 
import socket
import threading
import json
import time
import random

#<=== Server properties ===>#
PORT = 10300
SERVER = '84.125.157.181'
ADDR = (SERVER, PORT)
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
FORMAT = 'utf-8'
Lobbies = []
gameStart = False
username = ''
internalGameState = {}
dropPackets = False
#<=== End server properties ===>#

pygame.init() 

clock = pygame.time.Clock() 
#<=== Helper functions ===>#
def startMatch():
    global gameStart
    data = client.recv(4096)
    received = data.decode(FORMAT)
    splitted = received.split()
    print(received)

    if splitted[0] == "GAME-START":
        gameStart = True

def sendLoginUser(ms):
    msg_to_send = f"HELLO-FROM {ms}"
    string_bytes = msg_to_send.encode("utf-8")
    client.sendto(string_bytes, ADDR)

def openGame():
    print("Receiving")
    data = client.recv(4096)
    received = data.decode(FORMAT)
    splitted = received.split()
    
    print("Received " + received)
    if splitted[0] == "HELLO":
        return True

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

def receive(clientSocket):
    global internalGameState,dropPackets
    while(True):

        response, address = clientSocket.recvfrom(1024)
        response = response.decode()

        if dropPackets:
            randNum = random.randint(1, 5)
            
            if randNum == 1:
                userA = internalGameState["userA"]
                userB = internalGameState["userB"]
                userASpeed = internalGameState[userA+"Speed"]
                userBSpeed = internalGameState[userB+"Speed"]

                detuple = list(internalGameState[userA])
                detuple[1] = detuple[1] + userASpeed
                tuple(detuple)
                internalGameState[userA] = detuple

                detuple = list(internalGameState[userB])
                detuple[1] = detuple[1] + userBSpeed
                tuple(detuple)
                internalGameState[userB] = detuple

                detuple = list(internalGameState["ball"])
                detuple[0] += internalGameState["ballSpeedX"]
                detuple[1] += internalGameState["ballSpeedY"]
                tuple(detuple)
                internalGameState.update({"ball" : detuple})
            else:
                if("DATA" in response):
                    response = response.replace("DATA ", "")
                    internalGameState = json.loads(response)
                else:
                    pass
        else:
            if("DATA" in response):
                    response = response.replace("DATA ", "")
                    internalGameState = json.loads(response)
            else:
                pass
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


active = False

base_font = pygame.font.Font(None, 32) 
user_text = ''
name_text = ''
joinName = ''
user_num = ''
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
hacker = pygame.font.Font('freesansbold.ttf', 70)
#<=== End of Titles properties ===>#


endLoop = False
while True: 

    screen.fill(bg_color) 
    #<=== Render the main title and subtitle ===>#
    text = fontTitle.render('Welcome to Pong', True, pygame.Color("white"))
    textSub = fontSubTitle.render('Please login:', True, pygame.Color("white"))
    displayTxt(text, 40,screen_width / 2)
    displayTxt(textSub, 90,screen_width / 2)
    #<=== End of rendering the main title and subtitle ===>#

    for event in pygame.event.get(): 

        if event.type == pygame.QUIT: 
            pygame.quit() 
            sys.exit() 

        if event.type == pygame.MOUSEBUTTONDOWN: 
            if input_rect.collidepoint(event.pos): 
                active = True
            elif finish_rect.collidepoint(event.pos): 
                user_text = user_text[:]
                print(user_text)
                username = user_text
                sendLoginUser(user_text)
                endLoop = openGame()
                
            else:
                active = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                user_text = user_text[:]
                print(user_text)
                username = user_text
                sendLoginUser(user_text)
                endLoop = openGame()
            elif active:
                if event.key == pygame.K_RETURN:
                    print(user_text)  # Here you can do whatever you want with the text
                    user_text = ''
                elif event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                elif len(user_text) < 4:
                    user_text += event.unicode

    if active: 
        color = color_active 
    else: 
        color = color_passive 
        
    pygame.draw.rect(screen, color2, finish_rect) 
    pygame.draw.rect(screen, border_color, input_rect, 2)  
    pygame.draw.rect(screen, color, input_rect)
    
    text_surface = base_font.render(user_text, True, (255, 255, 255)) 
    screen.blit(text_surface, (input_rect.x+5, input_rect.y+5)) 
    input_rect.w = max(100, text_surface.get_width()+10) 
    
    if endLoop:
        break

    pygame.display.flip() 
    clock.tick(60)

listRefresh()

endSecondLoop = False

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
                activeUser = False
                activeJoinName = False
            elif lobbyUsers.collidepoint(event.pos): 
                activeUser = True
                activeName = False 
                activeJoinName = False
            elif joinLobbyName.collidepoint(event.pos):
                activeJoinName = True
                activeName = False 
                activeUser = False

            elif refresh.collidepoint(event.pos):
                listRefresh()
            elif createLobby_rect.collidepoint(event.pos): 
                name_text = name_text[:]
                print(name_text)
                print(user_num)
        
                sendLobby(name_text,user_num)
                
                data = client.recv(4096)
                received = data.decode(FORMAT)
                splitted = received.split()
                print(received)

                if splitted[0] == "CREATE-OK" or splitted[0] == "JOIN-OK":
                    endSecondLoop = True

            elif joinLobby_rect.collidepoint(event.pos): 
                print(joinName)
                if joinName == '':
                    print("Something empty")
                else:
                    sendLogin(joinName)
                    data = client.recv(4096)
                    received = data.decode(FORMAT)
                    splitted = received.split()
                    print(received)

                    if splitted[0] == "CREATE-OK" or splitted[0] == "JOIN-OK":
                        endSecondLoop = True

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
                    user_num = user_num[:-1]
                elif len(user_num) < 1:
                    if event.unicode.isdigit():
                        user_number = int(event.unicode)
                        if 1 < user_number <= 4:
                            user_num += event.unicode
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
    else:
        colorInputName = color_passive 
    if activeUser:
        colorInputUser = color_active
    else:
        colorInputUser = color_passive 

    if activeJoinName:
        colorJoinName = color_active
    else: 
        colorJoinName = color_passive

    #<=== Join and create lobby buttons ===>#
    pygame.draw.rect(screen, color_passive, createLobby_rect)
    pygame.draw.rect(screen, color_passive, joinLobby_rect)
    pygame.draw.rect(screen, colorInputName, lobbyName)
    pygame.draw.rect(screen, colorInputUser, lobbyUsers)
    pygame.draw.rect(screen, colorJoinName, joinLobbyName)
    pygame.draw.rect(screen, color_passive, lobbies)
    pygame.draw.rect(screen, color_passive, refresh)
    

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

    text_surface = base_font.render(user_num, True, (255, 255, 255)) 
    screen.blit(text_surface, (lobbyUsers.x+5, lobbyUsers.y+5)) 
    lobbyUsers.w = max(30, text_surface.get_width()+10) 

    text_surface = base_font.render(joinName, True, (255, 255, 255)) 
    screen.blit(text_surface, (joinLobbyName.x+5, joinLobbyName.y+5)) 
    joinLobbyName.w = max(300, text_surface.get_width()+10) 

    if endSecondLoop:
        break

    pygame.display.flip() 
    clock.tick(60)

gameThread = threading.Thread(target = startMatch, args = ())
gameThread.start()

while True: 

    screen.fill(bg_color) 
    #<=== Render the main title and subtitle ===>#
    text = fontTitle.render('Please wait while other players connect', True, pygame.Color("white"))
    displayTxt(text, screen_height / 2,screen_width/2)
    #<=== End of rendering the main title and subtitle ===>#
    
    for event in pygame.event.get():

        if event.type == pygame.QUIT: 
            pygame.quit() 
            sys.exit()

    if gameStart:
        break


    pygame.display.flip() 
    clock.tick(60)


receiving = threading.Thread(target = receive, args = (client, ))
receiving.start()

time.sleep(1)

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
                client.sendto(("pygame.KEYDOWN " + username + "Speed" + " " + str(4)).encode(), (SERVER, 5378))
                
            if event.key == pygame.K_w:
                client.sendto(("pygame.KEYDOWN " + username + "Speed" + " " + str(-4)).encode(), (SERVER, 5378))
        
            if event.key == pygame.K_h:
                print("Key is actively pressed")
                client.sendto(("pygame.KEYDOWN " + username + "Speed" + " " + str(6)).encode(), (SERVER, 5378))
                client.sendto(("pygame.KEYDOWN " + username + "Speed" + " " + str(6)).encode(), (SERVER, 5378))

            if event.key == pygame.K_y:
                print("Key is actively pressed")
                client.sendto(("pygame.KEYDOWN " + username + "Speed" + " " + str(-6)).encode(), (SERVER, 5378))
                client.sendto(("pygame.KEYDOWN " + username + "Speed" + " " + str(-6)).encode(), (SERVER, 5378))

            if event.key == pygame.K_l:
                dropPackets = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_s:
                print("Key is actively pressed")
                client.sendto(("pygame.KEYDOWN " + username + "Speed" + " " + str(4)).encode(), (SERVER, 5378))
                       
            if event.key == pygame.K_w:
                client.sendto(("pygame.KEYDOWN " + username + "Speed" + " " + str(-4)).encode(), (SERVER, 5378))

            if event.key == pygame.K_l:
                dropPackets = False

        
    if internalGameState["hackerDetected"] == True:
        break
    
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

while True: 

    screen.fill(bg_color) 

    text = fontTitle.render("HACKER!!!", True, pygame.Color("white"))
    displayTxt(text, screen_height / 2,screen_width/2)

    
    for event in pygame.event.get():

        if event.type == pygame.QUIT: 
            pygame.quit() 
            sys.exit()



    pygame.display.flip() 
    clock.tick(60)