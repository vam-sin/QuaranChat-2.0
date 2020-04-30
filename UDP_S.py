import time
from reliable_socket import ReliableUDPSocket

localIP     = "127.0.0.1"
localPort   = 20001
bufferSize  = 1024
timeout = 2

# Create a reliable socket
UDPServerSocket = ReliableUDPSocket(bufferSize  = 1024, timeout = 2)

# Bind to address and ip
UDPServerSocket.bind((localIP, localPort))

print("Welcome to QuaranChat 2.0!")

# Listen for incoming datagrams
while(True):
    received_packet, address = UDPServerSocket.receive()
    print("Packet from Client: " + received_packet['message'] + ", Type: " + received_packet['msgType'] + ", Number: " + str(received_packet['number']))