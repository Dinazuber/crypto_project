from Client import Client
import threading

def main():
    print("Hello from crypto-project! tester omg")
    client = Client()
    client.connect("vlbelintrocrypto.hevs.ch", 6000)
    client.send("Hello", 't')
    client.close()

    recv_msg = threading.Thread(target=client.receive())
    recv_msg.start()


if __name__ == "__main__":
    main()
