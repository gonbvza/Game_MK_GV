def loginUser():
    # 1. Send the server a HELLO-FROM message
    # 2. Wait for server response HELLO + username
    # 3. If you receive postivie response - open the main menu (lobby create and join)
    # 4. If you do not receive receive response: 
    #        - resend the HELLO-FROM if resposne completely lost
    #        - if username taken change username and send again
    #        - agree on protocol for this part (who sends what messages in case of errors)
    return

def mainMenu():
    # 1. this function is called when a succesfull login happens
    # 2. presents the user with option to join the game or create a game (lobby), this function calls two functions
    #       -lobbyJoin()
    #       -lobbyHost()
    # 3. doesn't communicate with the server - doesn't send anything yet
    return

def lobbyJoin():
    # 1. send a message to the server LIST-LOBBY\n, the packet conatains
    # 2. wait for a response with LIST-LOBBY Name1, Name2, Name3 .... \n
    # 3. lists all the avalible lobbies
    # 4. checks for user input which lobby to join
    # 5. send a JOIN Name1\n to the server
    # 6. wait for JOIN-OK
    # 7. if JOIN-OK back then call waiting screen
    
    return

def lobbyHost():
    # 1. send a message to server CREATE-LOBBY <name>, <users>\n
    # 2. wait for CREATE-OK\n response
    # 3. if response is positive - call waiting screen
    # 4. check for error messages (lobby already exists, name already taken, too many players)
    return

def waitScreen():
    # 1. Listen for how many users are there in the lobby LOBBY-LIST + Name1,Name2 ... \n
    # 2. wait for GAME-START\n signal
    # 3. if GAME-START <paddleName>\n received call game depending on the users
    # 4. change screen
    return 

def playGame():
    # 1. calls all the other functions necessary in correct order
    # 2. send the current reqeust to move UPWARDS <name>\n DOWNWARDS <name>\n etc. 
    # 3. wait for the response with the new velocity the new direction + BALL POSITION
    # 4. update screen 
    # 5. repeat
    return

def sendSpeed():
    # 1. send the current paddle speed to the server (new)
    return

def receiveSpeed():
    # 1. wait for server response on WHAT ARE THE CURRENT POSITIONS OF OTHER PADDLES
    # 2. update their positions on your screen
    return