import socket
import os

class ClientMp3:
    def __init__(self):
        self.HOST = 'localhost'  # Server IP address
        self.PORT = 5001

        self.client_socket = socket.socket()
        self.client_socket.connect((self.HOST, self.PORT))
        

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

    def start_client(self):
        while True:
            filename = input("Enter MP3 filename to send (or type 'exit' to quit): ").strip()
            if filename.lower() == 'exit':
                break
            self.send_mp3(filename)

    def send_mp3(self, filename):
        print(f"[CLIENT] Connected to server at {self.HOST}:{self.PORT}")

        try:
            self.send_file(filename, self.client_socket)
        except Exception as e:
            print(f"[!] Error: {e}")
        finally:
            self.client_socket.close()
            print("[CLIENT] Disconnected.")