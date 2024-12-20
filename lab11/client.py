import socket
import sys
import threading
import tty
import termios

from communication import send_message, receive_message


class ChatClient:
    def __init__(self, host: str, port: int) -> None:
        self.user_input = ''
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.received_messages = []

    def run_client(self) -> None:
        """Runs the chat client."""
        self.client_socket.connect((self.host, self.port))
        try:
            self.send_client_name()
            threading.Thread(target=self.receive_and_display_messages, daemon=True).start()
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            tty.setraw(sys.stdin.fileno())
            self.user_input = ''
            print("\r> ", end="", flush=True)
            self.accept_input()
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            self.client_socket.close()

    def accept_input(self) -> None:
        """Accepts user input and sends it to the server."""
        while True:
            character = sys.stdin.read(1)
            self.user_input += character
            if character == '\x03':  # Ctrl+C
                break
            elif character == '\x7f':  # backspace
                self.user_input = self.user_input[:-2]
                print(f' \r\033[K> {self.user_input} ', end="", flush=True)
            elif character == '\r':  # Enter
                self.user_input = self.user_input[:-1]
                send_message(self.client_socket, self.user_input)
                if self.user_input == "/exit":
                    break
                self.user_input = ''
                print('\n\r> ', end="", flush=True)
            else:
                print(f'\r> {self.user_input}', end="", flush=True)

    def send_client_name(self) -> None:
        """Sends the client's name to the server."""
        message = receive_message(self.client_socket)
        while not message == "Welcome to the chat!":
            print(message)
            name = input("Enter your name: ")
            send_message(self.client_socket, name)
            message = receive_message(self.client_socket)
        print(message)

    def receive_and_display_messages(self) -> None:
        """Continuously receive messages from the server and display them in real-time."""
        while True:
            try:
                message = receive_message(self.client_socket)
                print(f"\r{message}\n\r> {self.user_input}", end="", flush=True)
            except ConnectionError:
                print("\rConnection to server lost.")
                break


if __name__ == "__main__":
    chat_client = ChatClient("localhost", 8010)
    chat_client.run_client()
