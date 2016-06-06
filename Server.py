#Zelarous & Group
#SERVER

import socket
import os

argumants = {}


#This function checks to make 
def check_login(username, password):
    """Reads from a specified text file with username and password information. It then checks to make sure that the
    user's input is valid. If the username and password are correct, this function returns true. Otherwise it returns
    false"""
    read_file = open("Jeff.txt")
    user_information = read_file.read().splitlines()
    print(user_information[0] + " " + user_information[1])
    if username == user_information[0] and password == user_information[1]:
        print("Access to server granted")
        read_file.close()
        return True
    else:
        print("Access to server DENIED")
        read_file.close()
        return False

def login():
    """Allows the user to input their username and password, that information is then fed into the function
    valid_long(user, pass). If valid_login returns true, it breaks and allows the user to 'enter' the server"""
    while True:
        client.send("Username: ".encode())
        username = client.recv(1024)
        client.send("Password: ".encode())
        password = client.recv(1024)
        valid_login = check_login(username.decode(), password.decode())
        if valid_login:
            client.send("ACCESS TO SERVER GRANTED".encode())
            client.send("What woudld you like to do?".encode())
            break

s = socket.socket()
s.bind((socket.gethostname(), 5000))
s.listen(5)
client, client_ip = s.accept()


def confirmation():
    """Sends confirmation output to the client."""
    client.send("Data recieved".encode())

def cd():
    """"""
    global directory
    global root_directory
    
    client.send("Type in the name of a folder (include \\folderName)".encode())

    path_name = client.recv(1024).decode()
    new_directory = directory

    if path_name[0] == "r" and path_name[1] == "o" and path_name[2] == "o" and path_name[3] == "t":
        directory = root_directory
        print(len(path_name))
        if len(path_name) > 4:
            for x in range(4, len(path_name)):
                new_directory += path_name[x]
                print(path_name[x])
            directory = new_directory
            print(directory)
        else:
            directory = root_directory

    new_directory = directory + path_name
    
    if os.path.exists(new_directory):
       directory = new_directory
       confirmation()
       confirmation()
    else:
        client.send("That directory path does not exist.".encode())
        confirmation()
    
    
    
def ls():
    """"""
    directory_contents = os.listdir(directory)
    directory_contents = '\n'.join(directory_contents)
    client.send(str(directory_contents).encode())
    confirmation()

def get():
    """"""
    #Recieve the name of the file from the client
    name = client.recv(1024).decode()
    #Check to see if the file exists and if so send it
    try:
        file = open(name, 'rb')
        #SEND CONFIRMATION
        client.send("I HAVE THE FILE".encode())
        #Begin seperating the file into pieces to send
        piece = file.read(1024)
        while piece :
            client.send(piece)
            client.recv(1024)
            piece = file.read(1024)
        #Send a confirmation and close the file
        client.send("Your download has finished.".encode())
        file.close()
        confirmation()
    except FileNotFoundError:
        print("FILE NOT FOUND")
        client.send("NO".encode())
        client.send("What would you like to do?".encode())

def put():
    #Recive file confirmation from the client
    confirm = client.recv(1024).decode()
    if confirm != "nevermind":
        #Recieve the name of the file from the client
        name = confirm
        #Open the file to send
        f = open(name, 'wb')
        #Begin recieving the pieces
        l = client.recv(1024)
        while l:
            f.write(l)
            client.send("Recieved data".encode())
            l = client.recv(1024)
            #Check if the final piece has been sent
            try:
                if l.decode()== "Your download has finished.":
                    l = ""
            except UnicodeDecodeError:
                pass
        #Close the file
        f.close()
        client.send("Done".encode())
    else:
        client.send("What would you like to do?".encode())
    
def mget():
    """"""
    numFiles = client.recv(1024).decode()
    numFiles = int(numFiles)
    print(numFiles)
    for x in range(0, numFiles):
        #Recieve the name of the file from the client
        name = client.recv(1024).decode()
        #Check to see if the file exists and if so send it
        try:
            print("here")
            file = open(name, 'rb')
            #SEND CONFIRMATION
            client.send("I HAVE THE FILE".encode())
            #Begin seperating the file into pieces to send
            piece = file.read(1024)
            while piece :
                client.send(piece)
                client.recv(1024)
                piece = file.read(1024)
            #Send a confirmation and close the file
            client.send("Your download has finished.".encode())
            file.close()
        except FileNotFoundError:
            print(name)
            print("FILE NOT FOUND")
            client.send("NO".encode())   
    client.send("TRANSFERS COMPLETE".encode())

def mput():
    """"""
    numFiles = client.recv(1024).decode()
    numFiles = int(numFiles)
    for x in range(0, numFiles):
        #Recive file confirmation from the client
        confirm = client.recv(1024).decode()
        if confirm != "nevermind":
            #Recieve the name of the file from the client
            name = client.recv(1024).decode()
            #Open the file to send
            f = open(name, 'wb')
            #Begin recieving the pieces
            l = client.recv(1024)
            while l:
                f.write(l)
                client.send("Recieved data".encode())
                l = client.recv(1024)
                #Check if the final piece has been sent
                try:
                    if l.decode()== "Your download has finished.":
                        l = ""
                except UnicodeDecodeError:
                    pass
            #Close the file
            f.close()
            client.send("Done".encode())
        else:
            client.send("What would you like to do?".encode())
        

def dir():
    """"""
    pass

def handler(data):
    """Calls specified function based on the users input"""
    command = data.split()
    confirmation()

    for key in commands:
        if key == command[0]:
            print(key)
            commands[key]()

commands = {"cd":cd, "ls":ls, "get":get, "mget":mget, "mput":mput,"dir":ls,
            "put":put}

def check_for_valid_input(data):
    """Checks the users input to make sure that it is valid"""
    data_list = data.split()
    for key in commands:
        if key == data_list[0]:
            return True
    client.send("INVALID INPUT".encode())
    client.send("INVALID INPUT".encode())
    return False

login()
root_directory = os.getcwd() # NEVER CHANGE THIS
directory = os.getcwd()

while True:
    data = client.recv(1024).decode()
    valid_input = check_for_valid_input(data)
    if valid_input:
        handler(data)

