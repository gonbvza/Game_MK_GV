import socket
import threading
import json
import time
import pygame

clientAddresses = {}
lobbies = {}
clientGameStates = {}

def playerAnimation(state,  playerName, speedType):
        playerID = playerName
        playerDir = state[speedType]
        
        print(playerDir)

        detuple = list(state[playerID])
        detuple[1] = detuple[1] + playerDir

        if detuple[1] <= 0:
            detuple[1] = 0
        
        elif detuple[1] >= state["screenHeight"]:
            detuple[1] = state["screenHeight"]
        
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

    elif(detuple[0] <= 0):
        detuple[0] = clientGameStates[gameName]["screenWidth"] / 2
        detuple[1] = clientGameStates[gameName]["screenWidth"] / 2

    if(detuple[1] == clientGameStates[gameName]["player"][1]):
        clientGameStates[gameName]["ballSpeedX"] *= -1

    clientGameStates[gameName].update({"ball" : detuple})

def send(gameName, gameHostAddress, UDPServerSocket):

    while(True):
        jsonString = json.dumps(clientGameStates[gameName])

        UDPServerSocket.sendto(("DATA " + jsonString).encode(), gameHostAddress)

        time.sleep(0.01)
        ballAnimation(gameName)

        playerAnimation(clientGameStates[gameName], "player", "playerSpeed")
        
def receive(gameName, gameHostAddress, UDPServerSocket):

    while(True):
        response, address = UDPServerSocket.recvfrom(1024)
        response = response.decode()
        splittedResponse = response.split()
        time.sleep(0.01)

        if("pygame.KEYDOWN " in response):
                
            clientGameStates[gameName][splittedResponse[1]] = int(splittedResponse[2])
            
            print(clientGameStates[gameName][splittedResponse[1]])

def init(gameName, userAmount, gameHostAddress, UDPServerSocket):

    state = {

            "screenWidth" : 1280,
            "screenHeight" : 960,
            "users" : userAmount,
            "name" : gameName,
            "ball" : (1280/2 - 15, 960/2 - 15),
            "opponent" : (1280 - 20, 960/2 - 70),
            "player" :  (10, 960/2 - 70),
            "playerSpeed" : 0,
            "opponentSpeed" : 0,
            "ballSpeedX" : -4,
            "ballSpeedY" : -2,
            "socreboard" : {"player" : 0, "opponent" : 0}
        }
    
    
    
    clientGameStates.update({gameName : state})

    receiving = threading.Thread(target = receive, args = (gameName, gameHostAddress, UDPServerSocket))
    receiving.start()
    
    sending = threading.Thread(target = send, args = (gameName, gameHostAddress, UDPServerSocket))
    sending.start()

def main():
    global lobbies, clientAddresses
    
    UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    UDPServerSocket.bind(('127.0.0.1', 5378))
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

