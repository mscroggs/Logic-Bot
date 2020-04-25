from logic import FormulaFactory


def test_tautologies():
    f = FormulaFactory()
    for a in ["((a+b)>a)", "((a+b)>b)", "((a=a)/b)", "((a>a)/b)", "((a>b)/a)",
              "(a/(a>b))", "(a/(b=b))", "(a/(b>b))", "(a>(a/b))", "(a>(b/a))",
              "(a>(b=b))", "(a>(b>a))", "(a>(b>b))", "--(a=a)"]:
        f.set_ascii(a)
        assert f.formula.as_ascii() == a
        assert f.formula.is_valid()
        assert f.formula.is_tautology()

        f.set_ascii("-" + a)
        assert f.formula.is_contradiction()


def text_set_next():
    f = FormulaFactory
    for a in ["(a=(a=(-bvb)))"]:
        f.set_ascii(a)
        f.next()


def test_following():
    fac = FormulaFactory()
    fac.set_ascii("(a=(----b=b)")
    assert len(fac.symbols.follow(fac.formula._list)) == 1


def test_next():
    fac = FormulaFactory()
    fac.set_ascii("(a/(a>-(a+----")
    fac.next()
    assert fac.formula.as_ascii() == "(a/(a>-(a+a)))"


def test_bools():
    fac = FormulaFactory(include_bools=True)
    fac.set_ascii("-(1+1)")
    assert fac.formula.is_contradiction()
    assert not fac.formula.is_tautology()

    fac.set_ascii("-(0+1)")
    assert not fac.formula.is_contradiction()
    assert fac.formula.is_tautology()


def test_not_not():
    fac = FormulaFactory(allow_not_not=False)
    for i in range(30):
        fac.next()
        assert "--" not in fac.formula.as_ascii()
