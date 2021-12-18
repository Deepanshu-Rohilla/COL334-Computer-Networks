import sys
import time
import socket 
# from _thread import *
from threading import Thread
from collections import defaultdict as df
import colorama
from colorama import Fore, Style
import pyfiglet

numberOfClients = 0
users = {}


class User:
	def __init__(self,):
		self.socketSend = None
		self.socketRec = None
		self.name = ''

def add_user(user : User):
	if user.name not in users:
		users[user.name] = user
	else:
		existing = users[user.name]
		if user.socketRec and existing.socketRec:
			pass
		if user.socketSend and existing.socketSend:
			pass
		elif user.socketSend and existing.socketRec:
			existing.socketSend = user.socketSend
		elif user.socketRec and existing.socketSend:
			existing.socketRec = user.socketRec



def start(server):
	server.bind(("127.0.0.1", int(12345)))
	server.listen(100)
	result = pyfiglet.figlet_format("CHATIFY", font = "slant")
	print(Fore.YELLOW + result, end = "")
	print(Style.RESET_ALL)
	print(Fore.GREEN + "Server initialised successfully", end ="")
	print(Style.RESET_ALL)

	while True:
		connection, address = server.accept()
		print(str(address[0]) + ":" + str(address[1]) + " Connected")
		thread = Thread(target = clientThread, args = (server, connection))
		thread.start()


	server.close()

def clientThread(server, connection):
	name = ""
	receive = -1
	length = 0
	message = ""
	isReg = False
	while True:
		l = connection.recv(1024).decode().split("\n")
		l1 = l[0].split(" ")
		if(not isReg):
			if(l1[0]=='REGISTER'):
				isReg = True
				name = l1[2]
				if(not name.isalnum()):
					connection.send(str.encode("ERROR 100 Malformed username\n\n"))
				else:
					if(l1[1]=='TOSEND'):
						for user in users:
							if(name==user and users[name].socketSend):
								connection.send(str.encode("ERROR 104 Username taken\n\n"))
								return
						connection.send(str.encode("REGISTERED TOSEND " + name + "\n\n"))
						receive = 0
					if(l1[1]=='TORECV'):
						for user in users:
							if(name==user and users[name].socketRec):
								connection.send(str.encode("ERROR 104 Username taken\n\n"))
								return
						connection.send(str.encode("REGISTERED TORECV " + name + "\n\n"))
						receive = 1
					user = User()
					user.name = name
					if receive==0:
						user.socketSend = connection
					elif receive==1:
						user.socketRec = connection
					else:
						pass
					add_user(user)
					if(receive==1):
						return
			else:
				connection.send(str.encode("ERROR 101 No user registered\n\n"))

		else:
			if(l1[0]=="SEND"):
				try:
					name = l1[1]
					l2 = l[1].split(" ")
					if(l2[0]!='Content-length:'): # mal
						pass
					else:
						length = int(l2[1])
					message = l[3]
				except Exception as e:
					connection.send(str.encode("ERROR 103 Header incomplete\n\n"))
				senderName = ""
				found = False
				for x in users:
					if(users[x].socketSend == connection):
						found = True
						senderName = x
						break
				if found:
					if(name=='ALL'):
						sahi = True
						for user in users:
							if(user!=x):
								sendToSocket = users[user].socketRec
								packet = "FORWARD " + senderName + "\n" + "Content-length: " + str(length) + "\n\n"  + message + " (sent to ALL)"
								sendToSocket.send(str.encode(packet))
								try:
									ack = sendToSocket.recv(1024).decode().split("\n")
								except Exception as e:
									try:
										users.pop(user)
										connection.send(str.encode("ERROR 102 Unable to send\n\n"))
									except:
										pass
								ack1 = ack[0].split(" ")
								sahi = sahi and ack1[0]=='RECEIVED'
						if sahi:
							connection.send(str.encode("SENT"))
					else:
						try:
							sendToSocket = users[name].socketRec
						except Exception as e:
							connection.send(str.encode("ERROR 102 Unable to send\n\n"))
						
						packet = "FORWARD " + senderName + "\n" + "Content-length: " + str(length) + "\n\n" + message
						sendToSocket.send(str.encode(packet))
						try:
							ack = sendToSocket.recv(1024).decode().split("\n")
						except Exception as e:
							try:
								users.pop(name)
								connection.send(str.encode("ERROR 102 Unable to send\n\n"))
							except:
								pass

						ack1 = ack[0].split(" ")
						if(ack1[0]=='RECEIVED'):
							senderName = ack1[1]
							connection.send(str.encode("SENT"))
				else:
					connection.send(str.encode("ERROR 102 Unable to send\n\n"))



			elif(l1[0]=="ERROR"):
				pass

if __name__ == '__main__':
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	start(server)

    