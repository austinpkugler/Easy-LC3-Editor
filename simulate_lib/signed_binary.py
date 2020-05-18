
#accepts a sign-padded binary string, and converts it to a signed binary value
class SignedBinary:
    def __init__(self, string=""):
        self.str = string
    def to_integer(self):
        return int(self.str)