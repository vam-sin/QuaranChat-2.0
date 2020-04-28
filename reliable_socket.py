import socket
import json
import time
import sys
import binascii
from checksum import checksum

class ReliableUDPMessage:
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

class ReliableUDPSocket():
    pktNumber = '0' # Starts with zero always
    old_message = ''
    def __init__(self, timeout=2, bufferSize=1024):
        self.socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.timeout = timeout
        self.bufferSize = bufferSize

    def bind(self, address):
        self.socket.bind(address)

    def send(self, msgFromClient, toAddress, max_trials=10):
        packet = ReliableUDPMessage(msgFromClient, 'pkt', self.pktNumber)
        print("Packet created:\n\tMessage:" + packet.message + "\n\tType: " + packet.msgType + "\n\tNumber: " + packet.Number +"\n") 
        packet = packet.serialize()
        bytesToSend = json.dumps(packet).encode('utf-8')
        trial_num = 0
        while max_trials != 0:
            try:
                self.socket.sendto(bytesToSend, toAddress)
                print("Waiting for Acknowledgement. Trial ", trial_num)
                
                # Wait for ACK -  if it doesn't receive in set time, then timeout exception
                self.socket.settimeout(self.timeout)
                msgFromServer = self.socket.recvfrom(self.bufferSize) 
                rcvdpacket = json.loads(msgFromServer[0].decode('utf-8'))
                print("Packet from Server: " + rcvdpacket['message'] + ", Type: " + rcvdpacket['msgType'] + ", Number: " + rcvdpacket['Number'])
                print("Transmission Successful")
                if self.pktNumber == '1':
                    self.pktNumber = '0'
                else:
                    self.pktNumber = '1'
                break
            except socket.timeout:
                max_trials -= 1
                trial_num += 1
                print("Timeout! Retrasmitting!\n")

    def receive(self):
        message_address_pair = self.socket.recvfrom(self.bufferSize)
        message = json.loads(message_address_pair[0].decode('utf-8'))
        return_address = message_address_pair[1]
        ackpacket = ReliableUDPMessage("Acknowledgement", 'ack', message['Number'])
        ackpacket = ackpacket.serialize()
        bytesToSend = json.dumps(ackpacket).encode('utf-8')
        self.socket.sendto(bytesToSend, return_address)
        print("Ack Sent")
        return message, return_address