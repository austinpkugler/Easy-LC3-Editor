from simulate_lib.SignedBinary import SignedBinary
# variables in Instruction class are based off of LC3_instructions_guide.png
# instrucions that do not require different parts should have the unrequired parts as ""
class Instruction:

    def __init__(self):
        self.name = ""
        self.DR = ""
        self.SR = ""
        self.SR1 = ""
        self.SR2 = ""
        self.BaseR = ""
        self.imm5 = SignedBinary()
        self.PCoffset9 = SignedBinary()
        self.PCoffset11 = SignedBinary()
        self.offset6 = SignedBinary()


    def fix_offsets(self):
        for var in ["imm5", "PCoffset9", "offset6"]:
            if self.__dict__[var].str != "":
                if self.__dict__[var].str[0] == "#":
                    self.__dict__[var].str = self.__dict__[var].str[1:]
                elif self.__dict__[var].str[0] == "X":
                    self.__dict__[var].str = str(int(self.__dict__[var].str[1:], 16))
                elif self.__dict__[var].str[0] == "B":
                    self.__dict__[var].str = str(int(self.__dict__[var].str[1:], 2))