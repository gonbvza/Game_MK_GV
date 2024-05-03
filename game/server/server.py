import socket
import threading
import time

clientAddresses = {}
lobbies = {}

def ballAnimation(state, UDPServerSocket, gameHostAddress):

    if state["ball"][1] <= 0 or state["ball"][1] >= state["screenHeight"]:
        state["ballSpeedY"] *= -1
    
    elif state["ball"][0] <= 0 or state["ball"][0] >= state["screenWidth"]:
        state["ballSpeedX"] *= -1

    detuple = list(state["ball"])
    detuple[0] += state["ballSpeedX"]
    detuple[1] += state["ballSpeedY"]
    tuple(detuple)

    state["ball"] = detuple

    UDPServerSocket.sendto(("BALL-POSITION " + str(state["ball"][0]) + " " + str(state["ball"][1])).encode(), gameHostAddress)
    

def gameState(state, scoreboard, gameName, userAmount, gameHostAddress, UDPServerSocket):

    while(True):
        response, address = UDPServerSocket.recvfrom(1024)
        response = response.decode()
        
        if("-1" in response):
            state["ballSpeedX"] *= -1

        elif("GET-BALL-POS" in response):
            ballAnimation(state, UDPServerSocket, gameHostAddress)

def createGameLobby(gameName, userAmount, gameHostAddress, UDPServerSocket):

    state = {

            "screenWidth" : 1280,
            "screenHeight" : 960,
            "ball" : (1280/2 - 15, 960/2 - 15),
            "opponent" : (1280 - 20, 960/2 - 70),
            "player" :  (10, 960/2 - 70),
            "playerSpeed" : 0,
            "opponentSpeed" : 0,
            "ballSpeedX" : -4,
            "ballSpeedY" : -2,

        }
    
    if(userAmount):
        UDPServerSocket.sendto(("GAME-START\n").encode(), gameHostAddress)
    
    scoreboard = {}
    for player in lobbies[gameName]:
        scoreboard.update({player : 0})
    
    parameters = "width: " + str(state["screenWidth"]) + " "
    parameters += "height: " + str(state["screenHeight"]) + " "
    parameters += "ball: " + str(state["ball"][0]) + " " + str(state["ball"][1]) + " "
    parameters += "opponent: " + str(state["opponent"][0]) + " " + str(state["opponent"][1]) + " "
    parameters += "player: " + str(state["player"][0]) + " " + str(state["player"][1])
    parameters += "\n"
    
    UDPServerSocket.sendto(("SETUP " + parameters).encode(), gameHostAddress)

    UDPServerSocket.sendto(("SCORE " + " " + str(0) + " " + str(0)).encode(), gameHostAddress)

    velocities =  "player: " + str(state["playerSpeed"]) + " "
    velocities += "opponent: " + str(state["opponentSpeed"]) + " "
    velocities += "ball: " + str(state["ballSpeedX"]) + " " + str(state["ballSpeedY"]) + " "
    velocities += "\n"

    UDPServerSocket.sendto(("VELOCITY " + velocities).encode(), gameHostAddress)

    gameState(state, scoreboard, gameName, userAmount, gameHostAddress, UDPServerSocket)

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

                clientThread = threading.Thread(target = createGameLobby, args = (splittedData[1], splittedData[2], clientAddress, UDPServerSocket))
                clientThread.start()
                
            else:
                pass
    except KeyboardInterrupt:
        pass
main()
exit()

