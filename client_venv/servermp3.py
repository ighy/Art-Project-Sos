import socket
import threading
import os

class ServerMp3:
    def __init__(self, HOST='localhost', PORT=5001):
        self.HOST = HOST
        self.PORT = PORT

        self.server_socket = socket.socket()

    def handle_client(self, conn, addr, funct):
        print(f"[+] Connected by {addr}")
        try:
            while True:
                # Receive filename
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
                funct(filename)
        except Exception as e:
            print(f"[!] Error with {addr}: {e}")
        finally:
            conn.close()
            print(f"[-] Disconnected from {addr}")

    def start_server(self, funct):
        self.server_socket.bind((self.HOST, self.PORT))
        self.server_socket.listen(5)
        self.recieving_state = 1
        print(f"[SERVER] Listening on {self.HOST}:{self.PORT}...")

        while True:
            conn, addr = self.server_socket.accept()
            threading.Thread(target=self.handle_client, args=(conn, addr, funct), daemon=True).start()

    def end_server(self):
        self.recieving_state = 0


ServerMp3()
