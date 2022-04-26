import os
import threading

from colorama import *

# global variable
ENCODING = 'utf-8'
BUFFERSIZE = 1024


def receiveFile(socketClient, fileName):
    """
    Le fonction qui telecharger les fichiers venants du client
    :param socketClient: le socket du client qui fait le telechargement
    :param fileName: nom du fichier a telecharger
    :return: None
    """
    if socketClient is not None:
        with open(f"{fileName}", "wb+") as file_from_client:
            data = socketClient.recv(BUFFERSIZE ** 2)
            file_from_client.write(data)
            print(Fore.BLUE + 'End' + Fore.WHITE)


def getMessage(socket):
    if socket is None:
        raise Exception("socket is None, the socket should be connected init before")
    return socket.recv(BUFFERSIZE).decode(ENCODING)


def sendMessage(socket, message):
    if socket is not None:
        socket.send(message.encode(ENCODING))


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
                    # Formater le reponse
                    print("\n\n" + Fore.YELLOW + self.message + Fore.WHITE)

            except Exception as e:
                print(f"[Exception]=>{e}")
                self.socket.close()
                break

    def kill(self):
        os.kill(self.native_id, 9)
