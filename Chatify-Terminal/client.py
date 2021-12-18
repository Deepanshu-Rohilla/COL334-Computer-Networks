import socket
import select
import sys
import time
import os
from threading import Thread
import colorama
from colorama import Fore, Style
import pyfiglet

result = pyfiglet.figlet_format("CHATIFY", font = "slant")
print(Fore.YELLOW + result, end = "")
print(Style.RESET_ALL)


name = sys.stdin


user_id = input("Enter username: ")
ackSend = False
ackRec = False

while not ackSend:
    serverSend = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSend.connect(("127.0.0.1", 12345))
    serverSend.send(str.encode("REGISTER TOSEND " + user_id + "\n\n"))
    ackSendResponse = serverSend.recv(1024).decode()
    if(ackSendResponse=="REGISTERED TOSEND " + user_id + "\n\n"):
        ackSend = True
    elif(ackSendResponse=="ERROR 100 Malformed username\n\n"):
        print(Fore.RED + "Invalid username. Give alphanumeric name.", end = "")
        print(Style.RESET_ALL)
        user_id = input("Enter username: ")
    elif(ackSendResponse=="ERROR 104 Username taken\n\n"):
        print(Fore.RED + "Username already taken. Try with another username.", end="")
        print(Style.RESET_ALL)
        user_id = input("Enter username: ")



while not ackRec:
    serverRec = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverRec.connect(("127.0.0.1", 12345))
    serverRec.send(str.encode("REGISTER TORECV " + user_id + "\n\n"))
    ackRecResponse = serverRec.recv(1024).decode()
    if(ackRecResponse=="REGISTERED TORECV " + user_id + "\n\n"):
        ackRec = True
    elif(ackSendResponse=="ERROR 100 Malformed username\n\n"):
        user_id = input(Fore.RED + "Invalid username. Give an alphanumeric name.", end = "")
        print(Style.RESET_ALL)
    elif(ackSendResponse=="ERROR 104 Username taken\n\n"):
        user_id = input(Fore.RED + "Username already taken. Try with another username.", end ="")
        print(Style.RESET_ALL)
if(ackRec and ackSend):
    print(Fore.GREEN + "User added successfully to the chat", end = "")
    print(Style.RESET_ALL)


def receivingThreadFun(serverRec):
    while(True):
        stringToBePrinted = ""
        l = serverRec.recv(1024).decode().split("\n")
        l1 = l[0].split(" ")
        if(l1[0]=="FORWARD"):
            try:
                senderName = l1[1]
                message = l[3]
                stringToBePrinted = stringToBePrinted + senderName + ": " + message
                print(stringToBePrinted)
                serverRec.send(str.encode("RECEIVED " + senderName + "\n\n"))
            except Exception as e:
                serverRec.send(str.encode( "ERROR 103 Header Incomplete\n\n"))



def sendingThreadFun(serverSend, message,messageFor):
    packet = "SEND " + messageFor + "\nContent-length: " + str(len(message)) + "\n\n" + message + "\n"
    serverSend.send(str.encode(packet))
    try:
        ack = serverSend.recv(1024).decode().split("\n")[0]
    except Exception as e:
        ack = "ERROR 102 Unable to send"
    
    if(ack=='SENT'):
        return
    elif(ack=="ERROR 102 Unable to send"):
        print(Fore.RED + "Invalid username. Person either not in chat or has left the chat", end = "")
        print(Style.RESET_ALL)


connect = Thread(target = receivingThreadFun, args = (serverRec,))
connect.start()

while True:
    msg = input('> ')
    if(msg!=""):
        if(msg[0]=='@'):
            messageFor = ""
            i = 1
            while(i<len(msg)):
                if(msg[i]==' '):
                    break
                else:
                    messageFor = messageFor + msg[i]
                    i = i+1
            sendingThreadFun(serverSend,msg[i+1:],messageFor)
            msg = ""
        else:
            print(Fore.RED + "No user mentioned!!", end = "")
            print(Style.RESET_ALL)
            print("Try mentioning using '@' followed by someone's name (personal message) or ALL (broadcast)")

