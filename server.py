import socket
import threading
import server_config

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.clients = []
        self.nicknames = []
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))

    def broadcast(self, message):
        for client in self.clients:
            client.send(message)

    def handleClient(self, client):
        while True:
            try:
                message = client.recv(1024)
                self.broadcast(message)
            except:
                index = self.clients.index(client)
                self.clients.remove(client)
                client.close()
                nickname = self.nicknames[index]
                self.broadcast(f'{nickname} wyszedł z czatu!'.encode('utf-8'))
                self.nicknames.remove(nickname)
                break

    def start(self):
        self.server.listen()
        print(f'Nasłuchiwanie na porcie {self.port}')
        while True:
            client, address = self.server.accept()
            print(f'Połączono z {str(address)}')

            client.send('NICK'.encode('utf-8'))
            nickname = client.recv(1024).decode('utf-8')
            self.nicknames.append(nickname)
            self.clients.append(client)

            print(f'Nazwa połączonej osoby to {nickname}')
            self.broadcast(f'{nickname} dołączył do czatu.'.encode('utf-8'))
            client.send('Połączono z serwerem.'.encode('utf-8'))

            thread = threading.Thread(target=self.handleClient, args=(client,))
            thread.start()

if __name__ == '__main__':
    server = Server(server_config.Config.getHost(), server_config.Config.getPort())
    server.start()