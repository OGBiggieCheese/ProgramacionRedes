import socket
import threading

Host = "127.0.0.1"
Port = 65432
adr = (Host, Port)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(adr)

def recibir_mensaje():
    try:
        while True:
            msg = s.recv(1024)
            if not msg:
                break
            print(f"[SERVIDOR]: {msg.decode()}")
    except Exception as e:
        print(f"[ERROR]: {e}")

def enviar_mensaje():
    try:
        while True:
            msg = input(f"[CLIENTE]: ")
            s.sendall(msg.encode())
            if msg.lower() == "no mas":
                s.close()
                print("Se ha terminado")
                break
    except Exception as e:
        print(f"[ERROR]: {e}")

recibir_thread = threading.Thread(target=recibir_mensaje, daemon=True)
recibir_thread.start()
enviar_mensaje()
