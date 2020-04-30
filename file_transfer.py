import argparse
import sys
import time
from reliable_socket import ReliableUDPSocket
import os

def transfer_file(mode, file):
    file_transfer_socket = ReliableUDPSocket()
    serverAddressPort = ("127.0.0.1", 20001)
    packet_count = 0
    if mode == 'client':
        with open(file, 'r') as disk_file:
            data = disk_file.read()
        start_time = time.time()
        while(len(data) != 0):
            data_packet = data[0:64]
            file_transfer_socket.send(data_packet, serverAddressPort)
            packet_count += 1
            data = data[64:]
        file_transfer_socket.send("", serverAddressPort)
        print("Successfully transmitted file in ", packet_count, "packet transfers.")
    elif mode == 'server':
        transfer_started = False
        file_transfer_socket.bind(serverAddressPort)
        print("[SERVER] Awaiting file upload..")
        while(True):
            received_packet, address = file_transfer_socket.receive()
            if not transfer_started:
                start_time = time.time()
                transfer_started = True
            packet_count += 1
            with open(file, "a") as recv_file:
                if len(received_packet['message']) == 0:
                    print("Complete file received in ", packet_count, "packet transfers.")
                    # break
                else:
                    recv_file.write(received_packet['message'])
    else:
        print("Mode ", mode, " is undefined.")
        exit(0)
    end_time = time.time()
    duration = end_time - start_time
    file_size = os.path.getsize(file)
    print("File size (bytes): %f" % file_size)
    print("DURATION: ", duration)
    return duration, file_size