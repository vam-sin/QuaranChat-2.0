import argparse
import sys
import time
from reliable_socket import ReliableUDPSocket

# Throughput Calcualtions
start = time.time()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Test out file transfer using ReliableUDPSocket.')
    parser.add_argument('mode', help='use as server/client')
    parser.add_argument('file', help='file to transfer/location to save')
    args = parser.parse_args()
    file_transfer_socket = ReliableUDPSocket()
    serverAddressPort = ("127.0.0.1", 20001)
    packet_count = 0
    if args.mode == 'client':
        with open(args.file, 'rb') as disk_file:
            data = disk_file.read()
        while(len(data) != 0):
            data_packet = data[0:64]
            file_transfer_socket.send(data_packet, serverAddressPort)
            packet_count += 1
            del data[0:64]
        print("Successfully transmitted file in ", packet_count, "packet transfers.")
    elif args.mode == 'server':
        file_transfer_socket.bind(serverAddressPort)
        print("[SERVER] Awaiting file upload..")
        while(True):
            received_packet, address = file_transfer_socket.receive()
            packet_count += 1
            with open(args.file, "ab") as recv_file:
                if len(received_packet['message']) == 0:
                    print("Complete file received in ", packet_count, "packet transfers.")
                    break
                else:
                    recv_file.write(received_packet['message'])
    else:
        print("Mode ", args.mode, " is undefined.")
        exit(0)