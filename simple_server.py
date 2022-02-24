import threading
import socket

host = socket.gethostbyname(socket.gethostname())
port = 9090

s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.bind((host,port))

s.listen(5)

clients = []
nicknames = []

def trans(mess):
    for client in clients:
        client.send(mess)
        
def handle_connection(client): 
    quit = False
    print("[ Server Started ]")
    while not quit:
        try:
            message = client.recv(1024)
            trans(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            nicknames.remove(nicknames[index])
            trans(f"{nicknames[index]} left the chat.".encode('utf-8'))
            quit = True

def main():
    print("SERVER POSHOLLL...")
    while True:
        client, addr = s.accept()
        print(f"Connected to {addr}")
        
        client.send("NICK".encode('utf-8'))
        
        nickname = client.recv(1024).decode('utf-8')
        nicknames.append(nickname)
        clients.append(client)
        
        print(f"Nick is {nickname}")
        
        trans(f"{nickname} joined the chat.".encode('utf-8'))
        
        client.send("You are now connected".encode('utf-8'))
        
        thread = threading.Thread(target= handle_connection, args=(client,))
        thread.start()
        
if __name__ == '__main__':
    main()