import socket, time

client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client_socket.bind(('localhost',5000))
client_socket.listen()
conn, addr = client_socket.accept()
print(f"Connected by {addr}")
while True:
    time.sleep(1)
    data=conn.recv(1024)
    if not data: continue
    print(data)
