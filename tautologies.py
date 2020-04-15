from logic_core import Formula
import sys
f = Formula()
f.next()

if len(sys.argv)>=2:
    with open(sys.argv[1],"w") as file:
        file.write("# KEY\n#  - not\n#  + and\n#  / o\n#  > implies\n#  = if and only if\n#  a-z and A-J represent variables\n")

count = 0
leng = 1
seq = []

try:
    while True:
        if f.is_tautology():
            count += 1
            print(f)
            if len(sys.argv)>=2:
                with open(sys.argv[1],"a") as file:
                    file.write("\n"+f.as_ascii())
        f.next()
        while leng < len(f):
            seq.append(count)
            leng += 1
            count = 0
except KeyboardInterrupt:
    print(",".join([str(i) for i in seq]))
