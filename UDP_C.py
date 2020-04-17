import socket
import json
import time
import sys

# Task Set 1
# a) No loss (Done) 
# b) Packet Loss ( Done)
# # Retramsit should take the same message and not ask again
# c) ACK loss (Done) (Same behavior as a packet loss, have to retransmit that same packet)
# d) Premature timeout/ dealyed ACK

# Task Set 2
# a) Pocket Corruption (use checksum)

serverAddressPort = ("127.0.0.1", 20001)
bufferSize = 1024
timeout = 2
pktNumber = '0' # Starts with zero always
retransmit = 0 # Flag to say if retransmit or not
old_message = ''

class ReliableUDPPacket:
    # Constructor
    def __init__(self, message, msgType, Number):
        self.message = message
        self.msgType = msgType # pkt or ack
        self.Number = Number

    # has to be done in order to send through the socket
    def serialize(self):
    	packet_dict = {
    		"message": self.message,
    		"msgType": self.msgType,
    		"Number": self.Number
    	}

    	return packet_dict

def Transmit(UDPClientSocket):
	global retransmit
	global old_message
	try:
		global pktNumber
		sys.stdout.flush()
		if retransmit == 0:
			msgFromClient = input("Your Message: ")
		else:
			msgFromClient = old_message
		packet = ReliableUDPPacket(msgFromClient, 'pkt', pktNumber) 
		packet = packet.serialize()
		bytesToSend = json.dumps(packet).encode('utf-8')
		# print(bytesToSend)
		UDPClientSocket.sendto(bytesToSend, serverAddressPort)

		# Receive ACK
		print("Waiting for Acknowledgement")
		UDPClientSocket.settimeout(timeout)
		msgFromServer = UDPClientSocket.recvfrom(bufferSize) # if it doesn't receive in set time, then timeout exception
		rcvdpacket = json.loads(msgFromServer[0].decode('utf-8'))
		print("Packet from Server: " + rcvdpacket['message'] + ", Type: " + rcvdpacket['msgType'] + ", Number: " + rcvdpacket['Number'])
		retransmit = 0
		if pktNumber == '1':
			pktNumber = '0'
		else:
			pktNumber = '1'
	except socket.timeout:
		print("Timeout! Retrasmitting!")
		retransmit = 1
		old_message = msgFromClient
		sys.stdout.flush()
		Transmit(UDPClientSocket)

# Create a UDP socket at client side
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Send to server using created UDP socket
while True:
	# Send Packet to Server
	Transmit(UDPClientSocket)