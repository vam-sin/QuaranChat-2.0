from file_transfer import transfer_file
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Test out file transfer using ReliableUDPSocket.')
    parser.add_argument('mode', help='use as server/client')
    parser.add_argument('file', help='file to transfer/location to save')
    args = parser.parse_args()
    transfer_file(args.mode, args.file)