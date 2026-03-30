import sys
from collections import Counter
from  sympy import randprime
import random
from hashlib import sha256

class command:
    def __init__(self, client):
        self.client = client

        #List of all the commands
        self.commands = {
            '/help': {
                'action': self.cmd_help,
                'description': 'Affiche toutes les commandes disponibles avec leur description'
            },
            '/t': {
                'action': self.cmd_send_text,
                'description': "Envoie un message (texte) au serveur. Exemple : /t Hello World!"
            },
            '/s': {
                'action': self.cmd_send_server,
                'description': "Envoie un message encrypter. Exemple : /s Hello World!"
            },
            '/shift': {
                'action': self.cmd_shift_message,
                'description': "Fait un shift du message voulu par l'utilisateur avec la clé donner"
            },
            '/deshift': {
                'action': self.cmd_deshift_message,
                'description': "Fait un déshift du message voulu par l'utilisateur"
            },
            '/vigenere': {
                'action': self.cmd_vigenere,
                'description': "Fait un Vigenère du message voulu par l'utilisateur"
            },
            '/devigenere': {
                'action': self.cmd_devigenere,
                'description': "Fait un Vigenère du message voulu par l'utilisateur"
            },
            '/rsakeys': {
                'action': self.cmd_prepareKeys,
                'description': "Prépare une paire de clé RSA"
            },
            '/rsaencrypt': {
                'action': self.cmd_rsa_encrypt,
                'description': "Fait un encryptage en RSA du message voulu par l'utilisateur"
            },
            '/rsadecrypt': {
                'action': self.cmd_rsa_decrypt,
                'description': "Fait un décryptage en RSA du message voulu par l'utilisateur"
            },
            '/hash': {
                'action': self.cmd_hash,
                'description': "Fait un hashing du message voulu par l'utilisateur"
            },
            '/key': {
                'action': self.cmd_key,
                'description': "Assigne et envoie au serveur une clé. Exemple : /key 1234"
            },
            '/quit': {
                'action': self.cmd_quit,
                'description': "Quitte l'application"
            }
        }
    
    #Print all the possible commands
    def cmd_help(self, args=None):
        print("Commandes disponibles : ")
        for name, infos in self.commands.items():
            print(f"{name} : {infos['description']}")  
        print("-----")
    
    #Send a simple message (a broadcast -> /t) to the server
    def cmd_send_text(self, args):
        if args:
            #We have to create a join because we created a table of our words. and now we need to group them
            self.client.send(" ".join(args), 't')
        else:
            print("Error : the message is empty")
        

    #Send a message only to the server, to execute task
    def cmd_send_server(self, message):
        if message:
            #We have to create a join because we created a table of our words. and now we need to group them
            self.client.send(" ".join(message), 's')
        else:
            print("Error : the message is empty")

    #Execute the shift of "key" int of the message and send it to the server
    def cmd_shift_message(self, message, key):
        try:
            key_nb = int(key)
        except ValueError:
            print("Error: the key must be a number")
            return 
        if message:
            result = ''
            for c in message:
                result += chr((ord(c) + key_nb))
            self.client.send(result, 's')
            print(f"Sending the result \"{result}\" to the server")
        else:
            print("Error: need a message to shift")

    #TODO Finish to complete this method     
    def cmd_deshift_message(self, cipher):
        if not cipher: 
            return "Must have a message to decrypt"
        
        #We're gonna count how many times each charater appearse
        counts_nbLetter = Counter(cipher)
        #Keep only the letter the most used, and not the nb of times
        common_items = counts_nbLetter.most_common(2)
        most_frequent_letter, _ = common_items[0]

        if most_frequent_letter == '*':
            most_frequent_letter, _ = common_items[1]
            print(most_frequent_letter)
        else:
            print(most_frequent_letter)
        
        #Now, we're testing the must used number - the most used letter in general ("e")
        if ord(most_frequent_letter) < ord('e'):
            probable_key = ord('e') - ord(most_frequent_letter)
        else :
            probable_key = ord(most_frequent_letter) - ord('e')

        result = ""
        for c in cipher:
            result += chr(ord(c) - probable_key)
        
        print(f"The probably key is : {probable_key}\nAnd the probable message is {result}")

        
    #Do the vigenere algo to the message with the key and send it to the server
    def cmd_vigenere(self, message, key):
        if message:
            result = ""
            for i, c in enumerate(message):
                key_c = key[i%len(key)]
                new_c = chr(ord(c) + ord(key_c))
                result += new_c
            self.client.send(result, 's')
            print(f"Sending the result \"{result}\" to the server")
        else:
            print("Error : you must have a message and a key!")

    #TODO Finish to implement the devigenere
    def cmd_devigenere(self, message, key):
        if message:
            result = ""
            for i, c in enumerate(message):
                key_c = key[i%len(key)]
                new_c = chr(ord(c) - ord(key_c))
                result += new_c
            print(result)
        else :
            print("Error : must have a message and a key!")

    def cmd_rsa_encrypt(self,message, n=None, e_key=None):
        if n is None or e_key is None:
            print("Erreur : Cette fonction nécessite les arguments N et E.")
            return

        try:
            N = int(n)
            e = int(e_key)
        except ValueError:
            print("Erreur : N et E doivent être des entiers.")
            return

        if not message:
            print("Erreur : Message vide.")
            return

        # 2. Chiffrement
        encrypted_blocks = []
    
        for char in message:
            # UTILISATION DE POW(a, b, mod) - Indispensable !
            encrypted_blocks += str((int(char) ** e) % N).zfill(2)

        # 3. Formatage de la réponse
        # On sépare les nombres par un espace pour que le serveur puisse les distinguer
        result = " ".join(encrypted_blocks)

        print(f"Envoi du message chiffré : {result}")
        self.client.send(result, 's')

    def cmd_rsa_decrypt(self,message, n=None, d_key=None):
        if n is None or d_key is None:
            print("Erreur : Cette fonction nécessite les arguments N et d.")
            return

        try:
            N = int(n)
            d = int(d_key)
        except ValueError:
            print("Erreur : N et d doivent être des entiers.")
            return

        if not message:
            print("Erreur : Message vide.")
            return

        # 2. Chiffrement
        encrypted_blocks = message.split()
        plaintext = []

        for char in encrypted_blocks:
            decrypted_char = pow(int(char), d, N)
            try:
                plaintext.append(chr(decrypted_char).zfill(2))
            except ValueError:
                plaintext.append(f"[{decrypted_char}]")

        # 3. Formatage de la réponse
        # On sépare les nombres par un espace pour que le serveur puisse les distinguer
        result = " ".join(plaintext)
        print(result)

    #Find the mutiple
    def gcd(self, a, b):
        if(b == 0):
            return abs(a)
        else:
            return self.gcd(b, a % b)

    def cmd_prepareKeys(self):
        #Get prime numbers
        p = randprime(100, 100000)
        q = randprime(1000, 1000000)

        #Check that p != q
        while(p == q):
            q = randprime(1000, 1000000)

        #Modular
        N = p * q

        #Modular for private key
        N0 = (p-1)*(q-1)

        #Get e for public key
        start = random.randint(10000, 100000)
        for i in range(start, N0):
            if self.gcd(i, N0) == 1:
                e = i
                break
        
        try:
            d = pow(e, -1, N0)
        except ValueError:
            print("Error: e is not inversible")
            return
        
        print(f"Voici la clé : N={N}\ne={e}\nd={d}")
    
    #Send the key founded to the server
    def cmd_key(self, args):
        if args:
            value = args[0]
            print(f"Sending key : {value}")
            self.client.send(value, 'k')
        else:
            print("Error : Please send a correct key")

    def cmd_hash(self, message):
        result = sha256(message.encode('utf-8')).hexdigest()
        print(f"Sended : {result}")
        self.client.send(result, 's')
        
    #Disconnect and close the program
    def cmd_quit(self):
        print("Disconnecting from the server...")
        self.client.close()
        sys.exit(0)
    
    #Parse the console
    def parse_console(self, input):
        if not input.strip():
            return None, None
        
        args = input.split(' ')
        cmd = args[0]

        if input.startswith('/'):
            return (cmd, args[1:])
        
        return(cmd, args)
    
    def execute_cmd(self, cmd, args):
        if cmd is None:
            return
        
        if cmd.startswith('/'):
            if cmd in self.commands:
                action = self.commands[cmd]['action']
                if cmd == '/shift' or cmd == "/vigenere" or cmd=="/devigenere":
                    if len(args) < 2:
                        print("Error : The command /shift needs a key and a message")
                        print("Example : /shift 5 Hello world!")
                        return
                    key = args[0]
                    message = " ".join(args[1:])
                    action(message, key)

                elif cmd == "/deshift" or cmd == "/hash":
                    message = " ".join(args)
                    action(message)
                elif cmd == "/rsaencrypt" or cmd == "/rsadecrypt":
                    n = args[0]
                    e = args[1] #Becomes D if it's decrypt
                    message = " ".join(args[2:])
                    action(message, n, e)
                elif cmd == "/rsakeys":
                    action()
                else :
                    action(args)
            else:
                print(f"Unkown command : {cmd}.\nType /help to see the list of command")

        else:
            message = cmd + " " + " ".join(args) if args else cmd
            self.client.send(message, 't')