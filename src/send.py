import socket, time

client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client_socket.connect(('localhost',5000))
count=0
while True:
    time.sleep(0.1)
    message=f"Message {count}"
    count+=1
    client_socket.sendall(message.encode('utf-8'))
