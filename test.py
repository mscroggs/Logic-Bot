from core import Formula
from time import time

start = time()

f = Formula()
f.next()

leng = 0
count = 0
while leng <= 8:
    if f.is_tautology():
        print f
        count += 1
    f.next()
    while len(f)>leng:
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
