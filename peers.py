import socket
import os

class Peer:
    def __init__(self, ip, port, mode='receiver'):
        self.ip = ip
        self.port = port
        self.mode = mode

    def toggle_mode(self):
        self.mode = 'sender' if self.mode == 'receiver' else 'receiver'
        print(f"Mode toggled. Now in {self.mode} mode.")

    def receive_file_from_server(self, server_ip, server_port, filename):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((server_ip, server_port))
            print(f"Connected to {server_ip}:{server_port}")

            # Send filename request to server
            s.sendall(filename.encode())

            response = s.recv(1024).decode()

            if response == 'OK':
                with open(filename, 'wb') as file:
                    while True:
                        data = s.recv(1024)
                        if not data:
                            break
                        file.write(data)

                print(f"File '{filename}' received from {server_ip}:{server_port}")
            else:
                print(f"Error: {response}")

    def send_file_to_server(self, server_ip, server_port, filename):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.ip, self.port))
            s.listen()
            print(f"Server listening on {self.ip}:{self.port}")

            conn, addr = s.accept()
            print(f"Connected to by {addr}")

            # Receive filename request from client
            filename_request = conn.recv(1024).decode()

            if os.path.exists(filename_request):
                conn.sendall(b"OK")

                with open(filename_request, 'rb') as file:
                    while True:
                        data = file.read(1024)
                        if not data:
                            break
                        conn.sendall(data)

                print(f"File '{filename_request}' sent to {addr}")
            else:
                conn.sendall(b"File not found")
                print("Requested file does not exist")

    def perform_action(self, server_ip, server_port, filename):
        if self.mode == 'receiver':
            self.receive_file_from_server(server_ip, server_port, filename)
        elif self.mode == 'sender':
            self.send_file_to_server(server_ip, server_port, filename)
        else:
            print("Invalid mode. Please set mode as 'sender' or 'receiver'.")

# Example usage
peer = Peer("0.0.0.0", 12345, mode='receiver')

# Toggle mode
peer.toggle_mode()

# List of server IPs and ports
servers = [
    ("192.168.1.100", 8080),
    ("192.168.1.101", 8080)
]

# List of filenames to interact with each server
filenames = ["file_from_server1.txt", "file_from_server2.txt"]

# Perform action (send or receive) based on the current mode
for i, (server_ip, server_port) in enumerate(servers):
    if i < len(filenames):
        filename = filenames[i]
    else:
        filename = input("Enter filename: ")

    peer.perform_action(server_ip, server_port, filename)
