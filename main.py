from Client import Client
from command import command
import threading
from mainWindow import mainWindow as launch_ui

def main():
    print("Hello from crypto-project!")
    client = Client()
    client.connect("vlbelintrocrypto.hevs.ch", 6000)

    console_reader = command(client)
    mainWindow = launch_ui(client,console_reader)

    #Create a new thread to do async code
    recv_msg = threading.Thread(target=client.receive)
    
    #If we stop the program somewhere else, it also stops here
    recv_msg.daemon = True
    recv_msg.start()

    #We check anytime if a new command is typed by the user
    while True:
        msg = input('>')
        cmd, args = console_reader.parse_console(msg)
        console_reader.execute_cmd(cmd, args)

if __name__ == "__main__":
    main()  