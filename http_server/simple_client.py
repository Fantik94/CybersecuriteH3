import requests
import json

class SimpleHTTPClient:
    def __init__(self, base_url='http://localhost:8000'):
        self.base_url = base_url
        
    def get_root(self):
        """Teste la route racine"""
        response = requests.get(self.base_url)
        return response.text
        
    def get_api(self):
        """Teste la route /api"""
        response = requests.get(f'{self.base_url}/api')
        return response.json()
        
    def post_data(self, data):
        """Envoie des données en POST"""
        response = requests.post(
            self.base_url,
            json=data
        )
        return response.json()

def test_server():
    client = SimpleHTTPClient()
    
    # Test GET /
    print("\nTest GET /")
    print(client.get_root())
    
    # Test GET /api
    print("\nTest GET /api")
    print(json.dumps(client.get_api(), indent=2))
    
    # Test POST
    print("\nTest POST /")
    data = {"message": "Hello Server!"}
    print(json.dumps(client.post_data(data), indent=2))

if __name__ == '__main__':
    test_server() 