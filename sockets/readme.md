# Chat Application avec Python Sockets

Une application de chat simple utilisant les sockets Python permettant à plusieurs utilisateurs de communiquer en temps réel.

## Comment utiliser

1. **Lancer le serveur**
   ![Serveur](1.png)
   Ouvrez un terminal et exécutez :
   ```bash
   python chat_server.py
   ```

2. **Lancer le premier client**
   ![Client 1](2.png)
   Dans un nouveau terminal :
   ```bash
   python chat_client.py
   ```
   Entrez votre pseudo quand demandé.

3. **Lancer le deuxième client**
   ![Client 2](3.png)
   Dans un autre terminal :
   ```bash
   python chat_client.py
   ```
   Entrez un pseudo différent.

## Fonctionnalités

- Chat en temps réel
- Support de plusieurs clients simultanés
- Notification quand un utilisateur rejoint ou quitte le chat
- Interface en ligne de commande simple

## Prérequis

- Python 3.x
- Aucune bibliothèque externe requise
