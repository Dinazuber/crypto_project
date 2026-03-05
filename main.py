from Client import Client
from command import command
import threading

def main():
    print("Hello from crypto-project!")
    client = Client()
    client.connect("vlbelintrocrypto.hevs.ch", 6000)
    
    console_reader = command(client)

    recv_msg = threading.Thread(target=client.receive)
    recv_msg.daemon = True
    recv_msg.start()

    while True:
        msg = input('>')
        cmd, args = console_reader.parse_console(msg)
        console_reader.execute_cmd(cmd, args)

if __name__ == "__main__":
    main()
