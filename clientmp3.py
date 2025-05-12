import socket
import os

HOST = 'localhost'  # Server IP address
PORT = 5001

def send_file(filename, client_socket):
    if not os.path.isfile(filename):
        print("[!] File does not exist.")
        return

    client_socket.sendall(filename.encode())
    with open(filename, 'rb') as f:
        while chunk := f.read(4096):
            client_socket.sendall(chunk)
    client_socket.sendall(b"<END>")  # Signal end of file
    print("[✓] File sent successfully.")

def start_client():
    client_socket = socket.socket()
    client_socket.connect((HOST, PORT))
    print(f"[CLIENT] Connected to server at {HOST}:{PORT}")

    try:
        while True:
            filename = input("Enter MP3 filename to send (or type 'exit' to quit): ").strip()
            if filename.lower() == 'exit':
                break
            send_file(filename, client_socket)
    except Exception as e:
        print(f"[!] Error: {e}")
    finally:
        client_socket.close()
        print("[CLIENT] Disconnected.")

start_client()