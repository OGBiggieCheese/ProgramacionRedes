import socket
import threading

Host = "127.0.0.1"
Port = 65432
address = (Host, Port)


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(address)

def receive_messages(sock):
    try:
        while True:
            message = sock.recv(1024).decode()
            if not message:
                break
            print(message)
    except Exception as e:
        print(f"[ERROR]: {e}")

def send_messages(sock):
    try:
        while True:
            message = input()
            sock.sendall(message.encode())
            if message.lower() == "4":
                break
    except Exception as e:
        print(f"[ERROR]: {e}")





receive_thread = threading.Thread(target=receive_messages, args=(s,), daemon=True)
send_thread = threading.Thread(target=send_messages, args=(s,))

receive_thread.start()
send_thread.start()
send_thread.join()
s.close()
