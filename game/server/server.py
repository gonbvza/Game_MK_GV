import socket
import threading
import config

def player(clientAddress, UDPServerSocket):
    
    while(True):
        clientData, clientAddress =  UDPServerSocket.recvfrom(1024)
        clientData.decode()

        while(clientData and clientAddress):
            if('SEND-SPEED' in clientData):
                
                clientData.strip()
                clientData.split()

                UDPServerSocket.sendto('SPEED-OK ' + clientData[0] + clientData[2] + '\n', clientAddress)
            else:
                pass

def main():

    UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    UDPServerSocket.bind(('127.0.0.1', 5378))
    
    while(True):
        clientData, clientAddress =  UDPServerSocket.recvfrom(1024)
        clientData = clientData.decode("utf-8")


        if(clientAddress[0] not in config.clientAddresses):
            if('HELLO-FROM' in clientData):
                
                clientData.strip()
                clientData.split()

                config.clientAddresses.update({clientData[1] : clientAddress})

                UDPServerSocket.sendto(('HELLO ' + clientData[1] + '\n').encode("utf-8"), clientAddress)

                clientThread = threading.Thread(target = player, args = (clientAddress, UDPServerSocket))
                clientThread.start()
            else:
                UDPServerSocket.sendto('BAD-RQST-HDR\n', clientAddress)
            
main()
exit()

