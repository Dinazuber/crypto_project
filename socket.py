import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("vlbelintrocrypto.hevs.ch", 6000))
