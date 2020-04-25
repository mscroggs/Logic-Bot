from logic import FormulaFactory


def test_following():
    fac = FormulaFactory()
    fac.set_ascii("(a=(----b=b)")
    assert len(fac.symbols.follow(fac.formula._list)) == 1
