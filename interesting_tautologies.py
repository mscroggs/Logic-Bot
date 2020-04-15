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


f = Formula()
get_tautologies(f)

f = Formula(allow_true_and_false=True)
get_tautologies(f)

f = Formula(allow_true_and_false=True)
def check(x):
    if "--" in x.as_ascii():
        return False
    return True
get_tautologies(f, check)

