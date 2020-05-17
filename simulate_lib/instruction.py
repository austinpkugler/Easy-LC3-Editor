# variables in Instruction class are based off of this image: https://usermanual.wiki/Pdf/LC320Instructions.144663026-User-Guide-Page-1.png
# instrucions that do not require different parts should have the unrequired parts as ""
class Instruction:
    def __init__(self):
        self.name = ""
        self.DR = ""
        self.SR = ""
        self.SR1 = ""
        self.SR2 = ""
        self.imm5 = ""
        self.PCoffset9 = ""
        self.BaseR = ""
        self.offset6 = ""
