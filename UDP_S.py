import socket
import json

localIP     = "127.0.0.1"
localPort   = 20001
bufferSize  = 1024

class ReliableUDPPacket:
    # Constructor
    def __init__(self, message, msgType, Number):
        self.message = message
        self.msgType = msgType
        self.Number = Number

    def serialize(self):
    	packet_dict = {
    		"message": self.message,
    		"msgType": self.msgType,
    		"Number": self.Number
    	}

    	return packet_dict

# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip
UDPServerSocket.bind((localIP, localPort))

print("UDP server up and listening")

# Listen for incoming datagrams
while(True):
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    rcvdpacket = json.loads(bytesAddressPair[0].decode('utf-8'))
    address = bytesAddressPair[1]
    print("Packet from Client: " + rcvdpacket['message'] + ", Type: " + rcvdpacket['msgType'] + ", Number: " + str(rcvdpacket['Number']))
    
    # Sending ack to client
    ackpacket = ReliableUDPPacket("Acknowledgement", 'ack', rcvdpacket['Number'])
    ackpacket = ackpacket.serialize()
    bytesToSend = json.dumps(ackpacket).encode('utf-8')
    UDPServerSocket.sendto(bytesToSend, address)