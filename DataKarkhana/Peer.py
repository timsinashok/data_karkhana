import socket
import os

class FileTransferHandler:
    def __init__(self, peer_id, host, port, tracker_host, tracker_port):
        self.peer_id = peer_id
        self.host = host
        self.port = port
        self.tracker_host = tracker_host
        self.tracker_port = tracker_port

    def connect_and_receive_response(self):
        try:
            # Construct registration message
            message = f"REGISTER {self.peer_id} {self.host} {self.port}"
            # Connect to the tracker and register
            tracker_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            tracker_socket.connect((self.tracker_host, self.tracker_port))
            tracker_socket.sendall(message.encode())
            tracker_socket.close()

            # Start broadcasting
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.bind((self.host, self.port))
            server_socket.listen(1)
            print(f"Broadcasting on {self.host}:{self.port}")

            # Start listening for connections
            while True:
                try:
                    # Accept incoming connection
                    print("Waiting for connection...")
                    client_socket, client_address = server_socket.accept()
                    print(f"Connection accepted from {client_address}")

                    # Receive message from connected client
                    request_data = client_socket.recv(1024).decode()

                    # Don't close socket here
                    # client_socket.close()

                    print("Request data:", request_data)

                    # Parse the request data
                    request_parts = request_data.split()
                    if len(request_parts) >= 2:
                        if request_parts[0] == "REQUEST_DATA":
                            peer_ip = request_parts[1]
                            peer_port = int(request_parts[2])
                            filename = request_parts[3]
                            print(f"Peer IP: {peer_ip}, Port: {peer_port}, Filename: {filename}")

                            # Request file from peer
                            self.request_file_from_peer(peer_ip, peer_port, filename)
                        elif request_parts[0] == "SEND_DATA":
                            filename = request_parts[1]
                            self.send_file_to_peer(client_socket, filename)

                        else:
                            print("Invalid request format:", request_data)
                    else:
                        print("Invalid request format:", request_data)
                    client_socket.close()

                except Exception as e:
                    print("An error occurred while handling client connection:", e)

        except Exception as e:
            print("An error occurred:", e)

    def request_file_from_peer(self, peer_ip, peer_port, filename):
        try:
            # Connect to the peer
            peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            peer_socket.connect((peer_ip, peer_port))

            # Send the filename and your port number
            request_message = f"SEND_DATA {filename}"
            peer_socket.sendall(request_message.encode())

            # Receive and save the file
            with open(os.path.join("downloads", filename), 'wb') as f:
                while True:
                    chunk = peer_socket.recv(1024)
                    if not chunk:
                        break
                    f.write(chunk)

            peer_socket.close()
            print(f"File '{filename}' downloaded from peer {peer_ip}:{peer_port}")

        except Exception as e:
            print(f"An error occurred while downloading file '{filename}' from peer {peer_ip}:{peer_port}:", e)

    def send_file_to_peer(self, peer_socket, filename):
        try:
            with open(os.path.join("downloads", filename), 'rb') as file:
                file_data = file.read()
                peer_socket.sendall(file_data)
        except FileNotFoundError:
            peer_socket.sendall(b"File not found")

