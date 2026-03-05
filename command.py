import sys

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
    def cmd_deshift_message(self, message, key):
        try:
            key_nb = int(key)
        except ValueError:
            print("Error: the key must be a number")
            return 
        if message:
            result = ''
            for c in message:
                if c.islower() :
                    result += chr((ord(c) - ord('a')-key_nb) % 26 + ord('a'))
                elif c.isupper() :
                    result+= chr((ord(c) - ord('A')-key_nb) % 26 + ord('A'))
                else:
                    result+=c
            print(result)
        else:
            print("Error: need a message to shift")

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
    
    #Send the key founded to the server
    def cmd_key(self, args):
        if args:
            value = args[0]
            print(f"Sending key : {value}")
            self.client.send(value, 'k')
        else:
            print("Error : Please send a correct key")
        
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
                if cmd == '/shift' or cmd == "/deshift" or cmd == "/vigenere" or cmd=="/devigenere":
                    if len(args) < 2:
                        print("Error : The command /shift needs a key and a message")
                        print("Example : /shift 5 Hello world!")
                        return
                    key = args[0]
                    message = " ".join(args[1:])
                    action(message, key)
                else :
                    action(args)
            else:
                print(f"Unkown command : {cmd}.\nType /help to see the list of command")

        else:
            message = cmd + " " + " ".join(args) if args else cmd
            self.client.send(message, 't')
