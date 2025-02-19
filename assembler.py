import re
def to_twos_complement(n, bits):
    if n >= 0:
        # Positive numbers, use bin and remove the '0b' prefix
        return bin(n)[2:].zfill(bits)
    else:
        # For negative numbers, apply two's complement
        return bin((1 << bits) + n)[2:].zfill(bits)


def to_twos_complement(n, bits):
    if n >= 0:
        return bin(n)[2:].zfill(bits)
    else:
        return bin((1 << bits) + n)[2:].zfill(bits)


class Rtype:
    encoding={f"x{i}": to_twos_complement(i, 5) for i in range(0,32)}|{"zero":"00000","ra":"00001","sp":"00010","gp":"00011","tp":"00100","t0":"00101","t1":"00110","t2":"00111","s0":"01000","fp":"01000","s1":"01001","a0":"01010","a1":"01011"}|{f"a{i-10}": to_twos_complement(i, 5) for i in range(12,18)}|{f"s{i-16}": to_twos_complement(i, 5) for i in range(18,28)}|{f"t{i-25}": to_twos_complement(i, 5) for i in range(28,32)}
    
    f3={"add":"000","sub":"000","and":"111","or":"110","slt":"010","srl":"101"}
    f7={"add":"0000000","sub":"0100000","and":"0000000","or":"0000000","slt":"0000000","srl":"0000000"}
    def __init__(self,line ):
        self.inst=line
    def code(self):
        l = re.split(r'[ ,]+', self.inst)
        out=f"{self.f7[l[0]]}{self.encoding[l[3]]}{self.encoding[l[2]]}{self.f3[l[0]]}{self.encoding[l[1]]}0110011"
        return out
        
class I1type:
    encoding={f"x{i}": to_twos_complement(i, 5) for i in range(0,32)}|{"zero":"00000","ra":"00001","sp":"00010","gp":"00011","tp":"00100","t0":"00101","t1":"00110","t2":"00111","s0":"01000","fp":"01000","s1":"01001","a0":"01010","a1":"01011"}|{f"a{i-10}": to_twos_complement(i, 5) for i in range(12,18)}|{f"s{i-16}": to_twos_complement(i, 5) for i in range(18,28)}|{f"t{i-25}": to_twos_complement(i, 5) for i in range(28,32)}
    
    f3={"addi":"000","jalr":"000","lw":"010"}
    opcode={"addi":"0010011","jalr":"1100111","lw":"0000011"}

    def __init__(self,line ):
        self.line=line
    def code(self):
        l= re.split(r'[ ,]+',self.line)
        imm=to_twos_complement(int(l[3]),12)
        out=f"{imm}{self.encoding[l[2]]}{self.f3[l[0]]}{self.encoding[l[1]]}{self.opcode[l[0]]}"
        return out

class I2type:
    encoding={f"x{i}": to_twos_complement(i, 5) for i in range(0,32)}|{"zero":"00000","ra":"00001","sp":"00010","gp":"00011","tp":"00100","t0":"00101","t1":"00110","t2":"00111","s0":"01000","fp":"01000","s1":"01001","a0":"01010","a1":"01011"}|{f"a{i-10}": to_twos_complement(i, 5) for i in range(12,18)}|{f"s{i-16}": to_twos_complement(i, 5) for i in range(18,28)}|{f"t{i-25}": to_twos_complement(i, 5) for i in range(28,32)}
    
    f3={"addi":"000","jalr":"000","lw":"010"}
    opcode={"addi":"0010011","jalr":"1100111","lw":"0000011"}

    def __init__(self,line ):
        self.line=line
    def code(self):
        l=re.split(r'[ ,()]+',self.line)
        imm=to_twos_complement(int(l[2]),12)
        out=f"{imm}{self.encoding[l[3]]}{self.f3[l[0]]}{self.encoding[l[1]]}{self.opcode[l[0]]}"
        return out
        
class Stype:
    encoding={f"x{i}": to_twos_complement(i, 5) for i in range(0,32)}|{"zero":"00000","ra":"00001","sp":"00010","gp":"00011","tp":"00100","t0":"00101","t1":"00110","t2":"00111","s0":"01000","fp":"01000","s1":"01001","a0":"01010","a1":"01011"}|{f"a{i-10}": to_twos_complement(i, 5) for i in range(12,18)}|{f"s{i-16}": to_twos_complement(i, 5) for i in range(18,28)}|{f"t{i-25}": to_twos_complement(i, 5) for i in range(28,32)}
    
    opcode={"sw":"0100011"}
    f3={"sw":"010"}

    def __init__(self,line ):
        self.line=line
    def code(self):
        l=[x for x in re.split(r'[ ,()]+',self.line) if x]

        imm=to_twos_complement(int(l[2]),12)
        out=f"{imm[:7]}{self.encoding[l[1]]}{self.encoding[l[-1]]}010{imm[7:]}0100011"
        return out


class Btype:
    encoding={f"x{i}": to_twos_complement(i, 5) for i in range(0,32)}|{"zero":"00000","ra":"00001","sp":"00010","gp":"00011","tp":"00100","t0":"00101","t1":"00110","t2":"00111","s0":"01000","fp":"01000","s1":"01001","a0":"01010","a1":"01011"}|{f"a{i-10}": to_twos_complement(i, 5) for i in range(12,18)}|{f"s{i-16}": to_twos_complement(i, 5) for i in range(18,28)}|{f"t{i-25}": to_twos_complement(i, 5) for i in range(28,32)}
    
    f3={"beq":"000","bne":"001","blt":"100"}
    opcode={"beq":"1100011","bne":"1100011","blt":"1100011"}
    def __init__(self,line ):
        self.line=line
    def code(self):
        l=re.split(r'[ ,]+',self.line)
        imm=to_twos_complement(int(l[3]),12)
        out=f"{imm[:7]}{self.encoding[l[2]]}{self.encoding[l[1]]}{self.f3[l[0]]}{imm[7:]}1100011"
        return out


class Jtype:
    encoding={f"x{i}": to_twos_complement(i, 5) for i in range(0,32)}|{"zero":"00000","ra":"00001","sp":"00010","gp":"00011","tp":"00100","t0":"00101","t1":"00110","t2":"00111","s0":"01000","fp":"01000","s1":"01001","a0":"01010","a1":"01011"}|{f"a{i-10}": to_twos_complement(i, 5) for i in range(12,18)}|{f"s{i-16}": to_twos_complement(i, 5) for i in range(18,28)}|{f"t{i-25}": to_twos_complement(i, 5) for i in range(28,32)}
    
    opcode={"jal":"1101111"}
    def __init__(self,line ):
        self.line=line
    def code(self):
        l=[x for x in re.split(r'[ ,()]+',self.line) if x]
        imm=to_twos_complement(int(l[2]),20)
        out=f"{imm}{self.encoding[l[1]]}1101111"
        return out



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
    labels={}
    with open(filename,"r") as f:
        l=[x.rstrip() for x in f.read().split("\n")]
<<<<<<< HEAD

    #replacing label in the list with immediate values    
    for i in range(len(l)):
        if(":" in l[i]):
            a=l[i].split(":")
            labels[a[0]]=i
            l[i]=a[1].strip()
            
    for i in range(len(l)):
        a=l[i].split(',')
        if(a[-1] in labels):
            a[-1]=str((labels[a[-1]]-i)*4)
            l[i]=','.join(a)
=======
>>>>>>> 11087e77f325be95057833950aa3269fefbdb60c
    
        
               
    errors=debug(l)
    for i in errors:print(i)
    if(len(errors)>0):exit()
    ans=""
    for i in l:
        if(identity(i)=="R"):
            a=Rtype(i)
            ans+=a.code()+"\n"
        elif(identity(i)=="I1"):
            a=I1type(i)
            ans+=a.code()+"\n"
        elif(identity(i)=="I2"):
            a=I2type(i)
            ans+=a.code()+"\n"
        elif(identity(i)=="S"):
            a=Stype(i)
            ans+=a.code()+"\n"
        elif(identity(i)=="J"):
            a=Jtype(i)
            ans+=a.code()+"\n"
        elif(identity(i)=="B"):
            a=Btype(i)
            ans+=a.code()+"\n"

    print(ans)

<<<<<<< HEAD
read_assembly("Ex_test_10.txt")
=======
read_assembly("Ex_test_1.txt")
>>>>>>> 11087e77f325be95057833950aa3269fefbdb60c



    