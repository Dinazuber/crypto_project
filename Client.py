import socket 
import sys #to print stuff
from MessageHandler import MessageHandler

class Client:
    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.message_handler = MessageHandler()

    def connect(self, IP_address, port):
        try:
            self.client_socket.connect((IP_address, port))
        except Exception as e:
            print(f"Error : {e}")
        
    
    def send(self, message, cmd):
        self.client_socket.send(self.message_handler.encode_message(cmd, message))

    def _recvall(self, n):
        data = bytearray()
        while len(data) < n:
            packet = self.client_socket.recv(n-len(data))
            if not packet:
                return None
            data.extend(packet)
        return bytes(data)
    
    def receive(self):
        while True:
            header_data = self.client_socket.recvall(6)
            #We check if we have our 6 first bytes
            if not header_data:
                break #if not, we end our action

            #We get our payload size and convert into Int
            length = int.from_bytes(header_data[4:6], 'big')

            payload_size = length * 4 #we convert our length into bytes

            payload_data = b''
            if payload_size > 0:
                #if we got something in the payload (like a message)
                payload_data = self.client_socket.recvall(payload_size)
                if not payload_data:
                    break #if we got nothing into our message

            full_packet = header_data + payload_data

            #We show our message
            sys.stdout.write('\r\033[K')

            header, cmd, length, message = self.message_handler.decode_message(full_packet)

            print(f"[{cmd}] Server : {message}")

            sys.stdout.write(">")
            sys.stdout.flush()

    
    def close(self):
        self.client_socket.close
    