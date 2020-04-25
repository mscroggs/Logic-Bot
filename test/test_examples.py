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
