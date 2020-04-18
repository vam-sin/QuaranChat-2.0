import socket
import json
import time

localIP     = "127.0.0.1"
localPort   = 20001
bufferSize  = 1024

def Checksum_Calculation(message, msgType, Number):
	messagebin = bin(int.from_bytes(message.encode(), 'big'))
	msgTypebin = bin(int.from_bytes(msgType.encode(), 'big'))
	Numberbin = bin(int.from_bytes(Number.encode(), 'big'))

	checksum = int(messagebin, 2) + int(msgTypebin, 2) + int(Numberbin, 2)

	return checksum

class ReliableUDPPacket:
    # Constructor
    def __init__(self, message, msgType, Number):
        self.message = message
        self.msgType = msgType
        self.Number = Number
        self.checksum = Checksum_Calculation(message, msgType, Number)

    def serialize(self):
    	packet_dict = {
    		"message": self.message,
    		"msgType": self.msgType,
    		"Number": self.Number,
    		"checksum": self.checksum
    	}

    	return packet_dict

# Create a datagram socket (895)
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip
UDPServerSocket.bind((localIP, localPort))

print("Welcome to QuaranChat 2.0!")

# Listen for incoming datagrams
while(True):
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    rcvdpacket = json.loads(bytesAddressPair[0].decode('utf-8'))
    address = bytesAddressPair[1]
    print("Packet from Client: " + rcvdpacket['message'] + ", Type: " + rcvdpacket['msgType'] + ", Number: " + str(rcvdpacket['Number']))
    
    # Sending ack to client
    # time.sleep(4)
    if int(rcvdpacket['checksum']) != Checksum_Calculation(rcvdpacket['message'], rcvdpacket['msgType'], rcvdpacket['Number']):
    	print("Corrupted Packet")
    else:
    	print("Pristine Packet")
    	ackpacket = ReliableUDPPacket("Acknowledgement", 'ack', rcvdpacket['Number'])
    	ackpacket = ackpacket.serialize()
    	bytesToSend = json.dumps(ackpacket).encode('utf-8')
    	UDPServerSocket.sendto(bytesToSend, address)
    	print("Ack Sent")