class FrameManager:
    #We need all the informations to create our packet to send to the server
    def __init__(self, header, cmd='t', payload=''):
        self.header = header
        self.cmd = cmd
        self.payload = payload
        self.length = len(payload)
    
    #Create the packet to send to the server
    def create_packet(self, cmd_bytes, length_bytes, message_bytes):
        #Encode the header part (to be ready to send it to the server) for each character
        header_bytes = self.header.encode('ascii')
        return header_bytes + cmd_bytes + length_bytes + message_bytes
    
    #Undo the paquet to get cleared infos from the server
    def undo_packet(packet):
        #We retrieve the first 3 bytes of our responses (so from 0 --> 3 not included)
        header = packet[0:3].decode('ascii')
        #Get the bytes for the CMD
        cmd = packet[3:4].decode('ascii')
        #Get the bytes for the length of the payload (we take also the strong bits)
        length = int.from_bytes(packet[4:6], 'big')
        #Get the bytes from the payload (we multiplie by 4 to convert to bytes)
        payload = packet[6:6+length*4]

        return (header, cmd, length, payload)
    
    def __str__(self):
        return f"Frame : header={self.header}, cmd={self.cmd}, length={self.length}, payload={self.payload}"
