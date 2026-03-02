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
                'action': self.cmd_send_shift,
                'description': "Envoie une message encrypter avec le code César(shift). Exemple : /s Hello World!"
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
    
    def cmd_help(self, args=None):
        print("Commandes disponibles : ")
        for name, infos in self.commands.items():
            print(f"{name} : {infos['description']}")  
        print("-----")
    
    def cmd_send_text(self, args):
        if args:
            #We have to create a join because we created a table of our words. and now we need to group them
            self.client.send(" ".join(args), 't')
        else:
            print("Error : the message is empty")
        

    def cmd_send_shift(self, args):
        if args:
            #We have to create a join because we created a table of our words. and now we need to group them
            self.client.send(" ".join(args), 's')
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
