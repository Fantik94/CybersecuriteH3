import socket
import threading

class ChatServer:
    def __init__(self, host='127.0.0.1', port=55555):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen()
        self.clients = []
        self.nicknames = []
        
    def broadcast(self, message):
        for client in self.clients:
            client.send(message)
            
    def handle_client(self, client):
        while True:
            try:
                message = client.recv(1024)
                self.broadcast(message)
            except:
                index = self.clients.index(client)
                self.clients.remove(client)
                client.close()
                nickname = self.nicknames[index]
                self.broadcast(f'{nickname} a quitté le chat!'.encode('utf-8'))
                self.nicknames.remove(nickname)
                break
                
    def start(self):
        print("Le serveur est démarré...")
        while True:
            client, address = self.server.accept()
            print(f"Connecté avec {str(address)}")
            
            client.send('NICK'.encode('utf-8'))
            nickname = client.recv(1024).decode('utf-8')
            self.nicknames.append(nickname)
            self.clients.append(client)
            
            print(f'Le pseudo du client est {nickname}!')
            self.broadcast(f'{nickname} a rejoint le chat!'.encode('utf-8'))
            client.send('Connecté au serveur!'.encode('utf-8'))
            
            thread = threading.Thread(target=self.handle_client, args=(client,))
            thread.start()

if __name__ == "__main__":
    server = ChatServer()
    server.start() 