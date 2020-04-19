from logic_core import FormulaFactory

f = FormulaFactory()
f.next()

leng = 0
count = 0
with open("9s-new","w") as file:
    pass
while True:
    if f.formula.is_tautology():
        count += 1
        if len(f.formula) == 9:
            with open("9s-new","a") as file:
                file.write(str(f.formula) + "\n")
    f.next()
    while len(f.formula)>leng:
        print(leng, count)
        leng += 1
        count = 0
