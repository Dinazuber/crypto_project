from Client import Client
from command import command
from mainWindow import mainWindow as launch_ui

def main():
    print("Hello from crypto-project!")
    client = Client()
    client.connect("vlbelintrocrypto.hevs.ch", 6000)

    console_reader = command(client)
    mainWindow = launch_ui(client,console_reader)

if __name__ == "__main__":
    main()  