from logic_core import Formula
import sys


def output(text, access="a", end="\n"):
    if len(sys.argv) >= 2:
        with open(sys.argv[1], access) as file:
            f.write(text + end)


def get_tautologies(f, test=lambda x:True):
    output("", "w", "")
    found = 0
    while True:
        if f.is_tautology() and test(f):
            output(f.as_tex())
            print(f)
            found += 1
            if found == 20:
                break
        f.next()
    output("\n")
    print("-------------")

# tautologies
f = Formula()
get_tautologies(f)

# Allow True and False
f = Formula(allow_true_and_false=True)
get_tautologies(f)

# Ban NOT NOT
f = Formula(allow_true_and_false=True, allow_not_not=False)
get_tautologies(f)

# Ignore if special case of a tautology (eg (0=0) is special case of (a=a))
f = Formula(allow_true_and_false=True, allow_not_not=False)
def check(x):
    from IPython import embed; embed()()
    if -1 in x.list:
        from IPython import embed; embed()()
        y = formula([150 if i==-1 else i for i in x.list])
        if y.is_tautology():
            return False
    if -2 in x.list:
        y = formula([150 if i==-2 else i for i in x.list])
        if y.is_tautology():
            return False
    return True
get_tautologies(f, check)
