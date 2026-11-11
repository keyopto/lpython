import socket
from threading import Thread

host = 'localhost'
port = 8080
clients = {}
addresses = {}

# SOCK_STREAM is for TCP, SOCK_DGRAM is for UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((host, port))


def broadcast(msg, prefix=""):
    """
    Broadcasts a message to all connected clients.
    """
    disconnected_clients = []
    for client in clients:
        try:
            client.send(bytes(prefix, "utf8") + msg)
        except (BrokenPipeError, OSError):
            disconnected_clients.append(client)

    for client in disconnected_clients:
        if client in clients:
            del clients[client]
        if client in addresses:
            del addresses[client]
        client.close()


def handle_client(conn, addr):
    """
    Handles a single client connection.
    """
    try:
        conn.send(
            "Welcome to our chat, Please Type your name to continue".encode('utf8'))

        name = conn.recv(1024).decode('utf8')
        welcome = "Welcome " + name + \
            ". You can type #quit if you want to leave the chat room."
        conn.send(bytes(welcome, "utf8"))

        msg = name + " has joined the chat!"
        broadcast(msg.encode('utf8'))
        clients[conn] = name
        while True:
            msg = conn.recv(1024)
            if not msg:
                break
            if msg != bytes("#quit", "utf8"):
                broadcast(msg, name + ": ")
            else:
                conn.send(bytes("#quit", "utf8"))
                conn.close()
                del clients[conn]
                broadcast(bytes(name + " has left the chat.", "utf8"))
                break
    except (BrokenPipeError, OSError, ConnectionResetError):
        pass
    finally:
        if conn in clients:
            del clients[conn]
        if conn in addresses:
            del addresses[conn]
        conn.close()


def accept_client_connection():
    """
    Accepts incoming client connections and starts a new thread for each client.
    """
    while True:
        client_connection, client_address = sock.accept()
        print(client_address, "has connected.")
        addresses[client_connection] = client_address

        Thread(target=handle_client, args=(
            client_connection, client_address)).start()


if __name__ == "__main__":
    # Start listening for X incoming connections
    sock.listen(5)
    print("Server is listening for incoming connections...")

    t1 = Thread(target=accept_client_connection)
    t1.start()
    t1.join()

    sock.close()
