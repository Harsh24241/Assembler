import re

class Rtype:
    encoding={}
    def __inti__(self,line ):
        pass
    def code(self):
        pass
class Itype:
    encoding={}
    def __inti__(self,line ):
        pass
    def code(self):
        pass
class Ltype:
    encoding={}
    def __inti__(self,line ):
        pass
    def code(self):
        pass
class Btype:
    encoding={}
    def __inti__(self,line ):
        pass
    def code(self):
        pass
class Jtype:
    encoding={}
    def __inti__(self,line ):
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
    print(l)
read_assembly("Ex_test_4.txt")



    