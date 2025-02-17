import socket
import threading

class ChatClient:
    def __init__(self, host='127.0.0.1', port=55555):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))
        self.nickname = input("Choisissez votre pseudo: ")
        
    def receive(self):
        while True:
            try:
                message = self.client.recv(1024).decode('utf-8')
                if message == 'NICK':
                    self.client.send(self.nickname.encode('utf-8'))
                else:
                    print(message)
            except:
                print("Une erreur est survenue!")
                self.client.close()
                break
                
    def write(self):
        while True:
            message = f'{self.nickname}: {input("")}'
            self.client.send(message.encode('utf-8'))
            
    def start(self):
        receive_thread = threading.Thread(target=self.receive)
        receive_thread.start()
        
        write_thread = threading.Thread(target=self.write)
        write_thread.start()

if __name__ == "__main__":
    client = ChatClient()
    client.start() 