from logic import FormulaFactory
from time import time

def test_sequence():
    start = time()

    f = FormulaFactory()
    f.next()

    leng = 0
    count = 0
    while leng <= 9:
        if f.formula.is_tautology():
            count += 1
        f.next()
        while len(f.formula)>leng:
            if leng == 5:
                assert count == 2
            elif leng == 6:
                assert count == 2
            elif leng == 7:
                assert count == 12
            elif leng == 8:
                assert count == 6
            elif leng == 9:
                assert count == 57
            else:
                assert count == 0
            leng += 1
            count = 0

    print("Time taken: "+str(time()-start)+"s")

