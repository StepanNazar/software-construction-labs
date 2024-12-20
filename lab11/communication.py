"""Module for sending and receiving length-prefixed messages over a socket."""

import socket


def send_message(
    client_socket: socket.socket, message: str, prefix_length: int = 4
) -> None:
    """
    Sends a length-prefixed message over the socket.

    :param client_socket: the socket to send the message over
    :param message: the message to send
    :param prefix_length: the length of the message prefix in digits
    """
    length = len(message)
    client_socket.sendall(f"{length:0{prefix_length}d}".encode())
    client_socket.sendall(message.encode())


def receive_message(client_socket: socket.socket, prefix_length: int = 4) -> str:
    """
    Receives a length-prefixed message from the socket.

    :param client_socket: the socket to receive the message from
    :param prefix_length: the length of the message prefix in digits
    :return: the received message
    :raises ConnectionError: if the message could not be received
    """
    try:
        prefix_length = int(client_socket.recv(prefix_length).decode())
        return client_socket.recv(prefix_length).decode()
    except:
        raise ConnectionError
