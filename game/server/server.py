import socket
import threading
import config


def createGameLobby():
    print("Lobby created.")

def main():

    UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    UDPServerSocket.bind(('127.0.0.1', 5378))
    
    while(True):
        clientData, clientAddress =  UDPServerSocket.recvfrom(1024)
        clientData = clientData.decode()

        print("Message received: " + clientData.strip())
        splittedData = clientData.split()

        if('HELLO-FROM' in clientData):
            if(splittedData[1] not in config.clientAddresses):
                config.clientAddresses.update({splittedData[1]: clientAddress})
                UDPServerSocket.sendto(('HELLO ' + splittedData[1] + '\n').encode(), clientAddress)

                print("Login successful.")

            else:
                UDPServerSocket.sendto('BAD-RQST-HDR\n', clientAddress)

                print("Login unsuccessful.")
            
        elif('LIST-LOBBY\n' in clientData):
            lobbies = ''
            for lobby in config.lobbies:
                lobbies += lobby + " "
            
            UDPServerSocket.sendto('LIST-LOBBY ' + lobbies + '\n', clientAddress)
                
        elif('JOIN' in clientData):
            if(splittedData[1] in config.lobbies):
                config.lobbies.update({splittedData[1].append(clientAddress)})
                UDPServerSocket.sendto(('JOIN-OK\n').encode(), clientAddress)

                print("Joined lobby.")

            else:
                UDPServerSocket.sendto(('BAD-JOIN-RQST\n').encode(), clientAddress)

                print("Lobby doesn't exist.")

        elif('CREATE-LOBBY' in clientData):
            UDPServerSocket.sendto(('CREATE-OK\n').encode(), clientAddress)
                
            clientThread = threading.Thread(target = createGameLobby, args = ())
            clientThread.start()
            
        else:
            pass     

main()
exit()

