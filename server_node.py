import socket
import threading
import sys
import logging

class NodeServer:
    def __init__(self, host, port, services):
        self.host = host
        self.port = port
        self.services = services
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.neighbors = []
        self.is_running = False

    def start_server(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.is_running = True
        print(f"Server started on {self.host}:{self.port}")
        try:
            while self.is_running:
                client_socket, client_address = self.server_socket.accept()
                print(f"Connection from {client_address}")
                threading.Thread(target=self.handle_client, args=(client_socket,)).start()
        except Exception as e:
            print(f"Error: {e}")
        finally:
            self.server_socket.close()

    def handle_client(self, client_socket):
        while True:
            try:
                data = client_socket.recv(1024).decode()
                if data:
                    response = self.process_command(data)
                    client_socket.send(response.encode())
                else:
                    break
            except Exception as e:
                print(f"Error: {e}")
                break
        client_socket.close()

    def process_command(self, command):
        try:
            if command.startswith("start"):
                service = command.split()[1]
                if service in self.services and not self.services[service]:
                    self.services[service] = True
                    return f"Service {service} started"
                else:
                    return f"Service {service} is already running or not found"
            elif command.startswith("stop"):
                service = command.split()[1]
                if service in self.services and self.services[service]:
                    self.services[service] = False
                    return f"Service {service} stopped"
                else:
                    return f"Service {service} is already stopped or not found"
            elif command == "status":
                return str(self.services)
            else:
                return "Invalid command"
        except Exception as e:
            return f"Error processing command: {e}"

    def add_neighbors(self, neighbors):
        self.neighbors = neighbors

    def stop_server(self):
        self.is_running = False
        self.server_socket.close()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python server_node.py <port>")
        sys.exit(1)

    port = int(sys.argv[1])
    services = {"service1": False, "service2": False, "service3": False}
    server = NodeServer("127.0.0.1", port, services)
    server.add_neighbors([("127.0.0.1", 65433)])
    try:
        server.start_server()
    except KeyboardInterrupt:
        server.stop_server()
        print("Server stopped.")
