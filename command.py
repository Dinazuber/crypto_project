import sys

class command:
    def __init__(self, client):
        self.client = client

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
                'action': self.cmd_send_ceasar,
                'description': "Envoie une message encrypter avec le code César. Exemple : /s Hello World!"
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
    
    def cmd_help(self):
        print("\n Commandes disponibles : ")
        for name, infos in self.commands.items():
            print(f"{name} : ${infos['description']}")
        print("-----")
    
    def cmd_send_text(self, args):
        if args:
            self.client.send(args, '/t')
        else:
            print("Error : the message is empty")
        

    def cmd_send_ceasar(self, args):
        if args:
            self.client.send(args, 's')
        else:
            print("Error : the message is empty")
        
    def cmd_key(self, args):
        if args:
            value = args[0]
            print(f"Sending key : {value}")
            self.client.send(value, 'k')
        else:
            print("Error : Please send a correct key")
        
    def cmd_quit(self, args):
        print("Disconnecting from the server...")
        self.client.close()
        sys.exit(0)
    
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
                action(args)
            else:
                print(f"Unkown command : {cmd}.\nType /help to see the list of command")

        else:
            message = cmd + " " + " ".join(args) if args else cmd
            self.client.send(message, 't')
