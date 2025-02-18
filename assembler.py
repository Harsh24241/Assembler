import re

class Rtype:
    encoding={f"x{i}": format(i, '05b') for i in range(0,32)}
    
    f3={"add":"000","sub":"000","and":"010","or":"101","slt":"110","srl":"111"}
    f7={"add":"0000000","sub":"0100000","and":"0000000","or":"0000000","slt":"0000000","srl":"0000000"}
    def __init__(self,line ):
        self.inst=line
    def code(self):
        l = re.split(r'[ ,]+', self.inst)
        out=f"{self.f7[l[0]]} {self.encoding[l[3]]} {self.encoding[l[2]]} {self.f3[l[0]]} {self.encoding[l[1]]} 0110011"
        return out
        
class Itype:
    encoding={}
    def __init__(self,line ):
        pass
    def code(self):
        pass
class Ltype:
    encoding={}
    def __init__(self,line ):
        pass
    def code(self):
        pass
class Btype:
    encoding={}
    def __init__(self,line ):
        pass
    def code(self):
        pass
class Jtype:
    encoding={}
    def __init__(self,line ):
        pass
    def code(self):
        pass



#starting of the assembler project code now 
def identity(i):
    i=i.rstrip()
    if i=="":
        return " "
    if(i[0]==" "):return "error"

    #using re python library to match strings
    rsyntax = r"^(add|sub|and|or|slt|srl) (\w+),(\w+),(\w+)$"
    isyntax = r"^(addi|jalr) (\w+),(\w+),(-?\d+)$"
    ssyntax = r"^(sw|lw) (\w+),(\d+)\((\w+)\)$"
    bsyntax = r"^(beq|bne|blt) (\w+),(\w+),(-?\d+)$"
    #usyntax = r"^(lui|auipc) (\w+),(\d+)$"
    jsyntax = r"^(jal) (\w+),(-?\d+)$"

    # passing line by line through instruction array to checking it's type
    if re.match(rsyntax, i):
        return "R"
    elif re.match(isyntax, i):
        return "I"
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

    errors=debug(l)
    for i in errors:print(i)
    if(len(errors)>0):exit()
    ans=""
    for i in l:
        if(identity(i)=="R"):
            a=Rtype(i)
            ans+=a.code()
    print(ans,":binary code")

read_assembly("test.txt")



    