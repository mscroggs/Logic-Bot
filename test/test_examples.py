from logic import FormulaFactory


def test_sequence():
    f = FormulaFactory()
    for a in ["((a^b)>a)", "((a^b)>b)", "((a=a)vb)", "((a>a)vb)", "((a>b)va)",
              "(av(a>b))", "(av(b=b))", "(av(b>b))", "(a>(avb))", "(a>(bva))",
              "(a>(b=b))", "(a>(b>a))", "(a>(b>b))"]:
        f.set_ascii(a)
        assert f.formula.is_tautology()
