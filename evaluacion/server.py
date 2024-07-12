import socket
import threading
import mysql.connector

usuarios = ["pepe", "sech", "hola", "pep"]
contraseñas = ["1234", "2345", "3456", "4567"]

Host = "127.0.0.1"
Port = 65432
adr = (Host, Port)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def authenticate(conn):
    try:
        conn.sendall("Esperando tu logeo (utiliza /login usuario contraseña)".encode())
        data = conn.recv(1024).decode()
        
        if data.startswith("/login"):
            partes = data.split()
            if len(partes) == 3:
                usuario = partes[1]
                contraseña = partes[2]
                if usuario in usuarios:
                    indice = usuarios.index(usuario)
                    if contraseñas[indice] == contraseña:
                        conn.sendall(f"[SERVIDOR]: Bienvenido {usuario}, ten un buen dia".encode())
                        return True
                    else:
                        conn.sendall("[SERVIDOR]: Contraseña incorrectos".encode())
                        conn.close()
                else:
                    conn.sendall("[SERVIDOR]: El usuario ingresado no ha sido encontrado. Se cerrara la conexion".encode())
                    conn.close()
            else:
                conn.sendall("[SERVIDOR]: No estas utilizando correctamente el comando. Sigue las insturcciones. Se cerrara la conexion".encode())
                conn.close()
        else:
            conn.sendall("[SERVIDOR]: No estas ejecutando el comando de logeo. Se cerrara la conexion".encode())
            conn.close()    
    except Exception as e:
        print(f"[ERROR]: {e}")


def recibir_mensaje(conn):
    try:
        while True:
            msg = conn.recv(1024)
            if not msg:
                break
            print(f"[CLIENTE]: {msg.decode()}")
    except Exception as e:
        print(f"[ERROR]: {e}")

def enviar_mensaje(conn):
    try:
        while True:
            msg = input("[SERVIDOR]: ")
            conn.sendall(msg.encode())
            if msg.lower() == "no mas":
                conn.close()
                print("[SERVIDOR]: Se ha acabado la conexión")
                break
    except Exception as e:
        print(f"[ERROR]: {e}")

with s:
    print(f"[ESPERANDO...] El servidor está esperando conexiones en {adr}...")
    s.bind(adr)
    s.listen()

    conn, addr = s.accept()
    print(f"[CONEXION] Conexión aceptada de {addr}")

    if authenticate(conn):
        recibir_thread = threading.Thread(target=recibir_mensaje, args=(conn,), daemon=True)
        recibir_thread.start()
        enviar_mensaje(conn)
    else:
        conn.close()
