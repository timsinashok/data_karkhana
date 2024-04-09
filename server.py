import socket
import os

def send_file(ip, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((ip, port))
        s.listen()
        print(f"Server listening on {ip}:{port}")

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

# Server 1 IP and port
server1_ip = "192.168.1.100"
server1_port = 8080

# Start Server 1
send_file(server1_ip, server1_port)