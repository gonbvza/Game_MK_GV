import socket
import threading
import json
import time
import pygame

clientAddresses = {}
lobbies = {}
clientGameStates = {}

def playerAnimation(gameName, state, playerName, speedType):
        
        ballObj = clientGameStates[gameName]["ball"]

        clientYPositionMinus = clientGameStates[gameName][playerName][1] 
        clientYPositionPlus = clientGameStates[gameName][playerName][1] + 140

        clientXPosition = clientGameStates[gameName][playerName][0]

        if(clientGameStates[gameName]["leftPaddle"] == playerName):
            if((ballObj[0] <= clientXPosition)):
                if(ballObj[1] >= clientYPositionMinus and ballObj[1] <= clientYPositionPlus):
                    clientGameStates[gameName]["ballSpeedX"] *= -1
                    clientGameStates[gameName]["lastTouched"] = playerName

        elif(clientGameStates[gameName]["rightPaddle"] == playerName):
            if((ballObj[0] >= clientXPosition)):
                if(ballObj[1] >= clientYPositionMinus and ballObj[1] <= clientYPositionPlus):
                    clientGameStates[gameName]["ballSpeedX"] *= -1
                    clientGameStates[gameName]["lastTouched"] = playerName

        playerID = playerName
        playerDir = state[speedType]
        
        detuple = list(state[playerID])
        detuple[1] = detuple[1] + playerDir

        if detuple[1] <= 0:
            detuple[1] = 0
        
        elif detuple[1] >= (state["screenHeight"] - 140):
            detuple[1] = state["screenHeight"] - 140
        
        tuple(detuple)
        state[playerID] = detuple

def ballAnimation(gameName):
    if clientGameStates[gameName]["ball"][1] <= 0 or clientGameStates[gameName]["ball"][1] >= clientGameStates[gameName]["screenHeight"]:
        clientGameStates[gameName]["ballSpeedY"] *= -1
        
    elif clientGameStates[gameName]["ball"][0] <= 0 or clientGameStates[gameName]["ball"][0] >= clientGameStates[gameName]["screenWidth"]:
        clientGameStates[gameName]["ballSpeedX"] *= -1

    detuple = list(clientGameStates[gameName]["ball"])
    detuple[0] += clientGameStates[gameName]["ballSpeedX"]
    detuple[1] += clientGameStates[gameName]["ballSpeedY"]
    tuple(detuple)

    if(detuple[0] >= clientGameStates[gameName]["screenWidth"]):
        detuple[0] = clientGameStates[gameName]["screenWidth"] / 2
        detuple[1] = clientGameStates[gameName]["screenWidth"] / 2
        
        if(clientGameStates[gameName]["lastTouched"] != 0):
            clientGameStates[gameName]["scoreboard"][clientGameStates[gameName]["lastTouched"]] += 1

        clientGameStates[gameName]["lastTouched"] = 0
        clientGameStates[gameName]["ballSpeedX"] *= -1

    elif(detuple[0] <= 0):
        detuple[0] = clientGameStates[gameName]["screenWidth"] / 2
        detuple[1] = clientGameStates[gameName]["screenWidth"] / 2
        
        if(clientGameStates[gameName]["lastTouched"] != 0):
            clientGameStates[gameName]["scoreboard"][clientGameStates[gameName]["lastTouched"]] += 1
        
        clientGameStates[gameName]["lastTouched"] = 0
        clientGameStates[gameName]["ballSpeedX"] *= -1
        
    clientGameStates[gameName].update({"ball" : detuple})

def send(gameName, gameHostAddress, UDPServerSocket):

    while(True):
        jsonString = json.dumps(clientGameStates[gameName])

        for user in lobbies[gameName]:
            for key, value in clientAddresses.items():
                if value == user:
                    UDPServerSocket.sendto(("DATA " + jsonString).encode(), key)

        time.sleep(0.01)
        ballAnimation(gameName)
        for user in lobbies[gameName]:
            playerAnimation(gameName, clientGameStates[gameName], str(user), (str(user)+"Speed"))

def receive(gameName, gameHostAddress, UDPServerSocket):

    while(True):
        response, address = UDPServerSocket.recvfrom(1024)
        response = response.decode()
        splittedResponse = response.split()
        time.sleep(0.01)

        if("pygame.KEYDOWN " in response):
            clientGameStates[gameName][splittedResponse[1]] = int(splittedResponse[2])

def init(gameName, userAmount, gameHostAddress, UDPServerSocket):

    while(True):
        if(len(lobbies[gameName]) == int(userAmount)):

            state = {

                    "screenWidth" : 640,
                    "screenHeight" : 480,
                    "users" : userAmount,
                    "usernames" : lobbies[gameName],
                    "name" : gameName,
                    "ball" : (640/2, 480/2),
                    "lastTouched" : 0,
                    "leftPaddle" : str(lobbies[gameName][1]),
                    "rightPaddle" : str(lobbies[gameName][0]),
                    str(lobbies[gameName][0]) : (640- 20, 480/2 - 70),
                    str(lobbies[gameName][1]) :  (10, 640/2 - 70),
                    str(lobbies[gameName][0]) + "Speed" : 0,
                    str(lobbies[gameName][1]) + "Speed" : 0,
                    "ballSpeedX" : -4,
                    "ballSpeedY" : -2,
                    "scoreboard" : {str(lobbies[gameName][0]) : -1,
                                    str(lobbies[gameName][1]) : 0}
                }
            
            clientGameStates.update({gameName : state})

            for user in lobbies[gameName]:
                for key, value in clientAddresses.items():
                    if value == user:
                        UDPServerSocket.sendto(("GAME-START\n").encode(), key)

            receiving = threading.Thread(target = receive, args = (gameName, gameHostAddress, UDPServerSocket))
            receiving.start()
            
            sending = threading.Thread(target = send, args = (gameName, gameHostAddress, UDPServerSocket))
            sending.start()
            break
        
        else:
            pass

def main():
    global lobbies, clientAddresses
    
    UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    UDPServerSocket.bind(('192.168.1.231', 5378))
    try:
        while(True):
            clientData, clientAddress = UDPServerSocket.recvfrom(1024)
            clientData = clientData.decode()
            splittedData = clientData.split()

            if('HELLO-FROM' in clientData):
                if(splittedData[1] not in clientAddresses):
                    clientAddresses.update({clientAddress : splittedData[1]})
                    UDPServerSocket.sendto(('HELLO ' + splittedData[1] + '\n').encode(), clientAddress)

                else:
                    UDPServerSocket.sendto(('BAD-RQST-HDR\n').encode(), clientAddress)
    
            elif('LIST-LOBBY' in clientData):
                lobbiesNames = ''
                for lobby in lobbies:
                    lobbiesNames += lobby + " "

                UDPServerSocket.sendto(('LIST-LOBBY ' + lobbiesNames + '\n').encode(), clientAddress)
            
            elif('JOIN' in clientData):
                if(splittedData[1] in lobbies): 
                    lobbies[splittedData[1]].append(clientAddresses[clientAddress])
                    UDPServerSocket.sendto(('JOIN-OK\n').encode(), clientAddress)

                else:
                    UDPServerSocket.sendto(('BAD-JOIN-RQST\n').encode(), clientAddress)

            elif('CREATE-LOBBY' in clientData):
                UDPServerSocket.sendto(('CREATE-OK\n').encode(), clientAddress)

                lobbies.update({splittedData[1] : [clientAddresses[clientAddress]]})

                gameThread = threading.Thread(target = init, args = (splittedData[1], splittedData[2], clientAddress, UDPServerSocket))
                gameThread.start()
                
            else:
                pass
    except KeyboardInterrupt:
        pass
main()
exit()

