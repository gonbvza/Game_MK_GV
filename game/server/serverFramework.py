def checkForUserLogin():
    # 1. check for handshake message before client starts to communicate
    # 2. if the client is not in the dictionary and the message is HELLO-FROM - login the client
    # 3. if there are any errros - send appropriate protocol message
    return

def retrieveLobbies():
    # 1. if the message header is LIST-LOBBY\n then send back a LIST-LOBBY + all the lobbies in the dictionary
    return

def userJoins():
    # 2. if the message header is JOIN this function executes
    # 3. check if lobby exists
    # 4. if lobby exists and there is free space - join the lobby
    # 5. send back JOIN-OK\n message
    return

def createHostLobby():
    # 1. if the message is CREATE-LOBBY create a new lobby
    # 2. send back if lobby created successfully
    # 3. set the lobby parameters - users, names
    # 4. put the creator of the lobby into the users in the lobby
    # 5. send back JOIN-OK\n 
    # 6. create a thread for a lobby
    return


def checkIfGameStart():
    # 1. send every 2 seconds or 1 second how many users are currently in the lobby 
    # 2. assign each paddle to each client randomly
    # 3. create a new thread for each paddle
    # 4. if the number of current players is the number specified in the lobby parametrs - send GAME-START <paddleName> \n
    # 5. create a thread for the game
    return

def playGame():
    # 1. send the ball coordinate and x-y velocity
    # 2. send the scoreboard at the moment (at all times)
    # 3. wait for the speed from each paddle
    # 4. check if any client send that he touched the ball 
    # 5. if all clients send that the ball is out of the screen - check which side of the screen it left and assign the proper score to scoreboard
    # 6. wait for BALL-POSITION <clietnName> <wallTouched>\n
    return

def updateSpeed():
    # 1. listen for message UPWARDS <paddleName>\n
    # 2. if message recevied - change the speed in the dictionary (position) 
    # 3. send the updated speed to ALL OTHER PADDLES
    # 4. calculate the ball position
    # 5. send the BALL position
    return