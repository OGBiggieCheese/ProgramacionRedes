""" import socket

host = "127.0.0.1"
port = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host,port))
    s.sendall(b"Holaaaaaaaaaaaaaaaaaaa a todos")
    data = s.recv(1024)

print(f"Recibi {data!r}") """

import socket

host = "127.0.0.1"
port = 1002

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host,port))

file = open("pepetoro.jpg", "rb")

ImageData = file.read(2048)

while ImageData:
    s.send(ImageData)
    ImageData = file.read(2048)


file.close()
s.close()