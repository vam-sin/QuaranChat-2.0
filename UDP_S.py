import time
from reliable_socket import ReliableUDPSocket

localIP     = "127.0.0.1"
localPort   = 20001
bufferSize  = 1024
timeout = 2
n = 2
# Create a reliable socket
UDPServerSocket = ReliableUDPSocket(bufferSize  = 1024, timeout = 2)

# Bind to address and ip
UDPServerSocket.bind((localIP, localPort))

print("Welcome to QuaranChat 2.0!")

# Listen for incoming datagrams
while(True):
    UDPServerSocket.receive(n)