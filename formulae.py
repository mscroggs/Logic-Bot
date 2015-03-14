from os.path import join
path='/home/pi/logic'

def candidate(formula):
    global formulae

    if len(formula)<=140 and formula not in formulae:
        formulae.append(formula)
        print formula
        f=open(join(path,'formulae'),'a')
        f.write(formula+"\n")
        f.close()

variables=["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","@","#","2","3","4","5","6","7","8","9"]

f=open(join(path,'formulae'))
formulae=f.readlines()
for i in range(0,len(formulae)):
    formulae[i]=formulae[i].strip("\n")
f.close()

oldlen=0
newlen=26

while oldlen!=newlen:
    for f in formulae+variables:
        candidate("-"+f)
    for f in formulae+variables:
        for g in formulae:
            for star in ["I","F","N","U"]:
                candidate("("+f+star+g+")")
    oldlen=newlen
    newlen=len(formulae)

f=open(join(path,'formulae'),'a')
f.write("#FINISHED#")
f.close()

