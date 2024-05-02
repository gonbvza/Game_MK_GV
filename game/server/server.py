import socket
import threading
import time

#currently logged in clients in format {IPClientSocket : fancyUsername}
clientAddresses = {}
#currrent lobbies hosted in format {lobbyName : ['player1':, 'player2', ...]} (a dictionary of lists)
lobbies = {}

#specific lobby thread
def createGameLobby(gameName, userAmount, gameHostAddress, UDPServerSocket):
    
    while(True):
        time.sleep(1)
        if(len(lobbies[gameName]) == userAmount):
            UDPServerSocket.sendto(("GAME-START\n").encode(), gameHostAddress)
            break
        #wait untill all players join
        else:
            pass
    
    #initialize scoreboard in foramt {'playerName': 0}
    scoreboard = {}
    for player in lobbies[gameName]:
        scoreboard.update({lobbies[gameName][player] : 0})
    
    screenSize = ['1280', '960']

    #intialize ball in the middle of the screen
    ballCoordinates = ['640', '480']
    

    #game loop
    while(True):
        pass


#main thread
def main():
    global lobbies, clientAddresses

    UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    UDPServerSocket.bind(('127.0.0.1', 5378))
    
    #handshake loop
    while(True):
        clientData, clientAddress =  UDPServerSocket.recvfrom(1024)
        clientData = clientData.decode()

        print("Message received: " + clientData.strip())
        splittedData = clientData.split()
        
        #login user for the first time
        if('HELLO-FROM' in clientData):
            if(splittedData[1] not in clientAddresses):
                clientAddresses.update({clientAddress : splittedData[1]})
                UDPServerSocket.sendto(('HELLO ' + splittedData[1] + '\n').encode(), clientAddress)

                print("Login successful.")

            else:
                UDPServerSocket.sendto(('BAD-RQST-HDR\n').encode(), clientAddress)

                print("Login unsuccessful.")

        #list all current lobbies    
        elif('LIST-LOBBY' in clientData):
            lobbiesNames = ''
            for lobby in lobbies:
                lobbiesNames += lobby + " "

            UDPServerSocket.sendto(('LIST-LOBBY ' + lobbiesNames + '\n').encode(), clientAddress)
            print(lobbies)
        
        #join lobby functionality
        elif('JOIN' in clientData):
            if(splittedData[1] in lobbies):
                lobbies[splittedData[1]].append([clientAddresses[clientAddress]])
                UDPServerSocket.sendto(('JOIN-OK\n').encode(), clientAddress)

                print("Joined lobby.")

            else:
                UDPServerSocket.sendto(('BAD-JOIN-RQST\n').encode(), clientAddress)

                print("Lobby doesn't exist.")

        #create a lobby, update the parameters in the dictionary of lists
        elif('CREATE-LOBBY' in clientData):
            UDPServerSocket.sendto(('CREATE-OK\n').encode(), clientAddress)
            
            print("Lobby created.")

            lobbies.update({splittedData[1] : [clientAddresses[clientAddress]]})

            #create a game specific thread
            #clientThread = threading.Thread(target = createGameLobby, args = (splittedData[1], splittedData[2][:-1], clientAddress, UDPServerSocket))
            #clientThread.start()
            
        else:
            pass     

main()
exit()

