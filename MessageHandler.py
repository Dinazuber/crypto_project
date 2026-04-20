from FrameManager import FrameManager

class MessageHandler:
    def __init__(self, header='ISC'):
        self.frame = FrameManager(header)

    def add_data(data):
        """Add data recieved from network"""
    
    def get_message():
        """Extract all complete message from buffer.
        Return a list of bytes (raw message)
        """

#
# UTILITY FUNCTIONS
#

    def parse_text_message(message, byte_per_char=4):
        """Extract text from ISC message"""

    def parse_image_message(message):
        """Extract image from ISC message"""

    def encode_message(self, cmd, message):
        #Encode all the parts of the frame

        #Encode the CMD part into 1 byte (so we use ASCII)
        cmd_bytes = cmd.encode('ascii')
        #Encode the message using UTF-32-be

        if isinstance(message, str):
            message_bytes = message.encode('utf-32-be')
        else:
            message_bytes = message
            
        #Encode Length to 2 bytes and we keep only the strong bits
        length_bytes = (len(message_bytes) // 4).to_bytes(2, 'big')

        #We get all those informations into a frame
        frame = self.frame.create_packet(cmd_bytes, length_bytes, message_bytes)
        frame.__str__();

        return frame

    def decode_message(self, packet):
        # We transform the packet sended by the server into readable stuff
        unframe = FrameManager.undo_packet(packet)

        #We get all the different infos into variables
        header = unframe[0]
        cmd = unframe[1]
        length = unframe[2]
        message_bytes = unframe[3]

        #We decode the message with the same utf-32-be //be means we're taking mostly the strong bits
        message = message_bytes.decode('utf-32-be')

        return (header, cmd, length, message)
    
