import socket
import threading
import os

HOST = 'localhost'
PORT = 5001

def handle_client(conn, addr):
    print(f"[+] Connected by {addr}")
    try:
        while True:
            # Receivefilename
            filename = conn.recv(1024).decode()
            if not filename:
                break
            print(f"[>] Receiving file: {filename}")
            with open(f"received_{filename}", 'wb') as f:
                while True:
                    data = conn.recv(4096)
                    if not data or data.endswith(b"<END>"):
                        if data.endswith(b"<END>"):
                            f.write(data[:-5])  # Remove the <END> marker
                        break
                    f.write(data)
            print(f"[✓] File {filename} received from {addr}")
    except Exception as e:
        print(f"[!] Error with {addr}: {e}")
    finally:
        conn.close()
        print(f"[-] Disconnected from {addr}")

def start_server():
    server_socket = socket.socket()
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"[SERVER] Listening on {HOST}:{PORT}...")

    while True:
        conn, addr = server_socket.accept()
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

start_server()