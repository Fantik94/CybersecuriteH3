import argparse
import nmap
import json
import subprocess
import threading
import logging
from queue import Queue

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

class PortScanner:
    def __init__(self, target="127.0.0.1", start_port=1000, end_port=8000, threads=10):
        self.target = target
        self.start_port = start_port
        self.end_port = end_port
        self.threads = threads
        self.results = []
        self.port_queue = Queue()
        
    def worker(self, thread_id, show_process):
        """Fonction exécutée par chaque thread"""
        logging.info(f"Thread-{thread_id} démarré.")
        while not self.port_queue.empty():
            port = self.port_queue.get()
            logging.info(f"Thread-{thread_id} analyse le port {port}.")
            scan_data = self.scan_port(port, show_process)
            if scan_data:
                self.results.append(scan_data)
            self.port_queue.task_done()
        logging.info(f"Thread-{thread_id} terminé.")
            
    def scan_port(self, port, show_process):
        """Analyse un port spécifique"""
        nm = nmap.PortScanner()
        nm.scan(self.target, str(port))
        
        for host in nm.all_hosts():
            for proto in nm[host].all_protocols():
                lport = nm[host][proto].keys()
                for p in lport:
                    if p == port:
                        port_state = nm[host][proto][p]['state']
                        port_info = {"port": port, "state": port_state}
                        
                        if port_state == 'open' and show_process:
                            process_info = self.get_process_details(port)
                            port_info["process"] = process_info
                            
                        logging.info(f"Port {port} sur {self.target} est {port_state}.")
                        return port_info
        return None
        
    def get_process_details(self, port):
        """Obtient les détails du processus sur un port"""
        cmd = f"sudo lsof -iTCP:{port} -sTCP:LISTEN"
        try:
            process = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if process.stdout:
                lines = process.stdout.splitlines()
                if len(lines) > 1:
                    details = lines[1].split()
                    pid = details[1]
                    process_name = details[0]
                    process_info = self.get_process_info(pid)
                    return {
                        "pid": pid,
                        "name": process_name,
                        "location": process_info.get("cwd", "Inconnu"),
                        "command": process_info.get("cmdline", "Inconnu")
                    }
        except Exception as e:
            logging.error(f"Erreur lors de l'analyse du processus sur le port {port}: {e}")
        return {}
        
    def get_process_info(self, pid):
        """Récupère les informations d'un processus"""
        try:
            proc_info = {}
            with open(f"/proc/{pid}/cwd") as f:
                proc_info["cwd"] = f.read().strip()
            with open(f"/proc/{pid}/cmdline") as f:
                proc_info["cmdline"] = f.read().strip().replace('\x00', ' ')
            return proc_info
        except Exception as e:
            logging.error(f"Impossible de récupérer les infos du PID {pid}: {e}")
            return {"cwd": "Inconnu", "cmdline": "Inconnu"}
            
    def run(self, show_process=False):
        """Lance le scan"""
        logging.info(f"Démarrage du scan sur {self.target} du port {self.start_port} au port {self.end_port}")
        
        # Remplir la queue avec les ports
        for port in range(self.start_port, self.end_port + 1):
            self.port_queue.put(port)
            
        # Créer et démarrer les threads
        threads = []
        for i in range(self.threads):
            thread = threading.Thread(
                target=self.worker,
                args=(i+1, show_process)
            )
            threads.append(thread)
            thread.start()
            
        # Attendre la fin des threads
        for thread in threads:
            thread.join()
            
        return {"host": self.target, "ports": self.results}

def main():
    parser = argparse.ArgumentParser(description="Scanner de ports Python avec informations sur les processus.")
    parser.add_argument("-t", "--target", default="127.0.0.1", help="Adresse IP cible (défaut: localhost)")
    parser.add_argument("-sp", "--start-port", type=int, default=1000, help="Port de début (défaut: 1000)")
    parser.add_argument("-ep", "--end-port", type=int, default=8000, help="Port de fin (défaut: 8000)")
    parser.add_argument("-p", "--process", action="store_true", help="Afficher les infos des processus")
    parser.add_argument("-o", "--output", default="scan_results.json", help="Fichier de sortie JSON (défaut: scan_results.json)")
    parser.add_argument("-th", "--threads", type=int, default=10, help="Nombre de threads (défaut: 10)")
    
    args = parser.parse_args()
    
    scanner = PortScanner(
        args.target,
        args.start_port,
        args.end_port,
        args.threads
    )
    
    results = scanner.run(args.process)
    
    with open(args.output, 'w') as json_file:
        json.dump(results, json_file, indent=4)
        logging.info(f"Résultats sauvegardés dans {args.output}")

if __name__ == "__main__":
    main() 