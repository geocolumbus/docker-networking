# Listens to defined port and logs out whatever it recieves
# Tries to send messages to other container

import socket
import time
import os

SERVER_IP = os.getenv("SERVER_IP") or "localhost"
SERVER_PORT = int(os.getenv("SERVER_PORT") or "5000")
MESSAGE = os.getenv("MESSAGE") or "default message"

print(f'Connecting to "{MESSAGE}" at {SERVER_IP}:{SERVER_PORT}')

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    connected = False
    while not connected:
        try:
            time.sleep(2)
            s.connect((SERVER_IP, SERVER_PORT))
            connected = True
        except Exception as e:
            print(f"Unable to connect because {e}")

    # Start the message sending loop
    count = 0
    while True:
        time.sleep(2)
        try:
            count += 1
            message = f"{count} - {MESSAGE}"
            s.sendall(message.encode())
        except Exception as e:
            print(
                f'Unable to send "{MESSAGE}" to {SERVER_IP}:{SERVER_PORT} because {e}'
            )
            count -= 1
