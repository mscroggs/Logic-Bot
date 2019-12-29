from logic_core import Formula

f = Formula()
f.next()

while not f.is_tautology():
    f.next()
    print f.as_unicode()

print f
print f.list
