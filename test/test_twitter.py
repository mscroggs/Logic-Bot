from logic import FormulaFactory


def test_twitter():
    fac = FormulaFactory()
    fac.set_ascii("(av(a>-----b))")
    fac.next()

    while not fac.formula.is_tautology():
        fac.next()
        print(fac.formula)

    fac.formula.as_unicode()
    assert fac.formula.as_ascii() == "(av(a>-(a^a))"
