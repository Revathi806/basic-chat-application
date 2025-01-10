import socket
import threading

clients = {}
addresses = {}

def handle_client(client_socket, addr):
    username = client_socket.recv(1024).decode('utf-8')
    clients[username] = client_socket
    addresses[client_socket] = addr
    print(f"{username} has connected from {addr}")

    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                broadcast(message, username)
        except:
            break

    client_socket.close()
    del clients[username]
    del addresses[client_socket]
    print(f"{username} has disconnected.")

def broadcast(message, username):
    for client in clients.values():
        client.send(f"{username}: {message}".encode('utf-8'))

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('127.0.0.1', 5050))
    server.listen()
    print("Server is listening...")

    while True:
        client_socket, addr = server.accept()
        threading.Thread(target=handle_client, args=(client_socket, addr)).start()

start_server()