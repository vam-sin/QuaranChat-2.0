import socket
import json
import time

serverAddressPort = ("127.0.0.1", 20001)
bufferSize = 1024
timeout = 0.5

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

# Create a UDP socket at client side
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Send to server using created UDP socket
while True:
	msgFromClient = input("Your Message:")
	packet = ReliableUDPPacket(msgFromClient, 'pkt', '1') 
	packet = packet.serialize()
	bytesToSend = json.dumps(packet).encode('utf-8')
	# print(bytesToSend)
	UDPClientSocket.sendto(bytesToSend, serverAddressPort)

	# Receive ACK
	time.sleep(timeout)

	msgFromServer = UDPClientSocket.recvfrom(bufferSize)
	rcvdpacket = json.loads(msgFromServer[0].decode('utf-8'))
	print("Packet from Server: " + rcvdpacket['message'] + ", Type: " + rcvdpacket['msgType'] + ", Number: " + rcvdpacket['Number'])