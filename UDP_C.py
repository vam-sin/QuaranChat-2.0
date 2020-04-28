import socket
import json
import time
import sys
import binascii
from checksum import checksum

# Throughput Calcualtions
start = time.time()
packets_sent = 0

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
	global packets_sent
	try:
		global pktNumber
		sys.stdout.flush()
		if retransmit == 0:
			print("\n\n\n")
			print("#################################")
			print("\n\n\n")
			# Regular
			msgFromClient = input("Your Message: ")
			# Throughput Calculation
			# msgFromClient = "ClientMessage"
			print("\n")
		else:
			msgFromClient = old_message
		packet = ReliableUDPPacket(msgFromClient, 'pkt', pktNumber)
		print("Packet sent from Client: " + packet.message + ", Type: " + packet.msgType + ", Number: " + packet.Number) 
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
		print("Transmission Successful")
		packets_sent += 1
		print(str(packets_sent) + " packets sent in " + str(time.time() - start) + " seconds. \n")
		
		# Throughput calculations
		# if (time.time() - start) >= 10.0:
		# 	print("Throughtput is: " + str(packets_sent/(time.time() - start)) + " packets per second")
		# 	exit()
		
		retransmit = 0
		if pktNumber == '1':
			pktNumber = '0'
		else:
			pktNumber = '1'
	except socket.timeout:
		print("Timeout! Retrasmitting!\n")
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