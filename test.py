from logic_core import Formula, FormulaFactory
from time import time

start = time()

f = FormulaFactory()
f.next()

leng = 0
count = 0
while leng <= 8:
    if f.formula.is_tautology():
        print(f.formula)
        count += 1
    f.next()
    while len(f.formula)>leng:
        if leng == 5:
            assert count == 2
        if leng == 6:
            assert count == 2
        if leng == 7:
            assert count == 12
        if leng == 8:
            assert count == 6
        leng += 1
        count = 0

print("Time taken: "+str(time()-start)+"s")

