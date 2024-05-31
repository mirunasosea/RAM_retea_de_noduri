import socket
import time

class NodeClient:
    def __init__(self, server_hosts):
        self.server_hosts = server_hosts
        self.current_server = None
        self.connect_to_neighbor()

    def connect_to_neighbor(self):
        for host, port in self.server_hosts:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((host, port))
                self.current_server = s
                print(f"Connected to {host}:{port}")
                return
            except Exception as e:
                print(f"Failed to connect to {host}:{port}: {e}")
        print("Failed to connect to any neighbor")

    def send_command(self, command):
        if self.current_server:
            try:
                self.current_server.sendall(command.encode())
                response = self.current_server.recv(1024).decode()
                print(f"Response: {response}")
            except Exception as e:
                print(f"Error: {e}")
                self.current_server.close()
                self.connect_to_neighbor()
        else:
            print("No connection to a server")

    def run(self):
        while True:
            command = input("Enter command (start <service>, stop <service>, status): ")
            self.send_command(command)


if __name__ == "__main__":
    neighbors = [("127.0.0.1", 65432), ("127.0.0.1", 65433)]
    client = NodeClient(neighbors)
    try:
        client.run()
    except KeyboardInterrupt:
        print("Client stopped.")
