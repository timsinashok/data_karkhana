import socket
import os
import ast


class Downloader:
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

            # Get available files
            tracker_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            tracker_socket.connect((self.tracker_host, self.tracker_port))
            message = "LIST"
            tracker_socket.sendall(message.encode())
            response = tracker_socket.recv(1024).decode()
            tracker_socket.close()

            # Present file options to the user
            print("Available files:", response)

            # Ask user to choose a file
            chosen_file = input("Choose a file that you want to download: ")

            # Get peers for the file
            tracker_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            tracker_socket.connect((self.tracker_host, self.tracker_port))
            message = f"LOOKUP {chosen_file}"
            tracker_socket.sendall(message.encode())
            response = tracker_socket.recv(1024).decode()
            tracker_socket.close()
            print("Response from tracker:", response)

            # Parse the response
            if response.startswith("PEERS"):
                # Split the message by "PEER" and get the second part
                start_index = response.find("PEERS") + len("PEERS")
                dictionary_str = response[start_index:].strip()
                peers = ast.literal_eval(dictionary_str)

                # Ensure values are lists
                for key, value in peers.items():
                    if not isinstance(value, list):
                        peers[key] = [value]

                print("dict = ", peers)
                for key, value in peers.items():
                    self.download_file_from_peers((value[0], value[1]), key)

                self.compile_files("downloads", chosen_file)

            else:
                print("File not found in the response from the connected client:", response)

        except Exception as e:
            print("An error occurred:", e)

    @staticmethod
    def compile_files(directory, filename):
        # List all files in the directory
        files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

        # Sort files by their numerical suffix
        files.sort(key=lambda x: int(x.split('_')[-1].split('.')[0]))

        # Compile files in order
        compiled_content = ''
        print("Alredy arrived here")
        for file in files:
            with open(os.path.join(directory, file), 'r') as f:
                compiled_content += f.read()
        print("Compiled_content is: ", compiled_content)

        # Write compiled content to the specified filename
        with open(os.path.join(directory, filename), 'w') as f:
            print("Writing to file")
            f.write(compiled_content)
            print("Written to file")

        print(f"FILE {filename} is compiled and is ready for usage")

    @staticmethod
    def download_file_from_peers(peers, filename):
        os.makedirs("downloads", exist_ok=True)
        peer_host, peer_port = peers
        print("Trying to connect to", peer_host, peer_port)
        peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        peer_socket.connect((peer_host, peer_port))
        request_message = f"SEND_DATA {filename} "
        peer_socket.sendall(request_message.encode())

        with open(os.path.join("downloads", filename), 'wb') as f:
            while True:
                chunk = peer_socket.recv(1024)
                if not chunk:
                    break
                f.write(chunk)
            peer_socket.close()
        print(f"File '{filename}' downloaded from peer {peer_host}:{peer_port}")


if __name__ == "__main__":
    peer_id = "receiver3"
    host = "172.20.10.5"  # Replace with the actual IP address of the receiver machine
    port = 12345
    tracker_host = "172.20.10.5"  # Replace with the actual IP address of the tracker machine
    tracker_port = 12346
    downloader = Downloader(peer_id, host, port, tracker_host, tracker_port)
    downloader.connect_and_receive_response()
