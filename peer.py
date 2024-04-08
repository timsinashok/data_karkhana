import os

class Peer:
    def __init__(self, name, ip_address, port, status='U'):
        self.name = name
        self.ip_address = ip_address
        self.port = port
        self.files = []
        self.status = 'U'
    
    # function to divide a file into indexed chunks
    def chunker(file_path, chunk_size):
        with open(file_path, 'rb') as file:
            chunk_index = 0
            while True:
                chunk = file.read(chunk_size)
                if not chunk:
                    break
                chunk_filename = f"{file_path}.chunk{chunk_index}"
                with open(chunk_filename, 'wb') as chunk_file:
                    chunk_file.write(chunk)
                chunk_index += 1

    # function to merge chunks into a file
    def unchunker(file_path):
        chunk_index = 0
        with open(file_path, 'wb') as file:
            while True:
                chunk_filename = f"{file_path}.chunk{chunk_index}"
                if not os.path.exists(chunk_filename):
                    break
                with open(chunk_filename, 'rb') as chunk_file:
                    file.write(chunk_file.read())
                os.remove(chunk_filename)
                chunk_index += 1

    # function to send a file to a peer
    def send_file(self, file_path):
        chunker(file_path, 1024)
        for chunk_file in os.listdir():
            with open(chunk_file, 'rb') as file:
                data = file.read()
                # send data to peer
        os.remove(file_path)

    # function to receive a file from a peer
    def receive_file(self, file_path):
        with open(file_path, 'wb') as file:
            # receive data from peer
            # write data to file
        unchunker(file_path)
        



