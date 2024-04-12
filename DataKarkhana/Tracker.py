import socket
import os

class Tracker:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.tracker_socket = None
        self.peers = {}
        self.files = {}

    def start(self):
        self.tracker_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tracker_socket.bind((self.host, self.port))
        self.tracker_socket.listen(5)
        print(f"Tracker listening on {self.host}:{self.port}")

        while True:
            print("Current peers:", self.peers)
            print("Current files: \n\n", self.files)

            print("Before message received")
            conn, addr = self.tracker_socket.accept()
            print(f"Connection established with {addr}")

            data = conn.recv(1024).decode()
            print(f"Received data: {data}")

            if data.startswith("REGISTER"):
                self._register_peer(data)

            elif data.startswith("SHARE"):
                self._share_file(data, conn)

            elif data.startswith("LOOKUP"):
                self._lookup_file(data, conn)
            
            elif data.startswith("LIST"):
                self._list_files(conn)

            conn.close()

    def _register_peer(self, data):
        parts = data.split()
        peer_id = parts[1]
        ip = parts[2]
        port = int(parts[3])
        self.peers[peer_id] = (ip, port)
        print(f"Registered peer {peer_id} at {ip}:{port}")

    def _share_file(self, data, conn):
        parts = data.split()
        peer_id = parts[2]
        file_name = parts[1]
        sender_ip = parts[3]
        sender_port = int(parts[4])
        self.peers[peer_id] = (sender_ip, sender_port)
        print(f"File {file_name} shared by sender {sender_ip}:{sender_port}")

        num_peers = len(self.peers)
        conn.sendall(f"NUMBER_OF_PEERS {num_peers}".encode())

        file = file_name.split('.')[0]
        extension = file_name.split('.')[1]
        print("The decoded file is,", file)
        self.files[file_name] = {}
        self.files[file_name][file + '_0'+ '.txt'] = [sender_ip, sender_port]

        chunk_number = 1
        for receiver_peer_id, (receiver_ip, receiver_port) in self.peers.items():
            if receiver_ip != sender_ip or receiver_port != sender_port:
                new_file = file + "_" + str(chunk_number) + '.txt'

                request_message = f"REQUEST_DATA {sender_ip} {sender_port} {new_file}"
                print(f"Requesting {receiver_peer_id} to accept {new_file} from {receiver_ip}:{receiver_port}")

                receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                receiver_socket.connect((receiver_ip, receiver_port))
                receiver_socket.sendall(request_message.encode())
                self.files[file_name][file + "_" + str(chunk_number) + '.txt'] = [receiver_ip, receiver_port]
                receiver_socket.close()
                chunk_number += 1
        self.files[file_name][file + "_0." + extension][1] += 1

    def _lookup_file(self, data, conn):
        print("Got lookup request")
        print(data)
        print("Handling lookup request")
        file_name = data.split()[1]
        print(file_name)
        response = f"PEERS {self.files[file_name]}"
        conn.sendall(response.encode())
        print("Sent response")

    def _list_files(self, conn):
        print("Got list request")
        conn.sendall(str(list(self.files.keys())[0]).encode())
        print("Sent files") 

if __name__ == "__main__":
    tracker_host = "172.20.10.5"  # Replace with the actual IP address of the tracker machine
    tracker_port = 12346
    tracker = Tracker(tracker_host, tracker_port)
    tracker.start()
