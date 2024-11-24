#import socket module
from socket import *
import sys  # For terminating the program
import threading  # For handling multiple threads

# Define a function to handle client requests
def handle_client(connectionSocket):
    try:
        # Receive the HTTP request message
        message = connectionSocket.recv(1024).decode()  # Decode the received bytes
        
        # Parse the requested filename from the HTTP request
        filename = message.split()[1]
        
        # Open the requested file
        f = open(filename[1:], "r", encoding="utf-8")  # Strip the leading '/' from the filename
        
        # Read the content of the file
        outputdata = f.read()
        f.close()
        
        # Send an HTTP response header line
        header = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n"
        connectionSocket.send(header.encode())
        
        # Send the content of the requested file to the client
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())
        
        connectionSocket.send("\r\n".encode())  # Send the end of line
    except IOError:
        # Send response message for file not found (404 error)
        error_message = "HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\n" \
                        "<html><head></head><body><h1>404 Not Found</h1></body></html>"
        connectionSocket.send(error_message.encode())
    finally:
        # Close the connection socket
        connectionSocket.close()

# Create a server socket
serverSocket = socket(AF_INET, SOCK_STREAM)

# Prepare the server socket
serverPort = 6789  # Use a specific port number
serverSocket.bind(('', serverPort))  # Bind to the specified port
serverSocket.listen(5)  # Server is ready to listen to incoming connections

print("Ready to serve...")

while True:
    # Establish the connection
    connectionSocket, addr = serverSocket.accept()  # Accept incoming connections
    print(f"Connection received from {addr}")
    
    # Create a new thread to handle the client request
    client_thread = threading.Thread(target=handle_client, args=(connectionSocket,))
    client_thread.start()  # Start the thread

# Close the server socket (unreachable here but would be used for cleanup)
serverSocket.close()
sys.exit()  # Terminate the program after sending the corresponding data

