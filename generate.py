from math import floor
from time import time

def base_convert(n_10,base):
    if n_10<base:
        return [n_10]
    digit = n_10 % base
    n_10 -= digit
    n_10 /= base
    return base_convert(n_10,base)+[digit]

def in_order(list):
    if len(list)>0:
        if list[0]!=7:
            return False
        for i,val in enumerate(list[:-1]):
            if val!=list[i+1]-1:
                return False
    return True

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
    pass
with open("sequence","w") as f:
    pass

variables = ["a","b","c","d","e","f","g","h","i","j","k","l","m",
             "n","o","p","q","r","s","t","u","v","w","x","y","z",
             "A","B","C","D","E","F","G","H","I","J"]

charray = [")","(",">","=","/","+","-"]+variables

found = 0
leng = 1
i=0
next_print = 10**7
start = time()
while i<43**141:
    conv = base_convert(i,43)
    if len(conv)>leng:
        leng = len(conv)
        with open("sequence","a") as f:
            f.write(str(found)+",")
        found = 0
    formula = ""
    num_order=[]
    for num in conv:
        formula += charray[num]
        if num>=7 and num not in num_order:
            num_order.append(num)
    if i>next_print:
        next_print=i+10**7
        time_taken = time()-start
        proportion_done = float(i)/43**141
        if proportion_done == 0: proportion_done = 1
        time_to_finish = (time_taken/proportion_done)
        years = floor(time_to_finish/60/60/24/365.25)
        print "%s years to complete" % years
    if in_order(num_order):
        tautology = True
        for j in range(0,2**len(num_order)):
            assignment = base_convert(j,2)
            while len(assignment)<len(num_order):
                assignment = [0]+assignment
            for k,val in enumerate(assignment):
                test = str(val).join(formula.split(variables[k]))
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
                f.write(formula+"""
""")
    added = False
    for j,character in enumerate(conv):
        if (character>(j-1)/3+7 or 
            (j==1 and conv[0] in [0,2,3,4,5])
            ):
            dig = 43**(len(conv)-j)
            i -= i % dig
            i += dig
            added = True
            break
    if not added:
        i+=43
