from logic_core import Formula
import sys
f = Formula()
f.next()

if len(sys.argv)>=2:
    with open(sys.argv[1],"w") as file:
        pass

while True:
    if "--" not in f.as_ascii() and f.is_tautology() and not f.has_sub_tautology():
        if len(sys.argv)>=2:
            with open(sys.argv[1],"a") as file:
                file.write(f.as_ascii()+"\n")
        else:
            print(f)
    if len(sys.argv)>=2:
        print(f)
    f.next()
