import re

reg_encoding = {
    "zero": "00000", "x0": "00000",
    "ra":   "00001", "x1": "00001",
    "sp":   "00010", "x2": "00010",
    "gp":   "00011", "x3": "00011",
    "tp":   "00100", "x4": "00100",
    "t0":   "00101", "x5": "00101",
    "t1":   "00110", "x6": "00110",
    "t2":   "00111", "x7": "00111",
    "s0":   "01000", "fp": "01000", "x8": "01000",
    "s1":   "01001", "x9": "01001",
    "a0":   "01010", "x10": "01010",
    "a1":   "01011", "x11": "01011",
    "a2":   "01100", "x12": "01100",
    "a3":   "01101", "x13": "01101",
    "a4":   "01110", "x14": "01110",
    "a5":   "01111", "x15": "01111",
    "a6":   "10000", "x16": "10000",
    "a7":   "10001", "x17": "10001",
    "s2":   "10010", "x18": "10010",
    "s3":   "10011", "x19": "10011",
    "s4":   "10100", "x20": "10100",
    "s5":   "10101", "x21": "10101",
    "s6":   "10110", "x22": "10110",
    "s7":   "10111", "x23": "10111",
    "s8":   "11000", "x24": "11000",
    "s9":   "11001", "x25": "11001",
    "s10":  "11010", "x26": "11010",
    "s11":  "11011", "x27": "11011",
    "t3":   "11100", "x28": "11100",
    "t4":   "11101", "x29": "11101",
    "t5":   "11110", "x30": "11110",
    "t6":   "11111", "x31": "11111"
}

def to_binary(value, bits):
    value = int(value)
    if value < 0:
        value = (1 << bits) + value
    return format(value, f'0{bits}b')

class Instruction:
    def __init__(self, line):
        self.inst = line

class Rtype(Instruction):
    f3 = {"add":"000", "sub":"000", "and":"111", "or":"110", "slt":"010", "srl":"101"}
    f7 = {"add":"0000000", "sub":"0100000", "and":"0000000", "or":"0000000", "slt":"0000000", "srl":"0000000"}
    opcode = "0110011"
    def code(self):
        tokens = re.split(r'[ ,]+', self.inst)
        rd, rs1, rs2 = tokens[1], tokens[2], tokens[3]
        return f"{self.f7[tokens[0]]} {reg_encoding[rs2]} {reg_encoding[rs1]} {self.f3[tokens[0]]} {reg_encoding[rd]} {self.opcode}"

class Itype(Instruction):
    f3 = {"addi":"000", "jalr":"000", "lw":"010", "sw":"010"}
    opcode = {"addi":"0010011", "jalr":"1100111", "lw":"0000011", "sw":"0100011"}
    def code(self):
        tokens = [t.strip("'") for t in re.split(r'[ ,()]+', self.inst) if t.strip()]
        if tokens[0] == "lw":
            rd, rs1, imm = tokens[1], tokens[3], tokens[2]
        elif tokens[0] == "sw":
            rs2, rs1, imm = tokens[1], tokens[3], tokens[2]
        else:
            rd, rs1, imm = tokens[1], tokens[2], tokens[3]
        imm_bin = to_binary(imm, 12)
        if tokens[0] == "sw":
            return f"{imm_bin} {reg_encoding[rs1]} {self.f3[tokens[0]]} {reg_encoding[rs2]} {self.opcode[tokens[0]]}"
        return f"{imm_bin} {reg_encoding[rs1]} {self.f3[tokens[0]]} {reg_encoding[rd]} {self.opcode[tokens[0]]}"

class Jtype(Instruction):
    opcode = "1101111"
    def code(self):
        tokens = re.split(r'[ ,]+', self.inst)
        rd, label = tokens[1], tokens[2]
        imm = self.labels[label] - self.current_pc
        imm_bin = to_binary(imm, 21)
        imm_reordered = imm_bin[0] + imm_bin[10:20] + imm_bin[9] + imm_bin[1:9] + "0"
        return f"{imm_reordered} {reg_encoding[rd]} {self.opcode}"

class Btype(Instruction):
    f3 = "000"
    opcode = "1100011"
    def code(self):
        tokens = re.split(r'[ ,]+', self.inst)
        rs1, rs2, offset = tokens[1], tokens[2], tokens[3]
        if offset in self.labels:
            imm = self.labels[offset] - self.current_pc
        else:
            imm = int(offset)
        imm_bin = to_binary(imm, 13)
        imm_reordered = imm_bin[0] + imm_bin[2:8] + imm_bin[8:12] + imm_bin[1] + "0"
        return f"{imm_reordered} {reg_encoding[rs2]} {reg_encoding[rs1]} {self.f3} {self.opcode}"

def assemble(filename):
    labels = {}
    with open(filename, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]
    
    # First pass: collect labels
    current_pc = 0
    for line in lines:
        if ':' in line:
            label, _ = line.split(':', 1)
            labels[label.strip()] = current_pc
        current_pc += 4

    # Second pass: process instructions
    binary_output = []
    current_pc = 0
    for line in lines:
        if ':' in line:
            _, line = line.split(':', 1)
        line = line.strip()
        if not line:
            continue
        try:
            tokens = line.split()
            if tokens[0] in Rtype.f3:
                instruction = Rtype(line)
            elif tokens[0] in Itype.f3:
                instruction = Itype(line)
            elif tokens[0] == 'jal':
                instruction = Jtype(line)
                instruction.labels = labels
                instruction.current_pc = current_pc
            elif tokens[0] == 'beq':
                instruction = Btype(line)
                instruction.labels = labels
                instruction.current_pc = current_pc
            else:
                continue
            binary_output.append(instruction.code())
            current_pc += 4
        except Exception as e:
            print(f"Error processing line: {line}", e)
    for binary in binary_output:
        print(binary)


if __name__ == "__main__":
    assemble('test.txt')


    
