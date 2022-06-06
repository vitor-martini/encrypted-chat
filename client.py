import socket
IP = '192.168.15.7'
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((IP, 3000))

while True:
    message = input()
    if message == 'exit':
        break
    s.sendall(bytes(message, 'utf-8'))
    data = s.recv(1024)

s.close()