from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from urllib.parse import urlparse, parse_qs

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def _set_headers(self, content_type='text/html'):
        self.send_response(200)
        self.send_header('Content-type', content_type)
        self.end_headers()
        
    def do_GET(self):
        """Gère les requêtes GET"""
        parsed_path = urlparse(self.path)
        
        # Route racine
        if parsed_path.path == '/':
            self._set_headers()
            response = "Bienvenue sur le serveur HTTP Python!"
            
        # Route /api
        elif parsed_path.path == '/api':
            self._set_headers('application/json')
            response = json.dumps({
                "message": "Ceci est une API",
                "status": "OK"
            })
            
        # Route inconnue
        else:
            self.send_response(404)
            self.end_headers()
            response = "Page non trouvée"
            
        self.wfile.write(response.encode('utf-8'))
        
    def do_POST(self):
        """Gère les requêtes POST"""
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        self._set_headers('application/json')
        response = {
            "message": "Données reçues",
            "data": post_data.decode('utf-8')
        }
        
        self.wfile.write(json.dumps(response).encode('utf-8'))

def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Serveur démarré sur le port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run() 