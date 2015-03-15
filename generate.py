from math import floor
from time import time

class Symbols:
    def __init__(self):
        self.variables_dummy = ["a"]
        self.variables = ["a","b","c","d","e","f","g","h","i","j","k","l","m",
                     "n","o","p","q","r","s","t","u","v","w","x","y","z",
                     "A","B","C","D","E","F","G","H","I","J"]
        self.binary = [">","=","/","+"]
        self.unary = ["-"]
        self.first = ["("]+self.unary
        self.back_first = {}
        for i,val in enumerate(self.first):
            self.back_first[val]=i
        
        self.after = {}
        self.backw = {}
        for v in self.variables:
            self.after[v] = [")"]+self.binary
        for b in self.binary:
            self.after[b] = self.unary+self.variables_dummy
        for u in self.unary:
            self.after[u] = self.unary+self.variables_dummy
        self.after["("] = ["("]+self.unary+self.variables_dummy
        self.after[")"] = [")"]+self.binary
        
        for a in self.after:
            self.backw[a]={}
            for i,b in enumerate(self.after[a]):
                self.backw[a][b] = i

class Formula:
    def __init__(self):
        self.S = Symbols()
        self.choice = [self.S.first]
        self.back = [self.S.back_first]
        self.current = [0]

    def next(self):
        i = 0
        while i<len(self.current):
            self.current[i]+=1
            if self.current[i]<len(self.choice[i]):
                break
            else:
                self.current[i] = 0
            i+=1
        if i == len(self.current):
            self.current += [0]
            self.choice += [self.S.first]
            self.back += [self.S.back_first]
        i-=1
        while i>=0:
            self.choice[i] = self.S.after[self[i+1]]# or -i-2
            self.back[i] = self.S.backw[self[i+1]]
            if "a" in self.choice[i]:
                pass
            # update back and choice
            i-=1

    def __str__(self):
        output = ""
        for i,val in enumerate(self.current):
            output = self.choice[i][val]+output
        return output

    def __getitem__(self,i):
        return self.choice[i][self.current[i]]

def logic_iterate(test):
    test = "1".join(test.split("-0"))
    test = "0".join(test.split("-1"))

    test = "1".join(test.split("(0>0)"))
    test = "1".join(test.split("(0>1)"))
    test = "0".join(test.split("(1>0)"))
    test = "1".join(test.split("(1>1)"))

    test = "1".join(test.split("(0=0)"))
    test = "0".join(test.split("(0=1)"))
    test = "0".join(test.split("(1=0)"))
    test = "1".join(test.split("(1=1)"))

    test = "0".join(test.split("(0/0)"))
    test = "1".join(test.split("(0/1)"))
    test = "1".join(test.split("(1/0)"))
    test = "1".join(test.split("(1/1)"))

    test = "0".join(test.split("(0+0)"))
    test = "0".join(test.split("(0+1)"))
    test = "0".join(test.split("(1+0)"))
    test = "1".join(test.split("(1+1)"))
    return test

with open("tautologies","w") as f:
    f.write("# KEY\n")
    f.write("#  - not\n")
    f.write("#  + and\n")
    f.write("#  / or\n")
    f.write("#  > implies\n")
    f.write("#  = if and only if \n")
    f.write("#  a-z and A-J represent variables \n\n")
with open("sequence","w") as f:
    pass

found = 0
leng = 1
formula = Formula()
while True:
    current = str(formula)
    if len(current)>leng:
        leng = len(current)
        with open("sequence","a") as f:
            f.write(str(found)+",")
        found = 0
    tautology = True
    for j in range(0,2**len(current)):
        assignment = base_convert(j,2)
        assignment = [0]*(len(current)-len(assignment))+assignment
        test = current
        for k,val in enumerate(assignment):
            test = str(val).join(test.split(variables[k]))
        oldtest = "Z"
        while oldtest != test:
            oldtest = test
            test = logic_iterate(test)
        if test != "1":
            tautology = False
            break
    if tautology:
        found += 1
        with open("tautologies","a") as f:
            f.write(current+"\n")
        print(current)
