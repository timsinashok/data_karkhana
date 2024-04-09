import socket

def receive_file(ip, port, filename):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((ip, port))
        print(f"Connected to {ip}:{port}")

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

            print(f"File '{filename}' received from {ip}:{port}")
        else:
            print(f"Error: {response}")

# List of server IPs and ports
servers = [
    ("192.168.1.100", 8080),
    ("192.168.1.101", 8080)
]


# Receive files from each server
for i, (server_ip, server_port) in enumerate(servers):
    filename = input("Enter filename:")
    receive_file(server_ip, server_port, filename)