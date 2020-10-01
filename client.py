import socket
import time
import select
import sys
s = socket.socket()
host = "localhost"
print("Enter port number of the server to join the game:")
port = input()                                                              # Takes the port number as the input.

s.connect((host, int(port)))                                                # Connects  the client to the server

# To Receive and print instructions.
instruction=s.recv(1024)
print (instruction)

question=s.recv(1024)                                                        # Recieves and prints the question.
print(question)

q=0                                                                          # Index of the question number. 

buzzerinfo=s.recv(1024)                                                      # Recieves and prints the inc=formation about buzzer. Whether, you pressed buzzer first or someone else did.
print(buzzerinfo)

while (q<20):                                                                # Runs the while loop till the number of questions present in the list.
    data1 = s.recv(1024)                                                     
    if data1==".":                                                           # If . is recieved, it implies some player has reached the score of 5 or above. So this breaks the loop.
        break
    print(data1)                                                             # Else, the next question is printed.
    c,c1,c2=select.select([sys.stdin,s],[],[],20)                            # This is the syntax for buzzer.
    if len(c)>0:
        if c[0] == sys.stdin:
            y=raw_input()                                                    # Taking any key as input for buzzer.
            s.sendall(str(y))                                                # Sends the information that buzzer has been pressed.
        else:
            d=c[0].recv(1024)                                                
            print (d)
            q=q+1
            continue;
    data2=s.recv(1024)                                                       # This is recieved if you pressed the buzzer first.
    print (data2)                                                            # Asks us to answer the question.
    if data2=='Okay, Your Answer is: ':
        ans=raw_input()                                                      # Takes answer as input.
        time.sleep(1)
        s.sendall(str(ans))                                                  # Sends the answer.
        q=q+1
        result=s.recv(1024)                                                  # This is the response of the answer. Whether it is right or wrong.
        print(result)
    
data3=s.recv(1024)                                                           # This comes at the end when the winner is declared.
print(data3)





    
