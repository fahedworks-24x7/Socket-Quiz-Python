import socket
import sys
import time
import select

Questions=["1. Which city is situated on two continents?","2. Which continent is most populous?","3. Which country is the second biggest in the world?","4. Which country in the European Union has the biggest population?","5. Which is the largest capital city in the world (by population)?","6. Which country in Asia has the most volcano?","7. What country calls itself Nippon?","8. Where is the Tonle Sap located?","9. Which large river flows through London?","10. How many time zones does India span?","11. What is the capital of Thailand?","12. Rabat is the capital of?", "13. What is the hottest continent?","14. Which state in USA was once called Deseret?","15. What is the main tributary of the Ganges River in India?","16. Which country has 4 letters, with 'q' at the end?","17. Which river flows through Glasgow?","18. Which continent has Mt. Kilimanjaro?","19. Which country is called the Land Of Rising Sun?","20. Which state is IIITB located?"]
Answers=["ISTANBUL","ASIA","CANADA","GERMANY","TOKYO","INDONESIA","JAPAN","CAMBODIA","THAMES","TWO", "BANGKOK","MOROCCO","AFRICA","UTAH","YAMUNA","IRAQ","CLYDE","AFRICA","JAPAN","KARNATAKA"]

Score=[0,0,0]                                                # This list notes down the scores of the three players.
response=[]                                                  # This list is to deal with the buzzer.
ConnectionsList = []                                         # This list takes all the connections that have been made.
AddressList = []                                             # This list consists the addresses of the clients joined.

# Function for creating a socket.
def CreateSocket():
    try:
        global host
        global port
        global s
        host ="localhost" 
        print("Enter a Port Number: ") 
        port = input()                                        # Takes the port number as input.
        s = socket.socket()

    except socket.error as msg:
        print("Socket creation error: " + str(msg))

# Function for binding the socket with clients.
def BindSocket():
    try:
        global host
        global port
        global s
        s.bind((host, int(port)))                              # Binds the host to the server.
        s.listen(5)
        print("Server bound to " + str(port))                  # Assures that the connection is made.
        print("Waiting for the players to join...")
        
    except socket.error as msg:
        print("Socket Binding error" + str(msg) + "\n" + "Retrying...")

# Function for accepting connections and giving the introduction. 
def AcceptConnections():
    for c in ConnectionsList:
        c.close()

    del ConnectionsList[:]
    del AddressList[:]
    j=0
    while True:
            connection, address = s.accept()
            s.setblocking(1)                                       # Prevents timeout
            j=j+1
            ConnectionsList.append(connection)
            AddressList.append(address)
            if j<3:
                print("Player " + str(j)+" has joined the game at address " + address[0])
                connection.send(str.encode("\t\t\t\tWelcome to \n\t\t\t   KAUN BANEGA LAKHPATI!"))
                time.sleep(1)
                connection.send(str.encode("\t\t\t\t\b\bYou are Player "+ str(j)))
                time.sleep(1)
                connection.send(str.encode("There are some simple rules. A question will be displayed on your screen. You need to ring the buzzer to answer the question. Press any key to ring the buzzer. And you have 20 seconds time to ring the buzzer. Once you rang the buzzer, you will be awarded 1 point if your answer is right. And 0.5 will be deducted for each wrong answer. 0 points, otherwise. The first player to reach a score of 5 will win the LAKHPATI Title!!! Best of 'Lakh'!!"))

            else:
                print("Player " + str(j)+" has joined the game at address " + address[0])
                connection.send(str.encode("\t\t\t\tWelcome to \n\t\t\t   KAUN BANEGA LAKHPATI!"))
                print("3 Players have joined. Game In PROGRESS...")
                time.sleep(1)
                connection.send(str.encode("\t\t\t\t\b\bYou are Player "+ str(j)))
                time.sleep(1)
                connection.send(str.encode("There are some simple rules. A question will be displayed on your screen. You need to ring the buzzer to answer the question. Press any key to ring the buzzer. And you have 10 seconds time to ring the buzzer. Once you rang the buzzer, you will be awarded 1 point if your answer is right. And 0.5 will be deducted for each wrong answer. 0 points, otherwise. The first player to reach a score of 5 will win the LAKHPATI Title!!! Best of 'Lakh'!!"))
                thread_function()
                break;

# Function for asking questions and evaluating scores.
# Thread indicates that the following function happens simultaneously for all the clients.                
def thread_function():
    for i in range(len(Questions)):
        for connection in ConnectionsList:
            time.sleep(0.1)
            connection.send(str.encode("\n"+Questions[i]+"\nPress any key and Enter to answer this question. Your 10 seconds starts now..."))
        response1=select.select(ConnectionsList,[],[],10)                              # Waiting for the buzzer to be pressed.
        if(len(response1[0])>0):
            
            ParticularConnection = response1[0][0];                                    # ParticularConnection is the one which pressed the buzzer.
            b = ParticularConnection.recv(1024)
            response1=()
            for connection in ConnectionsList:
                if connection!=ParticularConnection:
                    connection.send(str.encode("Oops, Player "+str(ConnectionsList.index(ParticularConnection)+1)+ " has pressed the buzzer.\nYour score remains same. Better Luck Next Time."))
            for p in range(len(ConnectionsList)):
                    if ConnectionsList[p]==ParticularConnection:
                        t=p;
	
            if b:
                        ParticularConnection.send(str.encode("Okay, Your Answer is: "))
                        answer=(ParticularConnection.recv(1024))
                        if str(answer)==str(Answers[i]):
                            Score[t]=Score[t]+1
                            ParticularConnection.send(str.encode("Correct Answer, You get 1 Point.\nYour score is "+str(Score[t])))
                            if Score[t]>=5:
                                for c in ConnectionsList:
                                    c.send(str.encode("."))
                                    time.sleep(1)
                                break
                        else:
                            Score[t]=Score[t]-0.5
                            ParticularConnection.send(str.encode("Wrong Answer, You lose 0.5 Points.\nYour score is "+str(Score[t])))
                            time.sleep(1)
        elif (len(response1[0])==0):
            	for c in ConnectionsList:
             	   c.send(str.encode("Time's Up! Nobody pressed the buzzer.\nYour score remains the same.\nMoving on to the next question..."))

# Main function to call the other required functions and declare the winner.
def main():
    CreateSocket()
    BindSocket()
    AcceptConnections()
    s=0
    w=0
    for i in range(len(ConnectionsList)):
        if Score[i]>s:
            w=i                                              # w is the Index of the winning player.
            s=Score[i]                                       # s is the Score of the winning player.
    for c in ConnectionsList:
        if ConnectionsList.index(c)==w:
             c.send(str.encode("\nCongratulations! You scored " + str(s)+" Points. YOU WON THE GAME!!!" ))
        else:
             c.send(str.encode("\nPlayer " + str(w+1)+" has scored "+str(s)+" Points. YOU LOSE" )) 
    time.sleep(2)
    print("\n---GAME OVER---")
    print("Player "+str(w+1)+" has won the game.") 
    print("The scores are:")
    print("Player 1: "+str(Score[0]))
    print("Player 2: "+str(Score[1]))
    print("Player 3: "+str(Score[2]))     

main()

