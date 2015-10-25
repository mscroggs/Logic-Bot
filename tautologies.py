from core import Formula

f = Formula()
f.next()

while True:
    if f.is_tautology():
        print f
    f.next()

