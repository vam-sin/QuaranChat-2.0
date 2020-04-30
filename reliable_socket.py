import socket
import json
import sys
import time
import math
from checksum import * 

class ReliableUDPMessage:
    # Constructor
    def __init__(self, message, msgType, number, sno):
        self.message = message
        self.msgType = msgType # pkt or ack
        self.number = number
        self.sno = sno
        self.checksum = ChecksumCalculation("127.0.0.1", "127.0.0.1", 17, 10, 20001, 20001, 1024, message)

    # has to be done in order to send through the socket
    def serialize(self):
    	packet_dict = {
    		"message": self.message,
    		"msgType": self.msgType,
    		"number": self.number,
            "sno": self.sno,
            "checksum": self.checksum
    	}

    	return packet_dict

class ReliableUDPSocket():
    pktNumber = 0 # Starts with zero always
    SerialNumber = 1 # First packet has sno 1
    SentPackets = []
    ReceivedPackets = []
    PacketObjects = []
    def __init__(self, timeout=2, bufferSize=1024):
        self.socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.timeout = timeout
        self.bufferSize = bufferSize

    def bind(self, address):
        self.socket.bind(address)

    def send(self, toAddress):
        maxObjects = 2
        numNewObjects = 2
        sys.stdout.flush()
        print("\n\n\n")
        print("#################################")
        print("\n\n\n")
        # Regular
        if self.SerialNumber == 1:
            pass
        else:
            for k in range(len(self.SentPackets)):
                if self.SentPackets[k] not in self.ReceivedPackets:
                    packet = self.PacketObjects[k]
                    print("Packet created: Message: ", packet.message, " Type: ", packet.msgType, " Number: ", packet.number, " SerialNumber: ", packet.sno,"\n") 
                    packet = packet.serialize()
                    # print(packet)
                    bytesToSend = json.dumps(packet).encode("utf-8")
                    self.socket.sendto(bytesToSend, toAddress)
                    numNewObjects -= 1

        msgFromClient = []
        for i in range(numNewObjects):
            msgFromClient.append(input("Your Message: "))
            # Throughput Calculation
            # msgFromClient.append("Hello")
            # print("Inputted\n")

        # numbers for the new packets
        if self.SerialNumber == 1:
            pass
        else:
            lastpacket = self.PacketObjects[len(self.PacketObjects) - 1]
            if lastpacket.number == 1:
                self.pktNumber = 0
            else:
                self.pktNumber = 1

        for i in range(numNewObjects):
            packet = ReliableUDPMessage(msgFromClient[i], 'pkt', self.pktNumber, self.SerialNumber)
            self.PacketObjects.append(packet)
            self.SentPackets.append(self.SerialNumber)
            self.SerialNumber += 1
            if self.pktNumber == 1:
                self.pktNumber = 0
            else:
                self.pktNumber = 1
            print("Packet created: Message: ", packet.message, " Type: ", packet.msgType, " Number: ", packet.number, " SerialNumber: ", packet.sno,"\n") 
            packet = packet.serialize()
            # print(packet)
            bytesToSend = json.dumps(packet).encode("utf-8")
            self.socket.sendto(bytesToSend, toAddress)
        print("Waiting for Acknowledgements")
        
        # Wait for ACK -  if it doesn't receive in set time, then timeout exception
        self.socket.settimeout(self.timeout)
        for i in range(maxObjects):
            try:
                msgFromServer = self.socket.recvfrom(self.bufferSize) 
                rcvdpacket = json.loads(msgFromServer[0])
                if ChecksumVerification("127.0.0.1", "127.0.0.1", 17, 10, 20001, 20001, 1024, rcvdpacket['message'], int(rcvdpacket['checksum'])):
                    if int(rcvdpacket['sno']) in self.ReceivedPackets:
                        print("Duplicate Acknowledgement received for packet with serial number " + str(rcvdpacket['sno']))
                    else:
                        print("Recived Acknowledgement was pristine.")
                        print("Packet from remote host: ", rcvdpacket['message'], ", Type: ", rcvdpacket['msgType'], ", Number: ", rcvdpacket['number'], ", SerialNumber: ", rcvdpacket['sno'])
                        print("Transmission Successful for packet with serial number " + str(rcvdpacket['sno']))
                        self.ReceivedPackets.append(int(rcvdpacket['sno']))

                else:
                    print("Received Acknowledgement was corrupt.")

            except socket.timeout:
                print("Not all packets were received before timeout! Retrasmitting!\n")

        self.send(toAddress)

    def receive(self, n):
        print("\n\n\n")
        print("#################################")
        print("\n\n\n")
        sys.stdout.flush()
        for i in range(n):
            message_address_pair = self.socket.recvfrom(self.bufferSize)
            message = json.loads(message_address_pair[0].decode('utf-8'))
            return_address = message_address_pair[1]
            if ChecksumVerification("127.0.0.1", "127.0.0.1", 17, 10, 20001, 20001, 1024, message['message'], int(message['checksum'])):
                print("Received Message Packet was pristine.")
                print("Packet from Client: " + message['message'] + ", Type: " + message['msgType'] + ", Number: " + str(message['number']) + ", SerialNumber: " + str(message['sno']))
                ackpacket = ReliableUDPMessage("Acknowledgement", 'ack', message['number'], message['sno'])
                ackpacket = ackpacket.serialize()
                bytesToSend = json.dumps(ackpacket).encode('utf-8')
                self.socket.sendto(bytesToSend, return_address)
                print("Ack Sent")
                
                

            else:
                print("Received Message Packet was corrupt.")
                receive()