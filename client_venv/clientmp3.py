import socket
import os

class ClientMp3:
    
    def __init__(self, HOST='localhost', PORT=5001):
        self.HOST = HOST
        self.PORT = PORT
        self.sending_state = 1
        
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

    def close_socket(self):
        self.client_socket.close()
        print("[CLIENT] Disconnected.")
