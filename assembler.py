import re

class Rtype:
    encoding={f"x{i}": format(i, '05b') for i in range(0,32)}|{"zero":"00000","ra":"00001","sp":"00010","gp":"00011","tp":"00100","t0":"00101","t1":"00110","t2":"00111","s0":"01000","fp":"01000","s1":"01001","a0":"01010","a1":"01011"}|{f"a{i-10}": format(i, '05b') for i in range(12,18)}|{f"s{i-16}": format(i, '05b') for i in range(18,28)}|{f"t{i-25}": format(i, '05b') for i in range(28,32)}
    
    f3={"add":"000","sub":"000","and":"010","or":"101","slt":"110","srl":"111"}
    f7={"add":"0000000","sub":"0100000","and":"0000000","or":"0000000","slt":"0000000","srl":"0000000"}
    def __init__(self,line ):
        self.inst=line
    def code(self):
        l = re.split(r'[ ,]+', self.inst)
        out=f"{self.f7[l[0]]} {self.encoding[l[3]]} {self.encoding[l[2]]} {self.f3[l[0]]} {self.encoding[l[1]]} 0110011"
        return out
        
class I1type:
    encoding={f"x{i}": format(i, '05b') for i in range(0,32)}|{"zero":"00000","ra":"00001","sp":"00010","gp":"00011","tp":"00100","t0":"00101","t1":"00110","t2":"00111","s0":"01000","fp":"01000","s1":"01001","a0":"01010","a1":"01011"}|{f"a{i-10}": format(i, '05b') for i in range(12,18)}|{f"s{i-16}": format(i, '05b') for i in range(18,28)}|{f"t{i-25}": format(i, '05b') for i in range(28,32)}
    
    f3={"addi":"000","jalr":"000","lw":"010"}
    opcode={"addi":"0010011","jalr":"1100111","lw":"0000011"}

    def __init__(self,line ):
        self.line=line
    def code(self):
        l= re.split(r'[ ,]+',self.line)
        out=f""
class I2type:
    encoding={f"x{i}": format(i, '05b') for i in range(0,32)}|{"zero":"00000","ra":"00001","sp":"00010","gp":"00011","tp":"00100","t0":"00101","t1":"00110","t2":"00111","s0":"01000","fp":"01000","s1":"01001","a0":"01010","a1":"01011"}|{f"a{i-10}": format(i, '05b') for i in range(12,18)}|{f"s{i-16}": format(i, '05b') for i in range(18,28)}|{f"t{i-25}": format(i, '05b') for i in range(28,32)}
    
    f3={"addi":"000","jalr":"000","lw":"010"}
    opcode={"addi":"0010011","jalr":"1100111","lw":"0000011"}

    def __init__(self,line ):
        self.line=line
    def code(self):
        l=re.split(r'[ ,()]+',self.line)
        imm=format(int(l[2]),'012b')
        out=f"{imm[:8]} {encoding[l[-1]]} 010 {imm[8:]} 0100011"
        
class Stype:
    encoding={f"x{i}": format(i, '05b') for i in range(0,32)}|{"zero":"00000","ra":"00001","sp":"00010","gp":"00011","tp":"00100","t0":"00101","t1":"00110","t2":"00111","s0":"01000","fp":"01000","s1":"01001","a0":"01010","a1":"01011"}|{f"a{i-10}": format(i, '05b') for i in range(12,18)}|{f"s{i-16}": format(i, '05b') for i in range(18,28)}|{f"t{i-25}": format(i, '05b') for i in range(28,32)}
    
    opcode={"sw":"0100011"}
    f3={"sw":"010"}

    def __init__(self,line ):
        self.line=line
    def code(self):
        l=re.split(r'[ ,()]+',self.line)
        imm=format(int(l[2]),'012b')
        out=f"{imm[:8]} {encoding[l[-1]]} 010 {imm[8:]} 0100011"


class Btype:
    encoding={f"x{i}": format(i, '05b') for i in range(0,32)}|{"zero":"00000","ra":"00001","sp":"00010","gp":"00011","tp":"00100","t0":"00101","t1":"00110","t2":"00111","s0":"01000","fp":"01000","s1":"01001","a0":"01010","a1":"01011"}|{f"a{i-10}": format(i, '05b') for i in range(12,18)}|{f"s{i-16}": format(i, '05b') for i in range(18,28)}|{f"t{i-25}": format(i, '05b') for i in range(28,32)}
    
    f3={"beq":"000","bne":"001","blt":"100"}
    opcode={"beq":"1100011","bne":"1100011","blt":"1100011"}
    def __init__(self,line ):
        self.line=line
    def code(self):
        l=re.split(r'[ ,]+',self.line)
        imm=format(int(l[3]),'012b')
        out=f"{imm[:8]} {encoding[l[-1]]} 010 {imm[8:]} 1100011"


class Jtype:
    encoding={f"x{i}": format(i, '05b') for i in range(0,32)}|{"zero":"00000","ra":"00001","sp":"00010","gp":"00011","tp":"00100","t0":"00101","t1":"00110","t2":"00111","s0":"01000","fp":"01000","s1":"01001","a0":"01010","a1":"01011"}|{f"a{i-10}": format(i, '05b') for i in range(12,18)}|{f"s{i-16}": format(i, '05b') for i in range(18,28)}|{f"t{i-25}": format(i, '05b') for i in range(28,32)}
    
    opcode={"jal":"1101111"}
    def __init__(self,line ):
        self.line=line
    def code(self):
        l=re.split(r'[ ,()]+',self.line)
        imm=format(int(l[2]),'012b')
        out=f"{imm[:8]} {encoding[l[-1]]} 010 {imm[8:]} 0100011"



#starting of the assembler project code now 
def identity(i):
    i=i.rstrip()
    if i=="":
        return " "
    if(i[0]==" "):return "error"

    #using re python library to match strings
    rsyntax = r"^(add|sub|and|or|slt|srl) (zero|x[0-9]|x1[0-9]|x2[0-9]|x3[0-1]|ra|sp|gp|tp|t[0-6]|s[0-9]|fp|s1[0-1]|a[0-7]),(zero|x[0-9]|x1[0-9]|x2[0-9]|x3[0-1]|ra|sp|gp|tp|t[0-6]|s[0-9]|fp|s1[0-1]|a[0-7]),(zero|x[0-9]|x1[0-9]|x2[0-9]|x3[0-1]|ra|sp|gp|tp|t[0-6]|s[0-9]|fp|s1[0-1]|a[0-7])$"
    isyntax = r"^(addi|jalr|lw) (zero|x[0-9]|x1[0-9]|x2[0-9]|x3[0-1]|ra|sp|gp|tp|t[0-6]|s[0-9]|fp|s1[0-1]|a[0-7]),(zero|x[0-9]|x1[0-9]|x2[0-9]|x3[0-1]|ra|sp|gp|tp|t[0-6]|s[0-9]|fp|s1[0-1]|a[0-7]),(-?\d+)$"
    i2syntax= r"^(addi|jalr|lw) (zero|x[0-9]|x1[0-9]|x2[0-9]|x3[0-1]|ra|sp|gp|tp|t[0-6]|s[0-9]|fp|s1[0-1]|a[0-7]),(-?\d+)\((zero|x[0-9]|x1[0-9]|x2[0-9]|x3[0-1]|ra|sp|gp|tp|t[0-6]|s[0-9]|fp|s1[0-1]|a[0-7])\)$"
    ssyntax = r"^(sw) (zero|x[0-9]|x1[0-9]|x2[0-9]|x3[0-1]|ra|sp|gp|tp|t[0-6]|s[0-9]|fp|s1[0-1]|a[0-7]),(-?\d+)\((zero|x[0-9]|x1[0-9]|x2[0-9]|x3[0-1]|ra|sp|gp|tp|t[0-6]|s[0-9]|fp|s1[0-1]|a[0-7])\)$"
    bsyntax = r"^(beq|bne|blt) (zero|x[0-9]|x1[0-9]|x2[0-9]|x3[0-1]|ra|sp|gp|tp|t[0-6]|s[0-9]|fp|s1[0-1]|a[0-7]),(zero|x[0-9]|x1[0-9]|x2[0-9]|x3[0-1]|ra|sp|gp|tp|t[0-6]|s[0-9]|fp|s1[0-1]|a[0-7]),(-?\d+)$"
    #usyntax = r"^(lui|auipc) (\w+),(\d+)$"
    jsyntax = r"^(jal) (zero|x[0-9]|x1[0-9]|x2[0-9]|x3[0-1]|ra|sp|gp|tp|t[0-6]|s[0-9]|fp|s1[0-1]|a[0-7]),(-?\d+)$"

    # passing line by line through instruction array to checking it's type
    if re.match(rsyntax, i):
        return "R"
    elif re.match(isyntax, i):
        return "I1"
    elif re.match(i2syntax, i):
        return "I2"
    elif re.match(ssyntax, i):
        return "S"
    elif re.match(bsyntax, i):
        return "B"
    # elif re.match(usyntax, i):
    #     return "U"
    elif re.match(jsyntax, i):
        return "J"
    else:
        return "error"

def debug(l):
    error=[]
    for i in range(len(l)):
        if identity(l[i])=="error":
            error.append(f"line:{i+1} syntax error! invalid syntax for  RISC ISA")
    return error

def read_assembly(filename):
    with open(filename,"r") as f:
        l=[x.rstrip() for x in f.read().split("\n")]
        print(l)
    
    errors=debug(l)
    for i in errors:print(i)
    if(len(errors)>0):exit()
    ans=""
    for i in l:
        if(identity(i)=="R"):
            a=Rtype(i)
            ans+=a.code()
        elif(identity(i)=="I"):
            a=Itype(i)
            ans+=a.code()
        elif(identity(i)=="S"):
            a=Stype(i)
            ans+=a.code()
        elif(identity(i)=="J"):
            a=Jtype(i)
            ans+=a.code()
        elif(identity(i)=="B"):
            a=Btype(i)
            ans+=a.code()

    print(ans,":binary code")

read_assembly("test.txt")



    