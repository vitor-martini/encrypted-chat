import socket

IP = str(socket.gethostbyname_ex(socket.getfqdn())[2][1])
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((IP, 3000))
s.listen()

conn, addr = s.accept()
while 1:
    data = conn.recv(1024)
    print(data.decode('utf-8'))
    if not data:
        break
    conn.sendall(data)
conn.close()