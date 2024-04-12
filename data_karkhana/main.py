import sys
from Users import Tracker
from Users import Peer
from Users import Uploader
from Users import Downloader
import socket

def main():
    print("Choose a role:")
    print("1. Tracker")
    print("2. Uploader")
    print("3. Downloader")
    print("4. Normal Peer")

    role_choice = input("Enter your choice (1/2/3/4): ")

 

    if len(sys.argv) >= 3:
        tracker_host = sys.argv[1]
        tracker_port = int(sys.argv[2])
    else:
        tracker_host = input("Please input the tracker IP address: ")
        tracker_port = int(input("Please input the tracker port number: "))

    if role_choice == "1":
        tracker = Tracker.Tracker(tracker_host, tracker_port)
        tracker.start()

    elif role_choice == "2":
        alice_instance = Uploader.uploader()

        # host = input("Please input your IP address properly: ")  # Replace with the actual IP address of the receiver machine
        # port = int(input("Please enter your port number: "))

        host = get_ip()
        port = 12345
        file_path = input("Enter the name of the file you want to upload (for default, type: test.txt): ")
        peer_id = input("Enter your peer ID: ")
        alice_instance.send_file( peer_id, host, port, tracker_host, tracker_port, file_path)
        alice_instance.connect_and_receive_response(peer_id, host, port+1, tracker_host, tracker_port)

    elif role_choice == "3":

        host = get_ip()
        port = 12345

        # host = input("Please input your IP address properly: ")  # Replace with the actual IP address of the receiver machine
        # port = int(input("Please enter your port number: "))
        peer_id = input("Enter your peer ID (any string to recognize you over network): ")
        downloader = Downloader.Downloader(peer_id, host, port, tracker_host, tracker_port)
        downloader.connect_and_receive_response()

    elif role_choice == "4":

        host = get_ip()
        port = 12345

        # host = input("Please input your IP address properly: ")  # Replace with the actual IP address of the receiver machine
        # port = int(input("Please enter your port number: "))
        peer_id = input("Enter your peer ID (any string to recognize you over network): ")
        file_handler = Peer.FileTransferHandler(peer_id, host, port, tracker_host, tracker_port)
        file_handler.connect_and_receive_response()

    else:
        print("Invalid choice. Please choose a valid option.")

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 1))  # connect() for UDP doesn't send packets
    return s.getsockname()[0]

if __name__ == "__main__":
    main()
