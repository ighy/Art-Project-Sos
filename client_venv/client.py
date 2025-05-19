import socket
import threading

def receive_messages(client_socket):
    while True:
        try:
            response = client_socket.recv(1024).decode()
            if not response:
                break
            print(f"Received from server: {response}")
        except ConnectionResetError:
            break
    print("Disconnected from the server.")
    client_socket.close()

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 12345))
print("Connected to the server.")

# Start a thread to handle receiving messages
threading.Thread(target=receive_messages, args=(client_socket,), daemon=True).start()

# Main thread handles sending messages to the server
while True:
    try:
        message = input("Enter the message: ")
        client_socket.send(message.encode())
    except (ConnectionResetError, BrokenPipeError, KeyboardInterrupt):
        print("\nClosing connection.")
        client_socket.close()
        break
