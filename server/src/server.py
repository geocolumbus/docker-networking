# Listens to the specified port and logs out whatever it recieves

import socket
import time
import os

# get the hostname and ip_addr for the container
hostname = os.popen("hostname").read().strip()
ip_addr = os.popen("hostname -i").read().strip()

LISTEN_PORT = int(os.getenv("LISTEN_PORT") or "5000")

print(f"Server listening to {hostname} on {ip_addr}:{LISTEN_PORT}")

# it will only work if you bind to the ip_addr. "localhost" won't work.
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((ip_addr, LISTEN_PORT))
    s.listen()
    while True:
        print("Waiting for a connection.")
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")

            # Start the listen loop
            while True:
                # Listens and log messages
                time.sleep(2)
                data = conn.recv(1024)
                if data:
                    print(data)
        print("Connection lost")
