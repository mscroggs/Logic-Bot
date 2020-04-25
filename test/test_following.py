from logic import FormulaFactory


def test_following():
    fac = FormulaFactory()
    fac.set_ascii("(a=(----b=b)")
    assert len(fac.symbols.follow(fac.formula._list)) == 1


def test_next():
    fac = FormulaFactory()
    fac.set_ascii("(a/(a>-(a+----")
    fac.next()
    assert fac.formula.as_ascii() == "(a/(a>-(a+a)))"
