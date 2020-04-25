from logic import FormulaFactory

def test_twitter():
    print("A")
    fac = FormulaFactory()
    print("A")
    fac.set_ascii("(av(a>-----b))")
    print("A")
    fac.next()
    print("A")

    while not fac.formula.is_tautology():
        fac.next()
        print(fac.formula)

    fac.formula.as_unicode()
    assert fac.formula.as_ascii() == "(av(a>-(a^a))"
