#!/usr/bin/env python3
import socket

try:
    from .sendRecv import *
except:
    from sendRecv import *


class Server:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socketClient = None
        self.address = None
        self.run = True
        self.threadRecv = None

    def runServer(self, host: str, port: int) -> None:
        """
        Le fonction qui lance le server
        :param host: adresse ip du server 127.0.0.1 ou localhost ou 0.0.0.0
        :param port: example: 5555
        :return: None
        """
        try:
            self.socket.bind((host, port))
        except:
            print(f"Le port {port} est encore utiliser")

        print(f'Server start on port {port}')

        while self.run:
            try:
                # attente de client
                self.socket.listen(5)
                self.socketClient, self.address = self.socket.accept()

                print(f"{self.address} connected")

                prompt = getMessage(self.socketClient)

                while self.run:
                    if self.threadRecv is None:
                        # initialiser threadRecv, qui va tourner en arriere-plant pour
                        # recevoire tout les messsages venant du client
                        print("start receive response from client")
                        self.threadRecv = ThreadRecv(socket=self.socketClient)
                        self.threadRecv.start()

                    if self.threadRecv.prompt is not None:
                        prompt = self.threadRecv.prompt

                    # prompt for shell
                    msg = input(Fore.GREEN + prompt + Fore.WHITE)

                    if msg == "quit" or msg == "exit":
                        self.run = False
                        del self.threadRecv
                        sendMessage(socket=self.socketClient, message=msg)
                        break

                    elif msg[:8] == "download":
                        # envoi le commmand au client
                        sendMessage(socket=self.socketClient, message=msg)
                        # le nom du fichier a telecharger
                        file_name = msg[9:]
                        # recevoire la reponse venant du client
                        response = getMessage(socket=self.socketClient)
                        if response == "found":
                            print(Fore.BLUE + 'Start' + Fore.WHITE)
                            # commence a recevoire le fichier venant du client
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
    server.runServer(host="localhost", port=5555)
