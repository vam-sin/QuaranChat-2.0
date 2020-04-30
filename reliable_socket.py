import socket
import json
import sys
import time
import math
from checksum import * 

class ReliableUDPMessage:
    # Constructor
    def __init__(self, message, msgType, number):
        self.message = message
        self.msgType = msgType # pkt or ack
        self.number = number
        self.checksum = ChecksumCalculation("127.0.0.1", "127.0.0.1", 17, 10, 20001, 20001, 1024, message)

    # has to be done in order to send through the socket
    def serialize(self):
        packet_dict = {
            "message": self.message,
            "msgType": self.msgType,
            "number": self.number,
            "checksum": self.checksum
        }
        return packet_dict

class ReliableUDPSocket():
    pktNumber = 0 # Starts with zero always
    def __init__(self, timeout=0.1, bufferSize=1024):
        self.socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.timeout = timeout
        self.bufferSize = bufferSize

    def bind(self, address):
        self.socket.bind(address)

    def reverse_pkt_number(self):
        if self.pktNumber == 1:
            self.pktNumber = 0
        else:
            self.pktNumber = 1

    def send(self, msgFromClient, toAddress):
        packet = ReliableUDPMessage(msgFromClient, 'pkt', self.pktNumber)
        # print("Packet created:\n\tMessage: ", packet.message, "\n\tType: ", packet.msgType, "\n\tNumber: ", packet.number, "\n") 
        packet = packet.serialize()
        bytesToSend = json.dumps(packet).encode("utf-8")
        trial_num = 0
        while True:
            try:
                self.socket.sendto(bytesToSend, toAddress)
                print("Waiting for Acknowledgement. Trial ", trial_num)
                # Wait for ACK -  if it doesn't receive in set time, then timeout exception
                self.socket.settimeout(self.timeout)
                msgFromServer = self.socket.recvfrom(self.bufferSize) 
                rcvdpacket = json.loads(msgFromServer[0])
                if ChecksumVerification("127.0.0.1", "127.0.0.1", 17, 10, 20001, 20001, 1024, rcvdpacket['message'], int(rcvdpacket['checksum'])):
                    print("[CHECKSUM] Recived acknowledgement was not correct.")
                    if self.pktNumber == rcvdpacket['number']:
                        print("Transmission Successful")
                        self.reverse_pkt_number()
                        return
                    else:
                        print("Incorrect ACK received. Retransmit.")
                else:
                    print("[CHECKSUM] Received Acknowledgement was corrupt.")

            except socket.timeout:
                trial_num += 1
                print("Timeout! Retrasmitting!\n")


    def receive(self):
        while True:
            message_address_pair = self.socket.recvfrom(self.bufferSize)
            message = json.loads(message_address_pair[0].decode('utf-8'))
            return_address = message_address_pair[1]
            if ChecksumVerification("127.0.0.1", "127.0.0.1", 17, 10, 20001, 20001, 1024, message['message'], int(message['checksum'])):
                print("Received message packet was pristine.")
                ackpacket = ReliableUDPMessage("Acknowledgement", 'ack', message['number'])
                ackpacket = ackpacket.serialize()
                bytesToSend = json.dumps(ackpacket).encode('utf-8')
                self.socket.sendto(bytesToSend, return_address)
                print("Ack Sent")
                if message["number"] == self.pktNumber:
                    self.reverse_pkt_number()
                    break
                else:
                    print("Appears like a duplicate packet")
            else:
                print("Received Message Packet was corrupt.")
        return message, return_address

