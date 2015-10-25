from core import Formula

with open("running") as f:
    run = f.read()

if run!="yes":
    with open("running","w") as f:
        run = f.write("yes")

    with open("last") as f:
        last = [int(i) for i in f.read().split(",")]

    fo = Formula(last)
    fo.next()

    while not fo.is_tautology():
        fo.next()

    print fo

    with open("last","w") as f:
        f.write(",".join([str(i) for i in fo.list]))

    with open("running","w") as f:
        run = f.write("no")
