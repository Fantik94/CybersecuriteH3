import ftplib

def ftp_connect():
    ftp = ftplib.FTP()
    ftp.connect('127.0.0.1', 2121)  # Connexion au conteneur proxy
    ftp.login('user', 'pass')  # Connexion avec les identifiants du serveur FTP
    print(ftp.getwelcome())
    ftp.quit()

if __name__ == "__main__":
    ftp_connect() 