#Zelarous & Group

import socket
import os

s = socket.socket() #create scocket
s.connect((socket.gethostname(), 5000))

message = "r"

not_logged_in = "True"

def login():
    data = s.recv(1024)
    if data.decode() == "ACCESS TO SERVER GRANTED":
        global not_logged_in
        not_logged_in = "False"
        return
    print(data.decode())
    #Error check to ensure something is entered
    while True :
        try:
            message =input(": ").strip()
            if not message:
                raise SyntaxError
            else:
                break
        except SyntaxError:
            print("Enter a command")
    #Send the entered command
    s.send(message.encode())

#The client side of the command
def get():
    #Get the name of the file
    name = " "
    while True :
        try:
            name =input("Enter File Name: ").strip()
            if not name:
                raise SyntaxError
            else:
                break
        except SyntaxError:
            print("Enter file name")
    #Ask the server if the file exists
    s.send(name.encode())
    confirm = s.recv(1024)
    if confirm.decode() == "I HAVE THE FILE":
        #Create the file to place data into
        f = open(name, 'wb')
        #Begin recieving the pieces
        l = s.recv(1024)
        while l:
            f.write(l)
            s.send("Recieved data".encode())
            l = s.recv(1024)
            #Check if the final piece has been sent
            try:
                if l.decode()== "Your download has finished.":
                    l = ""
            except UnicodeDecodeError:
                pass
        #Close the file
        f.close()
        print(l)
    else:
        print("That file does not exist on the server")

def put():
    #Get the name of the file
    name = " "
    while True :
        try:
            name =input("Enter File Name: ").strip()
            if not name:
                raise SyntaxError
            else:
                break
        except SyntaxError:
            print("Enter file name")
    #Check the file to send
    try:
        file = open(name, 'rb')
        #Send the name to the server
        s.send(name.encode())
        #Begin seperating the file into pieces to send
        piece = file.read(1024)
        while piece :
            s.send(piece)
            s.recv(1024)
            piece = file.read(1024)
        #Send a confirmation and close the file
        s.send("Your download has finished.".encode())
        file.close()
    except FileNotFoundError:
        print("That file does not exist.")
        s.send("nevermind".encode())

def mget():
    pass

def mput():
    pass

        
def handler(data):
    """Calls specified function based on the users input"""
    command = data.split()

    for key in commands:
        if key == command[0]:
            print(key)
            commands[key]()

commands = {"get":get, "mget":mget, "mput":mput, "put":put}
   
while not_logged_in == "True":
    login()
while message != 'Q':
    #Recieved and print any sent data
    data = s.recv(1024)
    print(data.decode())
    #Error check to ensure something is entered
    while True :
        try:
            message =input(": ").strip()
            if not message:
                raise SyntaxError
            else:
                  break
        except SyntaxError:
            print("Enter a command")
    #Send the entered command
    s.send(message.encode())
    #Execute the get command
    data = s.recv(1024)
    handler(message)
            
s.close()   

