import socket
import threading

# Server configuration
HOST = "0.0.0.0"  # Listen on all network interfaces
PORT = 5000       # Port to listen on
clients = []      # List to store connected clients

def broadcast(message, sender):
    """Send a message to all clients except the sender."""
    for client in clients:
        if client != sender:
            try:
                client.sendall(message.encode())
            except:
                clients.remove(client)

def handle_client(client_socket, address):
    """Handle communication with a connected client."""
    print(f"New connection: {address}")
    client_socket.send("Welcome to the radio transmission server!".encode())
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if not message:
                break
            print(f"Message from {address}: {message}")
            broadcast(f"{address}: {message}", client_socket)
        except:
            break
    print(f"Connection closed: {address}")
    clients.remove(client_socket)
    client_socket.close()

def start_server():
    """Start the server to accept connections."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"Server listening on {HOST}:{PORT}")

    while True:
        client_socket, address = server_socket.accept()
        clients.append(client_socket)
        threading.Thread(target=handle_client, args=(client_socket, address)).start()

if __name__ == "__main__":
    start_server()
