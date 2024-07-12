import socket
import threading
import mysql.connector

Host = "127.0.0.1"
Port = 65432
address = (Host, Port)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(address)
s.listen()

print("Servidor prendido, esperando conexiones...")

mipepe = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="clientServer"
)

clients = {}

def authenticate(conn):
    try:
        conn.sendall("[SERVIDOR] Ingresa tu email: ".encode())
        email = conn.recv(1024).strip().decode()
        conn.sendall("[SERVIDOR] Ingresa tu clave: ".encode())
        password = conn.recv(1024).strip().decode()

        cursor = mipepe.cursor()
        query = "SELECT * FROM usuarios WHERE email = %s AND pwd = %s"
        cursor.execute(query, (email, password))
        user = cursor.fetchone()
        cursor.close()

        if user:
            conn.sendall("[SERVIDOR] Autenticación exitosa.\n".encode())
            return email
        else:
            conn.sendall("[SERVIDOR] Credenciales inválidas.\n".encode())
            conn.close()
            return None
    except Exception as e:
        print(f"[ERROR DE AUTENTICACIÓN]: {e}")
        conn.close()
        return None

def handle_client(conn, user_email):
    try:
        while True:
            conn.sendall("\n[SERVIDOR] Menú:\n1. Chat privado\n2. Enviar mensaje broadcast\n3. Enviar mensaje privado\n4. Salir\nElige una opción: ".encode())
            option = conn.recv(1024).strip().decode()

            if option == "1":
                chat_server(conn, user_email)
            elif option == "2":
                chat_broadcast(conn, user_email)
            elif option == "3":
                chat_user(conn, user_email)
            elif option == "4":
                conn.sendall("[SERVIDOR] Saliendo del chat...".encode())
                break
            else:
                conn.sendall("\n[SERVIDOR] Opción inválida. Por favor, elige una opción válida.\n".encode())
    except Exception as e:
        print(f"[ERROR]: {e}")
    finally:
        conn.close()
        del clients[user_email]
        print(f"[DESCONECTADO] {user_email} desconectado.")

def chat_server(conn, user_email):
    conn.sendall("[SERVIDOR] Función de chat privado aún no implementada.\n".encode())

def chat_broadcast(conn, user_email):
    conn.sendall("[SERVIDOR] Ingresa tu mensaje para enviar a todos: ".encode())
    msg = conn.recv(1024).strip().decode()
    response = f"[BROADCAST] {user_email}: {msg}\n"
    for client_conn in clients.values():
        if client_conn != conn:  
            client_conn.sendall(response.encode())

def chat_user(conn, user_email):
    conn.sendall("[SERVIDOR] Ingresa el email del destinatario: ".encode())
    recipient_email = conn.recv(1024).strip().decode()
    
    if recipient_email in clients:
        recipient_conn = clients[recipient_email]
        recipient_conn.sendall(f"[SERVIDOR] Solicitud de chat privado de {user_email}. ¿Aceptar? (Sí/No): ".encode())
        response = recipient_conn.recv(1024).strip().decode()
        if response.upper() == "SI":
            conn.sendall("[SERVIDOR] Solicitud aceptada. Ingresa tu mensaje privado: ".encode())
            while True:
                msg = conn.recv(1024).strip().decode()
                response = f"[PRIVADO] {user_email}: {msg}\n"
                recipient_conn.sendall(response.encode())
        else:
            conn.sendall("[SERVIDOR] Solicitud rechazada.\n".encode())
    else:
        conn.sendall("[SERVIDOR] El usuario no está conectado.\n".encode())




def chat_private_request(conn, user_email):
    conn.sendall("[SERVIDOR] Ingresa el email del destinatario: ".encode())
    recipient_email = conn.recv(1024).strip().decode()

    if recipient_email in clients:
        recipient_conn = clients[recipient_email]
        message = f"[SERVIDOR] Solicitud de chat privado de {user_email}. ¿Aceptar? (Sí/No): "
        recipient_conn.sendall(message.encode())
        response = recipient_conn.recv(1024).strip().decode()

        if response.upper() == "SI":
                conn.sendall("[SERVIDOR] Solicitud aceptada. Ingresa tu mensaje privado: ".encode())
                while True:
                    msg = conn.recv(1024).strip().decode()
                    response = f"[PRIVADO] {user_email}: {msg}\n"
                    recipient_conn.sendall(response.encode())
        else:
            conn.sendall("[SERVIDOR] Solicitud rechazada.\n".encode())
    else:
        conn.sendall("[SERVIDOR] El usuario no está conectado.\n".encode())




while True:
    conn, addr = s.accept()
    user_email = authenticate(conn)
    if user_email:
        clients[user_email] = conn
        threading.Thread(target=handle_client, args=(conn, user_email), daemon=True).start()
