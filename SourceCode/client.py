import sys
from socket import *

def main():
    if len(sys.argv) != 4:
        print("Usage: python client.py <server_host> <server_port> <filename>")
        sys.exit()

    # Command-line arguments
    server_host = sys.argv[1]
    server_port = int(sys.argv[2])
    filename = sys.argv[3]

    try:
        # Create a TCP client socket
        client_socket = socket(AF_INET, SOCK_STREAM)

        # Connect to the server
        client_socket.connect((server_host, server_port))
        print(f"Connected to server at {server_host}:{server_port}")

        # Create the HTTP GET request
        request = f"GET /{filename} HTTP/1.1\r\nHost: {server_host}\r\n\r\n"
        client_socket.send(request.encode())

        # Receive the server's response
        response = b""
        while True:
            chunk = client_socket.recv(1024)
            if not chunk:
                break
            response += chunk

        # Print the server response
        print(response.decode())

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Close the socket
        client_socket.close()
        print("\nConnection closed.")

if __name__ == "__main__":
    main()
