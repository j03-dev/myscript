import threading
from colorama import *


# global variable
ENCODAGE = 'utf-8'
BUFFERSIZE = 1024


def receiveFile(socketClient, fileName):            
	# the fucntion who download file from client
	if socketClient is not None:
		with open(f"{fileName}", "wb") as file_from_client:
			data = socketClient.recv(BUFFERSIZE**2)
			file_from_client.writeData(data)
			print(Fore.BLUE + 'End' + Fore.WHITE)


def getMessage(socket):
	if socket is None:
		raise Exception("socket is None")
	return socket.recv(BUFFERSIZE).decode(ENCODAGE)


def sendMessage(socket, message):
	if socket is not None:
		socket.send(message.encode(ENCODAGE))


class ThreadRecv(threading.Thread):
	def __init__(self, socket):
		threading.Thread.__init__(self)
		self.socket = socket
		self.message = None
		self.prompt = None

	def run(self):
		while True:
			try:
				self.message = getMessage(self.socket)

				if self.message == "quit":
					self.socket.close()
					break

				elif self.message == "chdir":
					self.prompt = getMessage(self.socket)

				else:
					# format the response
					print("\n\n" + Fore.YELLOW + self.message + Fore.WHITE)

			except Exception as e:
				print(f"[Exception]=>{e}")
				self.socket.close()
				break
