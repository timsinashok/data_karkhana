import socket
import os

class uploader:
    def __init__(self):
        pass

    def send_file_chunk(self, file_name, client_socket):
        chunk_size = 1024
        file_path = f"downloads/{file_name}"
        with open(file_path, 'rb') as file:
            while True:
                chunk = file.read(chunk_size)
                if not chunk:
                    break
                client_socket.send(chunk)
        print(f"File {file_name} sent to peer")

    def request_file_from_peer(self, peer_ip, peer_port, filename):
        try:
            peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            peer_socket.connect((peer_ip, peer_port))

            request_message = f"SEND_DATA {filename}"
            peer_socket.sendall(request_message.encode())

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
            file_path = f"downloads/{filename}"
            with open(file_path, 'rb') as file:
                file_data = file.read()
                peer_socket.sendall(file_data)
        except FileNotFoundError:
            peer_socket.sendall(b"File not found")

    def divide_file_into_chunks(self, file_path, num_chunks):
        chunks = []
        dest_path = 'downloads'
        file_size = os.path.getsize(file_path)
        chunk_size = int(file_size / num_chunks) + 1
        with open(file_path, 'rb') as file:
            index = 0
            while True:
                chunk = file.read(chunk_size)
                if not chunk:
                    break
                chunks.append((index, chunk))
                index += 1
        if not os.path.exists(dest_path):
            os.makedirs(dest_path)
        
        filename = os.path.splitext(file_path)[0]
        print(filename)

        for index, chunk in chunks:
            with open(os.path.join(dest_path, f"{filename}_{index}.txt"), 'wb') as chunk_file:
                chunk_file.write(chunk)

    def send_file(self, peer_id, host, port, tracker_host, tracker_port, file_path = "test.txt"):
        file_name = os.path.basename(file_path)
        tracker_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tracker_socket.connect((tracker_host, tracker_port))
        message = f"REGISTER {peer_id} {host} {port}"
        tracker_socket.sendall(message.encode())
        tracker_socket.close()

        tracker_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tracker_socket.connect((tracker_host, tracker_port))
        message = f"SHARE {file_name} {peer_id} {host} {port}"
        tracker_socket.sendall(message.encode())

        print(f"File {file_name} uploaded to tracker")

        while True:
            response = tracker_socket.recv(1024).decode()
            if response:
                break
        print("response from tracker = ", response)

        parts = response.split()
        num_chunks = parts[1]

        print(num_chunks)

        self.divide_file_into_chunks(file_name, int(num_chunks))
        tracker_socket.close()

        sender_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sender_socket.bind((host, port))
        sender_socket.listen(5)
        
        for i in range(int(num_chunks)-1):
            print(f"starting send{i}")
            
            while True:        
                client_socket, client_address = sender_socket.accept()
                print(f"connection accepted from {client_address}")
                response = client_socket.recv(1024).decode()
                if response:
                    break
            print("response from peer =", response)
            send_attributes = response.split()
            self.send_file_chunk(send_attributes[1], client_socket)
            client_socket.close()
        sender_socket.close()

    def connect_and_receive_response(self, peer_id, host, port, tracker_host, tracker_port):
        try:
            message = f"REGISTER {peer_id} {host} {port}"
            tracker_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            tracker_socket.connect((tracker_host, tracker_port))
            tracker_socket.sendall(message.encode())
            tracker_socket.close()

            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.bind((host, port))
            server_socket.listen(1)
            print(f"Broadcasting on {host}:{port}")

            while True:
                try:
                    print("Waiting for connection...")
                    client_socket, client_address = server_socket.accept()
                    print(f"Connection accepted from {client_address}")

                    request_data = client_socket.recv(1024).decode()
                    print("Request data:", request_data)

                    request_parts = request_data.split()
                    if len(request_parts) >= 2:
                        if request_parts[0] == "REQUEST_DATA":
                            peer_ip = request_parts[1]
                            peer_port = int(request_parts[2])
                            filename = request_parts[3]
                            print(f"Peer IP: {peer_ip}, Port: {peer_port}, Filename: {filename}")
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


