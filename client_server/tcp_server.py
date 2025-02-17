import socket
import threading
import logging
from datetime import datetime

class TCPServer:
    def __init__(self, host='0.0.0.0', port=9998):
        self.host = host
        self.port = port
        # Configuration du logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger('TCPServer')
        
    def handle_client(self, client_socket, address):
        """Gère chaque connexion client dans un thread séparé"""
        self.logger.info(f'Nouvelle connexion de {address[0]}:{address[1]}')
        
        try:
            with client_socket:
                while True:
                    # Réception des données avec un buffer de 1024 bytes
                    data = client_socket.recv(1024)
                    if not data:
                        break
                        
                    # Décodage et logging du message reçu
                    message = data.decode('utf-8')
                    self.logger.info(f'Message reçu de {address}: {message}')
                    
                    # Préparation et envoi de la réponse
                    response = f"Message reçu à {datetime.now().strftime('%H:%M:%S')}"
                    client_socket.send(response.encode('utf-8'))
                    
        except Exception as e:
            self.logger.error(f'Erreur avec le client {address}: {str(e)}')
        finally:
            self.logger.info(f'Connexion fermée avec {address}')
            
    def start(self):
        """Démarre le serveur et attend les connexions"""
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        try:
            server.bind((self.host, self.port))
            server.listen(5)
            self.logger.info(f'Serveur démarré sur {self.host}:{self.port}')
            
            while True:
                client_socket, address = server.accept()
                # Création d'un nouveau thread pour chaque client
                client_thread = threading.Thread(
                    target=self.handle_client,
                    args=(client_socket, address)
                )
                client_thread.start()
                
        except Exception as e:
            self.logger.error(f'Erreur serveur: {str(e)}')
        finally:
            server.close()

if __name__ == '__main__':
    server = TCPServer()
    server.start() 