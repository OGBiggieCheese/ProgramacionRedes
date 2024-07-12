import socket
import threading

Host = "127.0.0.1"
Port = 65432

address = (Host, Port)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

with s:
    print("Hola, prendiendo")
    s.bind(address)
    s.listen()
    conn, addr = s.accept()
    print(f"[ESCUCHANDO] ip {Host} puerto {Port}")


    def thread():
        try:
            while True:
                data = conn.recv(1024)
                print(f"[Cliente]: {data.decode()}")
                if not data:
                    break
        except Exception as e:
            print(f"[ERROR]: {e}")

    def thread2():
        while True:
            sm = input("[SERVIDOR]: ")
            conn.sendall(sm.encode())
            if sm == "Ya no quiero hablar contigo":
                conn.close()
                print("Se ha cortado la conexión")
                break

hola = threading.Thread(target=thread, daemon=True)
hola.start()

thread2()
