import socket
import threading

def handle_client(client_socket, addr):
    print(f"Connection from {addr} has been established!")

    # Thread to handle receiving messages from the client
    def receive_messages():
        while True:
            try:
                data = client_socket.recv(1024).decode()
                if not data:
                    break
                print(f"Received from client: {data}")
            except ConnectionResetError:
                break
        print(f"Connection from {addr} closed.")
        client_socket.close()

    # Start the receiving thread
    threading.Thread(target=receive_messages, daemon=True).start()

    # Main thread handles sending messages to the client
    while True:
        try:
            response = input("Enter a message to send to the client: ")
            client_socket.send(response.encode())
        except (ConnectionResetError, BrokenPipeError):
            break

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 12345))
server_socket.listen(5)  # Allow up to 5 queued connections
print("Server is listening...")

while True:
    client_socket, addr = server_socket.accept()
    threading.Thread(target=handle_client, args=(client_socket, addr)).start()
