from logic import FormulaFactory
from time import time


def test_twitter():
    start = time()

    fac = FormulaFactory()
    fac.set_ascii("(a/(a>-----b))")
    fac.next()

    while not fac.formula.is_tautology():
        fac.next()
        print(fac.formula)

    fac.formula.as_unicode()
    print("Time taken: " + str(time() - start) + "s")
    assert fac.formula.as_ascii() == "(a/(a>-(a+a))"
