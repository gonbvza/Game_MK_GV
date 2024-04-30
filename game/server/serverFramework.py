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