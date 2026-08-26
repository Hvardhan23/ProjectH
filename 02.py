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



if __name__ == "__main__":
    receive()
