import socket
import threading

from communication import send_message, receive_message


class ChatServer:
    def __init__(self, host="localhost", port=8010) -> None:
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.clients = {}
        self.client_lock = threading.Lock()

    def listen_client(self, client_name: str) -> None:
        """
        Continuously listens for messages from a client and broadcasts it to all connected clients.
        """
        client_socket = self.clients[client_name]
        try:
            while True:
                message = receive_message(client_socket)
                if message == "/exit":
                    break
                self.notify_clients(f"{client_name}: {message}", exclude=[client_name])
        except (ConnectionResetError, ConnectionAbortedError, ConnectionError):
            pass
        finally:
            client_socket.close()
            with self.client_lock:
                del self.clients[client_name]
            print(f"{client_name} has left the chat.")
            self.notify_clients(f"{client_name} has left the chat.")

    def notify_clients(self, message: str, exclude: list[str] = None) -> None:
        """
        Notifies all connected clients except those in the exclude list with the given message.
        """
        exclude = exclude or []
        with self.client_lock:
            for name, client_socket in self.clients.items():
                if name not in exclude:
                    send_message(client_socket, message)

    def handle_client(self, client_socket: socket.socket) -> None:
        """Handles a newly connected client."""
        try:
            name = self.get_client_name(client_socket)
            print(f"{name} has joined the chat.")
            self.notify_clients(f"{name} has joined the chat.", exclude=[name])
            threading.Thread(
                target=self.listen_client, args=(name,), daemon=True
            ).start()
        except Exception as e:
            print(f"Error handling client: {e}")
            client_socket.close()

    def get_client_name(self, client_socket: socket.socket) -> str:
        """
        Gets the name of the client, adds client to the clients dictionary, and returns the name.
        """
        name_accepted = False
        send_message(client_socket, "What is your name?")
        while not name_accepted:
            name = receive_message(client_socket)
            with self.client_lock:
                if name in self.clients:
                    send_message(
                        client_socket,
                        "Name already taken. Please choose another name.",
                    )
                else:
                    self.clients[name] = client_socket
                    name_accepted = True
                    send_message(client_socket, "Welcome to the chat!")
        return name

    def run_server(self) -> None:
        """ Runs the chat server, accepts clients, and handles them."""
        try:
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen()
            print(f"Server started on {self.host}:{self.port}")
            while True:
                client_socket, address = self.server_socket.accept()
                print(f"New connection from {address}")
                threading.Thread(
                    target=self.handle_client, args=(client_socket,), daemon=True
                ).start()
        finally:
            self.server_socket.close()


if __name__ == "__main__":
    chat_server = ChatServer(host="localhost", port=8010)
    chat_server.run_server()
