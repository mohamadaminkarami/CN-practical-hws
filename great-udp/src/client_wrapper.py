import re
import socket
import threading

from configs import (CLIENT_WRAPPER_PORT, LOSSY_IP, LOSSY_PORT, SEPARATOR,
                     TIMEOUT_IN_MILLISECONDS, WINDOW_SIZE)
from utils import get_current_time, is_timeout

queue = []
base = 0
sequence_number = 0
current_time = None
listen_socket = None
timeout = False


def handle_timeout():
    global current_time
    global listen_socket
    global base
    global sequence_number
    global queue
    global timeout
    while True:
        timeout = False
        if not listen_socket:
            continue
        if is_timeout(current_time, TIMEOUT_IN_MILLISECONDS):
            timeout = True
            print("[TIMEOUT] base:", base)
            current_time = get_current_time()
            for i in range(base, sequence_number):
                listen_socket.sendto(
                    f"{i}{SEPARATOR}{queue[i]}".encode(),
                    (LOSSY_IP, LOSSY_PORT),
                )
                print(f"[TIMEOUT][SEND] {i} AGAIN")


def handle_client_wrapper():
    # initialization
    global queue
    global base
    global sequence_number
    global current_time
    global listen_socket

    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    listen_socket.bind(("", CLIENT_WRAPPER_PORT))
    while True:
        data, _ = listen_socket.recvfrom(1024)
        message = data.decode()
        matched = re.match(f"{SEPARATOR}ack:([0-9]+){SEPARATOR}", message)

        # ack from server wrapper
        if matched:
            received_seq_number = int(matched.group(1))
            print(f"[CLIENT][RECEIVED] ACK {received_seq_number}")
            if base < received_seq_number:
                base = received_seq_number
                current_time = get_current_time()
            if base == sequence_number:
                current_time = None
        # message from ncat client
        else:
            queue.append(message)

        # rdt send data
        if (
            not timeout
            and sequence_number < base + WINDOW_SIZE
            and sequence_number < len(queue)
        ):
            listen_socket.sendto(
                f"{sequence_number}{SEPARATOR}{queue[sequence_number]}".encode(),
                (LOSSY_IP, LOSSY_PORT),
            )
            print("[CLIENT][SEND]", sequence_number)
            if base == sequence_number:
                current_time = get_current_time()
            sequence_number += 1
