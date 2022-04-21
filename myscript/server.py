#!/usr/bin/env python3
import socket
from colorama import *
from .sendRecv import *


class Server:
	def __init__(self):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socketClient = None
		self.address = None
		self.run = True
		self.daemon = None

	def runserver(self, host, port):
		self.socket.bind((host, port))

		print(f'Server start on port {port}')
		
		while self.run:
			try:
				self.socket.listen(5)
				self.socketClient, self.address = self.socket.accept()
				
				print("{self.address} connected")
				
				prompt = getMessage(self.socketClient)

				while self.run:
					if self.daemon is None:
						self.daemon = ThreadRecv(socket=self.socketClient)
						self.daemon.start()

					# format the prompt 
					msg = input(Fore.GREEN + prompt + Fore.WHITE)

					if self.daemon.prompt is not None:
						prompt = self.daemon.prompt

					if msg == "quit" or msg == "exit":
						self.run = False
						del self.daemon
						sendMessage(socket=self.socketClient, message=msg)
						break

					elif msg[:8] == "download":
						# send commmand to client
						sendMessage(socket=self.socketClient, message=msg)
						# the name of file to download
						file_name = msg[9:]
						# get response from client
						response = getMessage(socket=self.socketClient)
						if response == "found":
							print(Fore.BLUE + 'Start' + Fore.WHITE)
							# start receive file from client
							receiveFile(socketClient=self.socketClient, fileName=file_name)
						elif response == "not_found":
							print(Fore.RED + 'File not found' + Fore.WHITE)
						continue

					else:
						sendMessage(socket=self.socketClient, message=msg)
						continue

			except Exception as e:
				print('[Exception]', e)
				self.socket.close()
				self.run = False


if __name__ == "__main__":
	server = Server()
	server.runserver(host="localhost", port=5555)