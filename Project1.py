import socket
import threading

# Server function to handle clients
def handle_client(connection, client_address):
    print(f"Connected by {client_address}")
    try:
        data = connection.recv(1024)  # Receive up to 1024 bytes
        if data:
            print(f"Received: {data.decode()}")
            connection.sendall(data)  # Echo back
        else:
            print(f"No data received from {client_address}")
    except Exception as e:
        print(f"Error handling client {client_address}: {e}")
    finally:
        connection.close()
        print(f"Connection closed for {client_address}")

# Server Code
def start_server():
    host = 'localhost'
    port = 8080

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen(5)  # Allow up to 5 clients in the queue
        print(f"Server listening on {host}:{port}")

        while True:
            conn, addr = server_socket.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()  # Handle each client in a separate thread

# Client Code
def start_client():
    host = 'localhost'
    port = 8080

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        try:
            print("Connecting to server...")
            client_socket.connect((host, port))
            message = "Hello, Server!"
            client_socket.sendall(message.encode())

            data = client_socket.recv(1024)
            print(f"Response from server: {data.decode()}")

        except Exception as e:
            print(f"Error: {e}")

        print("Client socket closed.")

# Run server in a separate thread for testing
if __name__ == "__main__":
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()

    # Run client after a short delay
    import time
    time.sleep(1)
    start_client()
