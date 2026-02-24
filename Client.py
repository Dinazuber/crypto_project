import socket 

class Client:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    def __init__(self, bytes_per_char = 4):
        pass

    def connect(self, IP_address, port):
        self.client_socket.connect(("vlbelintrocrypto.hevs.ch", 6000))
    
    def send(self, message):
        self.client_socket.send(message.encode())
    
    def receive(self):
        while True:
            data = self.client_socket.recv()
            
    
    def close(self):
        self.client_socket.close
    