import socket
import os

class Peer:
    def __init__(self, ip, port, mode='receiver'):
        self.ip = ip
        self.port = port
        self._mode = mode

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, new_mode):
        if new_mode not in ('sender', 'receiver'):
            raise ValueError("Mode must be 'sender' or 'receiver'")
        self._mode = new_mode
        print(f"Mode changed. Now in {self.mode} mode.")

    def receive_file(self, filename):
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

    def send_file(self, server_ip, server_port, filename):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((server_ip, server_port))
            print(f"Connected to {server_ip}:{server_port}")

            # Send filename request to server
            s.sendall(filename.encode())

            response = s.recv(1024).decode()

            if response == 'OK':
                with open(filename, 'rb') as file:
                    while True:
                        data = file.read(1024)
                        if not data:
                            break
                        s.sendall(data)

                print(f"File '{filename}' sent to {server_ip}:{server_port}")
            else:
                print(f"Error: {response}")

# Example usage
peer = Peer("0.0.0.0", 12345, mode='receiver')

# Change mode
peer.mode = 'sender'

# If in receiver mode, receive file from another peer acting as a server
if peer.mode == 'receiver':
    peer.receive_file("received_file.txt")
# If in sender mode, send file to another peer acting as a client
else:
    peer.send_file("192.168.1.100", 8080, "file_to_send.txt")
