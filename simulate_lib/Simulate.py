import sys

from simulate_lib.Instruction import Instruction
from simulate_lib.SignedBinary import SignedBinary
import msvcrt

class Simulate:
    def __init__(self, fileName):
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
        self.flag = "Z" #can be either N, Z, or P
        self.memory = list()
        self.populate_addresses()
        self.lines = self.read_in_file()
        self.fileName = fileName
        self.STARTING_ADDRESS = int("3000", 16)
        self.program_counter = self.STARTING_ADDRESS
        self.halt = False

        self.convert_file_to_memory()


    def read_in_file(self):
        with open(self.fileName) as file: #opens file
            lines = file.read().strip().split('\n') #reads in file into lines
        lines = [self.remove_comment(x.rstrip()) for x in lines] # removes \n after each line
        lines = [x for x in lines if x != '']
        return lines

    def populate_addresses(self):
        for _ in range(2**16): # looping through addresses
            self.memory.append("0" * 16) #populates memory address with 16 0's

    def instruction_to_bin(self, instruction):
        binary_string = ""

        # converts add and and
        if instruction.name == "ADD":
            binary_string = "0001"
        elif instruction.name == "AND":
            binary_string = "0101"
        if instruction.name == "ADD" or instruction.name == "AND":
            binary_string += f"{int(instruction.DR[1]):b}".zfill(3)
            binary_string += f"{int(instruction.SR1[1]):b}".zfill(3)
            if instruction.SR2 == "": # is immediate add mode
                binary_string += "1"
                binary_string += f"{instruction.imm5.to_integer():b}".zfill(5)
            else:
                binary_string += "000"
                binary_string += f"{int(instruction.SR2[1]):b}".zfill(3)

        # converts all BRs
        elif 'BR' in instruction.name:
            binary_string = "0000"
            if 'N' in instruction.name or instruction.name == 'BR':
                binary_string += '1'
            else:
                binary_string += '0'
            if 'Z' in instruction.name or instruction.name == "BR":
                binary_string += '1' 
            else:
                binary_string += '0'
            if 'P' in instruction.name or instruction.name == "BR":
                binary_string += '1'
            else:
                binary_string += '0'
            binary_string += f"{instruction.PCoffset9.to_integer():b}".zfill(9)
        
        elif 'JMP' == instruction.name:
            binary_string = "1100"
            binary_string += "000"
            binary_string += f"{int(instruction.BaseR[1]):b}".zfill(3)
            binary_string += "000000"
        elif 'JSR' == instruction.name:
            binary_string = "0100"
            binary_string += "1"
            binary_string += f"{instruction.PCoffset11.to_integer():b}".zfill(11)
        elif 'JSRR' == instruction.name:
            binary_string = "0100"
            binary_string += "000"
            binary_string += f"{int(instruction.BaseR[1]):b}".zfill(3)
            binary_string += "000000"
        elif "LD" == instruction.name:
            binary_string == "0010"
            binary_string += f"{int(instruction.DR[1]):b}".zfill(3)
            binary_string += f"{instruction.PCoffset9.to_integer():b}".zfill(9)
        elif "LDI" == instruction.name:
            binary_string = "1010"
            binary_string += f"{int(instruction.DR[1]):b}".zfill(3)
            binary_string += f"{instruction.PCoffset9.to_integer():b}".zfill(9)
        elif "LDR" == instruction.name:
            binary_string = "0110"
            binary_string += f"{int(instruction.DR[1]):b}".zfill(3)
            binary_string += f"{int(instruction.BaseR[1]):b}".zfill(3)
            binary_string += f"{instruction.offset6.to_integer():b}".zfill(6)
        elif "LEA" == instruction.name:
            binary_string = "1110"
            binary_string += f"{int(instruction.DR[1]):b}".zfill(3)
            binary_string += f"{instruction.PCoffset9.to_integer():b}".zfill(9)
        elif "NOT" == instruction.name:
            binary_string = "1001"
            binary_string += f"{int(instruction.DR[1]):b}".zfill(3)
            binary_string += f"{int(instruction.SR[1]):b}".zfill(3)
            binary_string += "111111"
        elif "RET" == instruction.name:
            binary_string = "1100"
            binary_string += "000111000000"
        elif "RTI" == instruction.name:
            binary_string = "1000"
            binary_string += "000000000000"
        elif "ST" == instruction.name:
            binary_string = "0011"
            binary_string += f"{int(instruction.SR[1]):b}".zfill(3)
            binary_string += f"{instruction.PCoffset9.to_integer():b}".zfill(9)
        elif "STI" == instruction.name:
            binary_string = "1011"
            binary_string += f"{int(instruction.SR[1]):b}".zfill(3)
            binary_string += f"{instruction.PCoffset9.to_integer():b}".zfill(9)
        elif "STR" == instruction.name:
            binary_string = "0111"
            binary_string += f"{int(instruction.SR[1]):b}".zfill(3)
            binary_string += f"{int(instruction.BaseR[1]):b}".zfill(3)
            binary_string += f"{instruction.offset6.to_integer():b}".zfill(6)
        else:
            binary_string = "1111"
            binary_string += "0000"
            binary_string += f"{instruction.trapvec8.to_integer():b}".zfill(8)

        return binary_string
                
    def bin_to_instruction(self, binary_string):
        instruction = Instruction()
        # converts add
        if binary_string[0:4] == "0001":
            instruction.name = "ADD"
            instruction.DR = "R" + str(int(binary_string[4:7], 2))
            instruction.SR1 = "R" + str(int(binary_string[7:10], 2))
            if binary_string[10] == "1": # immediate mode
                instruction.imm5.str = str(int(binary_string[11:], 2))
            else: # not immediate mode
                instruction.SR2 = "R" + str(int(binary_string[13:], 2))
        elif binary_string[0:4] == "0101":
            instruction.name = "AND"
            instruction.DR = "R" + str(int(binary_string[4:7], 2))
            instruction.SR1 = "R" + str(int(binary_string[7:10], 2))
            if binary_string[10] == "1": # immediate mode
                instruction.imm5.str = str(int(binary_string[11:], 2))
            else: #not immediate mode
                instruction.SR2 = "R" + str(int(binary_string[13:], 2))

        elif binary_string[0:4] == "0000":
            instruction.name = "BR" 
            if binary_string[4] == '1':
                instruction.name += "N"
            if binary_string[5] == '1':
                instruction.name += "Z"
            if binary_string[6] == '1':
                instruction.name += "P"
            instruction.PCoffset9.str = str(int(binary_string[7:], 2))
        elif binary_string[0:4] == "1100":
            instruction.name = "JMP"
            instruction.BaseR = str(int(binary_string[7:10], 2))
        elif binary_string[0:4] == "0100" and binary_string[4] == '1':
            instruction.name = "JSR"
            instruction.PCoffset11.str = str(int(binary_string[5:], 2))

        elif binary_string[0:4] == "0100" and binary_string[4] == '0':
            instruction.name = "JSRR"
            instruction.BaseR = "R" + str(int(binary_string[7:10], 2))

        elif binary_string[0:4] == "0010":
            instruction.name = "LD"
            instruction.DR = "R" + str(int(binary_string[4:7], 2))
            instruction.PCoffset9.str = str(int(binary_string[7:], 2))
            
        elif binary_string[0:4] == "1010":
            instruction.name = "LDI"
            instruction.DR = "R" + str(int(binary_string[4:7], 2))
            instruction.PCoffset9.str = str(int(binary_string[7:], 2))

        elif binary_string[0:4] == "0110":
            instruction.name = "LDR"
            instruction.DR = "R" + str(int(binary_string[4:7], 2))
            instruction.BaseR = "R" + str(int(binary_string[7:10], 2))
            instruction.offset6.str = str(int(binary_string[10:], 2))
            
        elif binary_string[0:4] == "1110":
            instruction.name = "LEA"
            instruction.DR = "R" + str(int(binary_string[4:7], 2))
            instruction.PCoffset9.str = str(int(binary_string[7:], 2))

        elif binary_string[0:4] == "1001":
            instruction.name = "NOT"
            instruction.DR = "R" + str(int(binary_string[4:7], 2))
            instruction.SR = "R" + str(int(binary_string[7:10], 2))
            
        elif binary_string[0:4] == "1100":
            instruction.name = "RET"
            
        elif binary_string[0:4] == "1000":
            instruction.name = "RTI"
            
        elif binary_string[0:4] == "0011":
            instruction.name = "ST"
            instruction.SR = "R" + str(int(binary_string[4:7], 2))
            instruction.PCoffset9.str = str(int(binary_string[7:], 2))
            
        elif binary_string[0:4] == "1011":
            instruction.name = "STI"
            instruction.SR = "R" + str(int(binary_string[4:7], 2))
            instruction.PCoffset9.str = str(int(binary_string[7:], 2))
            
        elif binary_string[0:4] == "0111":
            instruction.name = "STR"
            instruction.SR = "R" + str(int(binary_string[4:7], 2))
            instruction.BaseR = "R" + str(int(binary_string[7:10], 2))
            instruction.offset6.str = str(int(binary_string[10:], 2))

        # Its a TRAP
        elif binary_string[0:4] == "1111":
            instruction.name = "TRAP"
            instruction.trapvec8.str = f"{int(binary_string[8:], 2)}"
        return instruction

    def convert_file_to_memory(self):
        self.lines = self.read_in_file()
        for index, line in enumerate(self.lines):
            if self.is_instruction(line):
                self.memory[self.STARTING_ADDRESS + index] = self.instruction_to_bin(self.parse_instruction(line))

    def remove_comment(self, line):
        return line.split(';')[0]

    def is_instruction(self, line):
        parts_of_line = line.split(',')
        if len(parts_of_line) == 1 and '.' in line:
            return False
        return True

    def parse_instruction(self, line):
        instruction = Instruction()
        parts_of_line = line.split(None, 1)
        first_half = [parts_of_line[0]]
        second_half = []
        if len(parts_of_line) > 1:
            second_half = parts_of_line[1].split(',')
        parts_of_line = first_half + second_half
        parts_of_line = [x.upper().rstrip().lstrip() for x in parts_of_line]
        instruction.name = parts_of_line[0]
        if instruction.name == "ADD" or instruction.name == "AND":
            instruction.DR = parts_of_line[1]
            instruction.SR1 = parts_of_line[2]
            if 'R' in parts_of_line[3]:
                instruction.SR2 = parts_of_line[3]
            else:
                instruction.imm5.str = parts_of_line[3]

        elif "BR" in instruction.name:
            instruction.PCoffset9.str = parts_of_line[1]

        elif instruction.name == "JMP" or instruction.name == "JSRR":
            instruction.BaseR = parts_of_line[1]

        elif instruction.name == "JSR":
            instruction.PCoffset11.str = parts_of_line[1]

        elif instruction.name == "LD" or instruction.name == "LDI" or instruction.name == "LEA":
            instruction.DR = parts_of_line[1]
            instruction.PCoffset9.str = parts_of_line[2]

        elif instruction.name == "LDR":
            instruction.DR = parts_of_line[1]
            instruction.BaseR = parts_of_line[2]
            instruction.offset6.str = parts_of_line[3]
        
        elif instruction.name == "NOT":
            instruction.DR = parts_of_line[1]
            instruction.SR = parts_of_line[2]

        elif instruction.name == "ST" or instruction.name == "STI":
            instruction.SR = parts_of_line[1]
            instruction.PCoffset9.str = parts_of_line[2]

        elif instruction.name == "STR":
            instruction.SR = parts_of_line[1]
            instruction.BaseR = parts_of_line[2]
            instruction.offset6.str = parts_of_line[3]
        # do stuff here

        elif instruction.name == "GETC":
            instruction.name = "TRAP"
            instruction.trapvec8.str = f"{int('20', 16)}"

        elif instruction.name == "OUT":
            instruction.name = "TRAP"
            instruction.trapvec8.str = f"{int('21', 16)}"

        elif instruction.name == "PUTS":
            instruction.name = "TRAP"
            instruction.trapvec8.str = f"{int('22', 16)}"

        elif instruction.name == "IN":
            instruction.name = "TRAP"
            instruction.trapvec8.str = f"{int('23', 16)}"
        
        elif instruction.name == "HALT":
            instruction.name = "TRAP"
            instruction.trapvec8.str = f"{int('25', 16)}"

        elif instruction.name == "TRAP":
            instruction.trapvec8.str = parts_of_line[1]

        instruction.fix_offsets()
        return instruction

    def calculate_instruction(self):
        instruction = self.bin_to_instruction(self.memory[self.program_counter])
        self.program_counter += 1

        dict_of_instructions = {
            "ADD": self.add_instruction,
            "AND": self.and_instruction,
            "JMP": self.jmp_instruction,
            "JSR": self.jsr_instruction,
            "JSRR": self.jsrr_instruction,
            "LD": self.ld_instruction,
            "LDI": self.ldi_instruction,
            "LDR": self.ldr_instruction,
            "LEA": self.lea_instruction,
            "NOT": self.not_instruction,
            "RET": self.ret_instruction,
            "RTI": self.rti_instruction,
            "ST": self.st_instruction,
            "STI": self.sti_instruction,
            "STR": self.str_instruction,
        }

        try:
            dict_of_instructions[instruction.name](instruction)
        except KeyError:
            if instruction.trapvec8.str != "":
                if instruction.trapvec8.to_integer() == int("20", 16):
                    self.trap_20(instruction)
                elif instruction.trapvec8.to_integer() == int("21", 16):
                    self.trap_21(instruction)
                elif instruction.trapvec8.to_integer() == int("22", 16):
                    self.trap_22(instruction)
                elif instruction.trapvec8.to_integer() == int("23", 16):
                    self.trap_23(instruction)
                elif instruction.trapvec8.to_integer() == int("25", 16):
                    self.trap_25(instruction)
            elif "BR" in instruction.name:
                self.br_instruction(instruction)
        

    def add_instruction(self, instruction):
        if instruction.imm5 == "":
            self.register_values[instruction.DR] = self.register_values[instruction.SR1] + self.register_values[instruction.SR2]
        else:
            self.register_values[instruction.DR] = self.register_values[instruction.SR1] + instruction.imm5.to_integer()
        
        if self.register_values[instruction.DR] > 0:
            self.flag = 'P'
        elif self.register_values[instruction.DR] == 0:
            self.flag = 'Z'
        else:
            self.flag = 'N'

    def and_instruction(self, instruction):
        if instruction.imm5 == "":
            self.register_values[instruction.DR] = self.register_values[instruction.SR1] & self.register_values[instruction.SR2]
        else:
            self.register_values[instruction.DR] = self.register_values[instruction.SR1] & instruction.imm5.to_integer()

        if self.register_values[instruction.DR] > 0:
            self.flag = 'P'
        elif self.register_values[instruction.DR] == 0:
            self.flag = 'Z'
        else:
            self.flag = 'N'

    def br_instruction(self, instruction):
        if self.flag in instruction.name:
            self.program_counter += instruction.PCoffset9.to_integer()

    def jmp_instruction(self, instruction):
        self.program_counter = instruction.BaseR

    def jsr_instruction(self, instruction):
        self.register_values["R7"] = self.program_counter
        self.program_counter += instruction.PCoffset11.to_integer()

    def jsrr_instruction(self, instruction):
        self.register_values["R7"] = self.program_counter
        self.program_counter += self.register_values[instruction.BaseR]

    def ld_instruction(self, instruction):
        self.register_values[instruction.DR] = self.memory[self.program_counter + instruction.PCoffset9.to_integer()]

        if self.register_values[instruction.DR] > 0:
            self.flag = 'P'
        elif self.register_values[instruction.DR] == 0:
            self.flag = 'Z'
        else:
            self.flag = 'N'

    def ldi_instruction(self, instruction):
        self.register_values[instruction.DR] = self.memory[self.memory[self.program_counter + instruction.PCoffset9.to_integer()]]

        if self.register_values[instruction.DR] > 0:
            self.flag = 'P'
        elif self.register_values[instruction.DR] == 0:
            self.flag = 'Z'
        else:
            self.flag = 'N'

    def ldr_instruction(self, instruction):
        self.register_values[instruction.DR] = self.memory[instruction.BaseR + instruction.offset6.to_integer()]

        if self.register_values[instruction.DR] > 0:
            self.flag = 'P'
        elif self.register_values[instruction.DR] == 0:
            self.flag = 'Z'
        else:
            self.flag = 'N'

    def lea_instruction(self, instruction):
        self.register_values[instruction.DR] = instruction.PCoffset9.to_integer() + self.program_counter

        if self.register_values[instruction.DR] > 0:
            self.flag = 'P'
        elif self.register_values[instruction.DR] == 0:
            self.flag = 'Z'
        else:
            self.flag = 'N'
    def not_instruction(self, instruction):
        self.register_values[instruction.DR] = ~self.register_values[instruction.SR1]

        if self.register_values[instruction.DR] > 0:
            self.flag = 'P'
        elif self.register_values[instruction.DR] == 0:
            self.flag = 'Z'
        else:
            self.flag = 'N'

    def ret_instruction(self, instruction):
        self.program_counter = self.register_values["R7"]

    def rti_instruction(self, instruction):
        pass

    def st_instruction(self, instruction):
        self.memory[self.program_counter + instruction.PCoffset9.to_integer()] = f"{self.register_values[instruction.SR]:b}".zfill(16)

    def sti_instruction(self, instruction):
        self.memory[self.memory[self.program_counter + instruction.PCoffset9.to_integer()]] = f"{self.register_values[instruction.SR]:b}".zfill(16)

    def str_instruction(self, instruction):
        self.memory[instruction.BaseR + instruction.offset6.to_integer()] = f"{self.register_values[instruction.SR]:b}".zfill(16)

    def trap_20(self, instruction):
        self.register_values["R0"] = msvcrt.getch()[0]

    def trap_21(self, instruction):
        print(chr(self.register_values["R0"]), end="", flush=True)

    def trap_22(self, instruction):
        address = self.register_values["R0"]
        while self.memory[address] != "0"*16:
            print(chr(int(self.memory[address], 2)), end="", flush=True)
            address += 1

    def trap_23(self, instruction):
        print("Input a character>", end="", flush=True)
        self.register_values["R0"] = msvcrt.getch()[0]
        print(chr(self.register_values["R0"]))

    def trap_25(self, instruction):
        print("\n----- Halting the processor -----")
        self.halt = True

    def run(self):
        self.convert_file_to_memory()

        while not self.halt:
            self.calculate_instruction()
