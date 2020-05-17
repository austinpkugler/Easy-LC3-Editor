import sys
from instruction import Instruction

class AsmParser:
    def __init__(self):
        self.fileName = sys.argv[-1] # gets filename
        self.register_values = {
            "R0": 0,
            "R1": 0,
            "R2": 0,
            "R3": 0,
            "R4": 0,
            "R5": 0,
            "R6": 0,
            "R7": 0
        }
        self.flag = "0"
        self.memory = list()
        self.populate_addresses()
        self.lines = self.read_in_file()



    def read_in_file(self):
        with open(fileName) as file: #opens file
            lines = file.readlines() #reads in file into lines
        lines = [x.rstrip() for x in lines] # removes \n after each line
        return lines

    def populate_addresses(self):
        for i in range(2**16): # looping through addresses
            self.memory.append("0"*16) #populates memory address with 16 0's

    def instruction_to_bin(self, instruction):
        binary_string = ""

        # converts add and and
        if instruction.name == "ADD":
            binary_string = "0001"
        elif instruction.name == "AND":
            binary_string = "0101"
        if instruction.name == "ADD" or instruction.name == "AND":
            binary_string += f"{int(instruction.DR[1]):b}"
            binary_string += f"{int(instruction.SR1[1]):b}"
            if instruction.SR2 == "": # is immediate add mode
                binary_string += "1"
                binary_string += f"{int(instruction.imm5):b}"
            else:
                binary_string += "000"
                binary_string += f"{int(instruction.SR2[1]):b}"

        # converts all BRs
        elif 'BR' in instruction.name:
            binary_string = "0000"
            if 'N' in instruction.name or instruction.name == 'BR':
                binary_string += '1'
            else:
                binary_string += '0'
            if 'Z' in instruction.name:
                binary_string += '1' 
            else:
                binary_string += '0'
            if 'P' in instruction.name
                binary_string += '1'
            else:
                binary_string += '0'
            binary_string += f"{int(instruction.PCoffset9):b}"
        
        elif 'JMP' == instruction.name:
            binary_string = "1100"
            binary_string += "000"
            binary_string += f"{int(instruction.BaseR[1]):b}"
            binary_string += "000000"
        elif 'JSR' == instruction.name:
            binary_string = "0100"
            binary_string += "1"
            binary_string += f"{int(instruction.PCoffset11):b}"
        elif 'JSRR' == instruction.name:
            binary_string = "0100"
            binary_string += "000"
            binary_string += f"{int(instruction.BaseR[1]):b}"
            binary_string += "000000"
        elif "LD" == instruction.name:
            binary_string == "0010"
            binary_string += f"{int(instruction.DR[1]):b}"
            binary_string += f"{int(instruction.PCoffset9):b}"
        elif "LDI" == instruction.name:
            binary_string = "1010"
            binary_string += f"{int(instruction.DR[1]):b}"
            binary_string += f"{int(instruction.PCoffset9):b}"
        elif "LDR" == instruction.name:
            binary_string = "0110"
            binary_string += f"{int(instruction.DR[1]):b}"
            binary_string += f"{int(instruction.BaseR[1]):b}"
            binary_string += f"{int(instruction.offset6):b}"
        elif "LEA" == instruction.name:
            binary_string = "1110"
            binary_string += f"{int(instruction.DR[1]):b}"
            binary_string += f"{int(instruction.PCoffset9):b}"
        elif "NOT" == instruction.name:
            binary_string = "1001"
            binary_string += f"{int(instruction.DR[1]):b}"
            binary_string += f"{int(instruction.SR[1]):b}"
            binary_string += "111111"
        elif "RET" == instruction.name:
            binary_string = "1100"
            binary_string += "000111000000"
        elif "RTI" == instruction.name:
            binary_string = "1000"
            binary_string += "000000000000"
        elif "ST" == instruction.name:
            binary_string = "0011"
            binary_string += f"{int(instruction.SR[1]):b}"
            binary_string += f"{int(instruction.PCoffset9):b}"
        elif "STI" == instruction.name:
            binary_string = "1011"
            binary_string += f"{int(instruction.SR[1]):b}"
            binary_string += f"{int(instruction.PCoffset9):b}"
        elif "STR" == instruction.name:
            binary_string = "0111"
            binary_string += f"{int(instruction.SR[1]):b}"
            binary_string += f"{int(instruction.BaseR[1]):b}"
            binary_string += f"{int(instruction.offset6):b}"
        else:
            binary_string = "1111"
            binary_string += "0000"
            if 'TRAPX20' == instruction.name or "GETC" == instruction.name:
                binary_string += f"{int("20", 16):b}"
            elif 'TRAPX21' == instruction.name or "OUT" == instruction.name:
                binary_string += f"{int("21", 16):b}"
            elif 'TRAPX22' == instruction.name or "PUTS" == instruction.name:
                binary_string += f"{int("22", 16):b}"
            elif 'TRAPX23' == instruction.name or "IN" == instruction.name:
                binary_string += f"{int("23", 16):b}"
            elif 'TRAPX25' == instruction.name or "HALT" == instruction.name:
                binary_string += f"{int("25", 16):b}"
            else: #if user defined trap TRAPxXX
                binary_string += f"{int(instruction.name[5:], 16):b}"
                
    def bin_to_instruction(self, binary_string):
        instruction = Instruction()
        # converts add
        if binary_string[0:4] == "0001":
            instruction.name = "ADD"
            instruction.DR = "R" + str(int(binary_string[4:7], 2))
            instruction.SR1 = "R" + str(int(binary_string[7:10], 2))
            if binary_string[10] == "1": # immediate mode
                instruction.imm5 = str(int(binary_string[11:], 2))
            else: #not immediate mode
                instruction.SR2 = "R" + str(int(binary_string[13:], 2))
        elif binary_string[0:4] == "0101":
            instruction.name = "AND"
            instruction.DR = "R" + str(int(binary_string[4:7], 2))
            instruction.SR1 = "R" + str(int(binary_string[7:10], 2))
            if binary_string[10] == "1": # immediate mode
                instruction.imm5 = str(int(binary_string[11:], 2))
            else: #not immediate mode
                instruction.SR2 = "R" + str(int(binary_string[13:], 2))
        # converts all BRs

        # Austin doesnt really think the part bELow this workssss
        elif binary_string[0:4] == "0000"
            instruction.name = "BR" 
            if 'N' in instruction.name or instruction.name == 'BR':
                instruction.name += "N"
            if 'Z' in instruction.name:
                instruction.name += "Z"
            if 'P' in instruction.name
                instruction.name = "P"
            instruction.PCoffset9 = str(int(binary_string[7:], 2))
        elif binary_string[0:4] == "1100"
            instruction.name = "JMP"
            instruction.BaseR = str(int(binary_string[7:10], 2))
        elif binary_string[0:4] == "0100"
            instruction.name = "JSR"
            instruction.PCoffset11 = str(int(binary_string[5:], 2))

        #idk how u doin JSRR so ill leTchU Take dis 1
        elif binary_string[0:4] == "0100"
            binary_string = "0100"
            binary_string += "000"
            binary_string += f"{int(instruction.BaseR[1]):b}"
            binary_string += "000000"

        # Austin hopes he didnt fuck up anything starting here but knows if he
        # did it isnt that big of a deal
        elif binary_string[0:4] == "0010":
            instruction.name = "LD"
            
        elif binary_string[0:4] == "1010":
            instruction.name = "LDI"
            
        elif binary_string[0:4] == "0110":
            instruction.name = "LDR"
            
        elif binary_string[0:4] == "1110":
            instruction.name = "LEA"
            
        elif binary_string[0:4] == "1001":
            instruction.name = "NOT"
            
        elif binary_string[0:4] == "1100":
            instruction.name = "RET"
            
        elif binary_string[0:4] == "1000":
            instruction.name = "RTI"
            
        elif binary_string[0:4] == "0011":
            instruction.name = "ST"
            
        elif binary_string[0:4] == "1011":
            instruction.name = "STI"
            
        elif binary_string[0:4] == "0111":
            instruction.name = "STR"
            


        # Austin didnt read anything below this
        else:
            binary_string = "1111"
            binary_string += "0000"
            if 'TRAPX20' == instruction.name or "GETC" == instruction.name:
                binary_string += f"{int("20", 16):b}"
            elif 'TRAPX21' == instruction.name or "OUT" == instruction.name:
                binary_string += f"{int("21", 16):b}"
            elif 'TRAPX22' == instruction.name or "PUTS" == instruction.name:
                binary_string += f"{int("22", 16):b}"
            elif 'TRAPX23' == instruction.name or "IN" == instruction.name:
                binary_string += f"{int("23", 16):b}"
            elif 'TRAPX25' == instruction.name or "HALT" == instruction.name:
                binary_string += f"{int("25", 16):b}"
            else: #if user defined trap TRAPxXX
                binary_string += f"{int(instruction.name[5:], 16):b}"


        
        
            



    def remove_comment(self, line):
        line.split(';')[0]
        return line

    def is_instruction(self, line):
        if "," in line:
            return True
        return False

    def parse_instruction(self, line):
        parts_of_line = line.split(',')
        parts_of_line = [x.upper().rstrip().lstrip() for x in parts_of_line]

    def calculate_instruction(self, instruction):
    

    
    def add_instruction(self, instruction):
        pass

    def and_instruction(self, instruction):
        pass

    def br_instruction(self, instruction):
        pass

    def jmp_instruction(self, instruction):
        pass

    def jsr_instruction(self, instruction):
        pass

    def jsrr_instruction(self, instruction):
        pass

    def ld_instruction(self, instruction):
        pass

    def ldi_instruction(self, instruction):
        pass

    def ldr_instruction(self, instruction):
        pass

    def lea_instruction(self, instruction):
        pass

    def not_instruction(self, instruction):
        pass

    def ret_instruction(self, instruction):
        pass

    def rti_instruction(self, instruction):
        pass

    def st_instruction(self, instruction):
        pass

    def sti_instruction(self, instruction):
        pass

    def str_instruction(self, instruction):
        pass

