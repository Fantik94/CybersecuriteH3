import socket
import logging
import json
from datetime import datetime
import os
import ctypes
import sys
import time

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

class NetworkSniffer:
    def __init__(self, host='127.0.0.1'):
        self.host = host
        try:
            # Configuration du logging avec plus de détails
            logging.basicConfig(
                filename='sniffer.log',
                level=logging.INFO,
                format='%(asctime)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            self.logger = logging.getLogger('NetworkSniffer')
            self.logger.info(f"Sniffer initialisé sur {self.host}")
            print(f"Sniffer initialisé sur {self.host}")
        except Exception as e:
            print(f"Erreur d'initialisation du logging: {e}")
            
    def save_packet(self, data, packet_type="UNKNOWN"):
        try:
            timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            filename = f"packet_{timestamp}.json"
            
            packet_data = {
                "timestamp": timestamp,
                "size": len(data),
                "type": packet_type,
                "data": data.hex()
            }
            
            with open(filename, 'w') as json_file:
                json.dump(packet_data, json_file, indent=4)
            
            self.logger.info(f"Paquet {packet_type} capturé - Taille: {len(data)} bytes - Sauvegardé dans {filename}")
            print(f"Paquet capturé! Type: {packet_type}, Taille: {len(data)} bytes")
            
        except Exception as e:
            self.logger.error(f"Erreur lors de la sauvegarde: {e}")
            print(f"Erreur lors de la sauvegarde: {e}")
        
    def analyze_packet(self, data):
        """Analyse basique du type de paquet"""
        try:
            # Analyse de l'en-tête IP
            ip_header = data[0:20]
            protocol = ip_header[9]
            
            if protocol == 1:
                return "ICMP"
            elif protocol == 6:
                return "TCP"
            elif protocol == 17:
                return "UDP"
            else:
                return f"PROTOCOL-{protocol}"
        except:
            return "UNKNOWN"
        
    def start_sniffing(self):
        sniffer = None
        try:
            self.logger.info("Démarrage du sniffer...")
            print("Création du socket...")
            
            sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
            sniffer.bind((self.host, 0))
            self.logger.info(f"Socket lié à {self.host}")
            
            sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
            sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
            self.logger.info("Mode promiscuous activé")
            
            print("\nSniffer démarré. En attente de paquets...")
            print("Faites un ping dans un autre terminal...")
            print("Appuyez sur Ctrl+C pour arrêter\n")
            
            while True:
                data = sniffer.recvfrom(65535)[0]
                packet_type = self.analyze_packet(data)
                self.save_packet(data, packet_type)
                
        except socket.error as e:
            error_msg = f"Erreur socket: {e}"
            self.logger.error(error_msg)
            print(error_msg)
            if hasattr(e, 'winerror') and e.winerror == 10013:
                self.logger.error("Privilèges administrateur requis!")
                print("Erreur: Privilèges administrateur requis!")
        except Exception as e:
            error_msg = f"Erreur inattendue: {str(e)}"
            self.logger.error(error_msg)
            print(error_msg)
        finally:
            if sniffer:
                try:
                    sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
                    self.logger.info("Mode promiscuous désactivé")
                except:
                    pass
                sniffer.close()
                self.logger.info("Sniffer arrêté")
                print("Sniffer arrêté")

def main():
    try:
        if not is_admin():
            print("Ce programme nécessite des privilèges administrateur!")
            print("Veuillez relancer en tant qu'administrateur.")
            time.sleep(5)
            sys.exit(1)
            
        print("Démarrage du sniffer réseau...")
        sniffer = NetworkSniffer()
        sniffer.start_sniffing()
    except Exception as e:
        print(f"Erreur dans le programme principal: {str(e)}")
    finally:
        print("\nAppuyez sur Entrée pour quitter...")
        input()

if __name__ == '__main__':
    main() 