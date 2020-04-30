import time
import sys
from reliable_socket import ReliableUDPSocket

# Throughput Calcualtions
start = time.time()
packets_sent = 0
total_time = 10
n = 2 # The number of unacked packets that can be sent

serverAddressPort = ("127.0.0.1", 20001)

# Create a UDP socket at client side
UDPClientSocket = ReliableUDPSocket()

# Send messages, one by one, to server using created ReliableUDPSocket
while True: 
    UDPClientSocket.send(serverAddressPort)
    packets_sent += n
    if time.time() - start >= total_time:
        throughput = packets_sent/(time.time()-start)
        print(str(throughput) + " packets per second " + "\n")
        exit()
