import time
import sys
from reliable_socket import ReliableUDPSocket

# Throughput Calcualtions
start = time.time()
packets_sent = 0

serverAddressPort = ("127.0.0.1", 20001)

# Create a UDP socket at client side
UDPClientSocket = ReliableUDPSocket()

# Send messages, one by one, to server using created ReliableUDPSocket
while True:
    sys.stdout.flush()
    print("\n\n\n")
    print("#################################")
    print("\n\n\n")
    # Regular
    msgFromClient = input("Your Message: ")
    # Throughput Calculation
    # msgFromClient = "ClientMessage"
    print("\n")
    UDPClientSocket.send(msgFromClient, serverAddressPort)
    packets_sent += 1
    print(str(packets_sent) + " packets sent in " + str(time.time() - start) + " seconds. \n")