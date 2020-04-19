from logic_core import FormulaFactory

f = FormulaFactory()
f.next()

leng = 0
count = 0
while True:
    if f.formula.is_tautology():
        count += 1
    f.next()
    while len(f.formula)>leng:
        print(leng, count)
        leng += 1
        count = 0
