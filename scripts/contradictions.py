from logic import FormulaFactory
import sys

n = None
filename = None
for option, value in zip(sys.argv[1::2], sys.argv[2::2]):
    if option == "--file" or option == "-f":
        filename = value
    if option == "--max_number" or option == "-n":
        n = int(value)

fac = FormulaFactory()
fac.next()

if filename is not None:
    with open(filename, "w") as f:
        f.write(fac.symbols.ascii_key() + "\n")

count = 0
leng = 1
seq = []

try:
    while n is None or len(fac.formula) <= n:
        if fac.formula.is_contradiction():
            count += 1
            print(fac.formula)
            if filename is not None:
                with open(sys.argv[1], "a") as file:
                    file.write(fac.formula.as_ascii() + "\n")
        fac.next()
        while leng < len(fac.formula):
            seq.append(count)
            leng += 1
            count = 0
except KeyboardInterrupt:
    print(",".join([str(i) for i in seq]))
