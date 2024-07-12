import socket
import threading

host = "127.0.0.1"
port = 65432

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))

def pepe():
    while True:
        data = s.recv(1024)
        print(f"[SERVIDOR]: {data.decode()}")

def sech():
    while True:
        send_data = input(f"[CLIENTE {host}:{port}]: ")
        s.sendall(send_data.encode())
        if send_data == "No quiero hablar contigo":
            s.close()
            print("Se ha cerrado el socket")

pepe_thread = threading.Thread(target=pepe, daemon=True)
pepe_thread.start()
sech()
