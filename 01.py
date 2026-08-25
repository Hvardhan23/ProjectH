##cost fun
#value
#edit review
#fun
import socket
import threading

# Server configuration
HOST = '127.0.0.1'  # Localhost
PORT = 55555        # Choose any unassigned port above 1024

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []
nicknames = []

# Send messages to all connected clients
def broadcast(message):
    for client in clients:
        try:
            client.send(message)
        except:
            # Remove broken connections
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            nicknames.remove(nickname)
            break

# Handle individual client communication
def handle_client(client):
    while True:
        try:
            # Receive message from client
            message = client.recv(1024)
            broadcast(message)
        except:
            # Handle disconnection cleanly
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            print(f"{nickname} left the chat.")
            broadcast(f"{nickname} left the chat!".encode('utf-8'))
            nicknames.remove(nickname)
            break

# Main execution loop to accept connections
def receive():
    print(f"Server is listening on {HOST}:{PORT}...")
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        # Prompt client for a nickname
        client.send('NICK'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        nicknames.append(nickname)
        clients.append(client)

        print(f"Nickname of client is {nickname}!")
        broadcast(f"{nickname} joined the chat!\n".encode('utf-8'))
        client.send('Connected to the server!'.encode('utf-8'))

        # Start a thread to manage this unique client connection
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

if __name__ == "__main__":
    receive()
