import socket
import logging
import json

class TCPClient:
    def __init__(self, host='localhost', port=9998):
        self.host = host
        self.port = port
        # Configuration du logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger('TCPClient')
        
    def send_message(self, message):
        """Envoie un message au serveur et attend la réponse"""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            try:
                # Connexion au serveur
                client.connect((self.host, self.port))
                self.logger.info(f'Connecté au serveur {self.host}:{self.port}')
                
                # Envoi du message
                if isinstance(message, dict):
                    message = json.dumps(message)
                client.send(message.encode('utf-8'))
                self.logger.info(f'Message envoyé: {message}')
                
                # Réception de la réponse
                response = client.recv(4096).decode('utf-8')
                self.logger.info(f'Réponse reçue: {response}')
                return response
                
            except Exception as e:
                self.logger.error(f'Erreur: {str(e)}')
                return None
            
    def interactive_mode(self):
        """Mode interactif pour envoyer des messages"""
        print(f'\n--- Envoyez des messages à {self.host}:{self.port} (tapez "quit" pour sortir) ---\n')
        
        while True:
            message = input("Message > ")
            if message.lower() == 'quit':
                break
                
            response = self.send_message(message)
            if response:
                print(f"Réponse: {response}\n")

if __name__ == '__main__':
    client = TCPClient()
    client.interactive_mode() 