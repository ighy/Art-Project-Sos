import socket
import os

class ClientMp3:
    
    def __init__(self):
        self.HOST = 'localhost'  # Server IP address
        self.PORT = 5001
        
        self.client_socket = socket.socket()
        self.client_socket.connect((self.HOST, self.PORT))

        print(f"[CLIENT] Connected to server at {self.HOST}:{self.PORT}")

    def handle_input(self, filename):
        try:
            if filename.lower() == 'exit':
                pass
            self.send_file(filename)
        except Exception as e:
            print(f"[!] Error: {e}")
        finally:
            self.client_socket.close()
            print("[CLIENT] Disconnected.")

    def send_file(self, filename):
        if not os.path.isfile(filename):
            print("[!] File does not exist.")
            return

        self.client_socket.sendall(filename.encode())
        with open(filename, 'rb') as f:
            while chunk := f.read(4096):
                self.client_socket.sendall(chunk)
        self.client_socket.sendall(b"<END>")  # Signal end of file
        print("[✓] File sent successfully.")