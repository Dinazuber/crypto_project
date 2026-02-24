class MessageHandler:
    def __init__(self, byte_per_char=4):
        pass

    def add_data(self, data):
        """Add data recieved from network"""
    
    def get_message(self):
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