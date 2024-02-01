import socket

from configs import (CLIENT_WRAPPER_IP, CLIENT_WRAPPER_PORT, SEPARATOR,
                     SERVER_IP, SERVER_PORT, SERVER_WRAPPER_PORT)


def handle_server_wrapper():
    expected_seq_number = 0

    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    listen_socket.bind(("", SERVER_WRAPPER_PORT))

    while True:
        data, _ = listen_socket.recvfrom(1024)
        seq_number, message = data.decode().split(SEPARATOR)
        seq_number = int(seq_number)
        print("[SERVER][RECEIVED]", seq_number)

        if seq_number == expected_seq_number:
            expected_seq_number += 1
            listen_socket.sendto(message.encode(), (SERVER_IP, SERVER_PORT))
        listen_socket.sendto(
            f"{SEPARATOR}ack:{expected_seq_number}{SEPARATOR}".encode(),
            (CLIENT_WRAPPER_IP, CLIENT_WRAPPER_PORT),
        )
