from Client import Client

def main():
    print("Hello from crypto-project!")
    client = Client()
    client.connect("vlbelintrocrypto.hevs.ch", 6000)
    client.send("Hello")
    client.close()


if __name__ == "__main__":
    main()
