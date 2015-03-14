from os.path import join
path='/home/pi/logic'

def next(ar,i=0):
    global cont
    if i<len(ar):
        if ar[i]=="0":
            ar[i]="1"
        else:
            ar[i]="0"
            ar=next(ar,i+1)
    else:
        cont=False
    return ar

def solve(lo):
    lo=lo.replace("-0","1")
    lo=lo.replace("-1","0")

    lo=lo.replace("(0I0)","1")
    lo=lo.replace("(0I1)","1")
    lo=lo.replace("(1I0)","0")
    lo=lo.replace("(1I1)","1")

    lo=lo.replace("(0F0)","1")
    lo=lo.replace("(0F1)","0")
    lo=lo.replace("(1F0)","0")
    lo=lo.replace("(1F1)","1")

    lo=lo.replace("(0N0)","0")
    lo=lo.replace("(0N1)","0")
    lo=lo.replace("(1N0)","0")
    lo=lo.replace("(1N1)","1")

    lo=lo.replace("(0U0)","0")
    lo=lo.replace("(0U1)","1")
    lo=lo.replace("(1U0)","1")
    lo=lo.replace("(1U1)","1")

    return lo

f=open(join(path,"formulae"))
formulae=f.readlines()
f.close()

f=open(join(path,"donet"))
i=int(f.read())
f.close()

variables=["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","@","#","2","3","4","5","6","7","8","9"]


while formulae[-1]!="#FINISHED#" or i<len(formulae)-1:
  if i<len(formulae):
    formula=formulae[i].strip("\n")

    insofar=True
    inA=[]
    fail=False
    for a in variables:
        if a not in formula:
            insofar=False
        elif not insofar:
            fail=True
            break
        else:
            inA.append(a)

    if not fail:
        valA=["0"]*len(inA)
        cont=True
        taut=True
        while cont and taut:
            feval=formula
            for j in range(0,len(inA)):
                feval=feval.replace(inA[j],valA[j])
            while feval not in ["0","1"]:
                feval=solve(feval)
            if feval!="1":
                taut=False
            valA=next(valA)
        if taut:
            f=open(join(path,"true"),"a")
            f.write(str(formula)+"\n")
            f.close()

    i+=1
    f=open(join(path,"donet"),"w")
    f.write(str(i))
    f.close()


  else:
    f=open(join(path,"formulae"))
    formulae=f.readlines()
    f.close()
