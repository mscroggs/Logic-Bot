from core import Formula
import sys
f = Formula()
f.next()

if len(sys.argv)>=2:
    with open(sys.argv[1],"w") as file:
        pass

count = 0
leng = 1
seq = []

try:
    while True:
        if f.is_contradiction():
            count += 1
            print(f)
            if len(sys.argv)>=2:
                with open(sys.argv[1],"a") as file:
                    file.write(f.as_ascii()+"\n")
        f.next()
        while leng < len(f):
            seq.append(count)
            leng += 1
            count = 0
except KeyboardInterrupt:
    print ",".join([str(i) for i in seq])
