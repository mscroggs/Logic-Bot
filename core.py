from string import ascii_lowercase
greek_lowercase = [u'\u03B1',u'\u03B2',u'\u03B3',u'\u03B4',u'\u03B5',u'\u03B6',
                   u'\u03B7',u'\u03B8',u'\u03B9',u'\u03BA',u'\u03BB',u'\u03BC',
                   u'\u03BD',u'\u03BE',u'\u03BF',u'\u03C0',u'\u03C1',u'\u03C3',
                   u'\u03C4',u'\u03C5',u'\u03C6',u'\u03C7',u'\u03C8',u'\u03C9']
letters =  [i for i in ascii_lowercase] + greek_lowercase

class InvalidFormula(BaseException):
    pass

class Formula:
    def __init__(self, current=[0]):
        self.list = current

    def has_sub_tautology(self):
        for j in range(1,len(self)+1):
            for i in range(j):
                if (i>0 or j<len(self)) and self.is_sub_tautology(i,j):
                    return True
        return False

    def next(self):
        n = len(self.list)-1
        self.list[n] += 1
        while True:
            try:
                self.get_symbol_lists()[n][self.list[n]]
                break
            except IndexError:
                self.list[n] = 0
                n -= 1
                if n >= 0:
                    self.list[n] += 1
                else:
                    self.list.append(0)
                    break

    def get_symbol_lists(self):
        ok_letters = -1
        output = [[Symbol(0),Symbol(5)]]
        for i,n in enumerate(self.list[:-1]):
            sym = output[i][n]
            afters,letter_next = sym.after()
            if letter_next:
                afters += [Symbol(j+7,afters[0].prev) for j in range(ok_letters+2)]
            if sym.is_letter():
                ok_letters = max(ok_letters,sym.letter_n())
            output.append(afters)
        return output

    def as_machine(self, true, a=None, b=None):
        mach = ""
        sls = self.get_symbol_lists()[a:b]
        for i,n in enumerate(self.list[a:b]):
            mach += sls[i][n].as_machine(true)
        return mach

    def brackets_match(self):
        o = 0
        c = 0
        for i in self.as_ascii():
            if i == ")":
                o += 1
            if i == "(":
                c += 1
        return o==c

    def get_truth(self, true, a=None, b=None):
        old_mach = "z"
        mach = self.as_machine(true, a, b)

        while mach!=old_mach:
            old_mach = mach

            mach = "1".join(mach.split("NOT0"))
            mach = "0".join(mach.split("NOT1"))

            mach = "0".join(mach.split("(0AND0)"))
            mach = "0".join(mach.split("(0AND1)"))
            mach = "0".join(mach.split("(1AND0)"))
            mach = "1".join(mach.split("(1AND1)"))

            mach = "0".join(mach.split("(0OR0)"))
            mach = "1".join(mach.split("(0OR1)"))
            mach = "1".join(mach.split("(1OR0)"))
            mach = "1".join(mach.split("(1OR1)"))

            mach = "1".join(mach.split("(0IMP0)"))
            mach = "1".join(mach.split("(0IMP1)"))
            mach = "0".join(mach.split("(1IMP0)"))
            mach = "1".join(mach.split("(1IMP1)"))

            mach = "1".join(mach.split("(0IFF0)"))
            mach = "0".join(mach.split("(0IFF1)"))
            mach = "0".join(mach.split("(1IFF0)"))
            mach = "1".join(mach.split("(1IFF1)"))

        if mach == "1":
            return True
        if mach == "0":
            return False
        raise InvalidFormula

    def highest_letter(self):
        max_l = -1
        for i,n in enumerate(self.list):
            sym = self.get_symbol_lists()[i][n]
            if sym.is_letter():
                max_l = max(sym.letter_n(),max_l)
        return max_l

    def is_tautology(self):
        from itertools import product
        if not self.brackets_match():
            return False
        for true in product([0,1],repeat=self.highest_letter()+1):
            try:
                if not self.get_truth(true):
                    return False
            except InvalidFormula:
                return False
        return True

    def is_sub_tautology(self, a=None, b=None):
        from itertools import product
        if not self.brackets_match():
            return False
        for true in product([0,1],repeat=self.highest_letter()+1):
            try:
                if not self.get_truth(true, a, b):
                    return False
            except InvalidFormula:
                return False
        return True

    def is_contradiction(self):
        from itertools import product
        if not self.brackets_match():
            return False
        for true in product([0,1],repeat=self.highest_letter()+1):
            try:
                if self.get_truth(true):
                    return False
            except InvalidFormula:
                return False
        return True

    def as_ascii(self):
        output=""
        for i,n in enumerate(self.list):
            output += self.get_symbol_lists()[i][n].as_ascii()
        return output

    def as_unicode(self):
        output=""
        for i,n in enumerate(self.list):
            output += self.get_symbol_lists()[i][n].as_unicode()
        return output

    def __str__(self):
        return self.as_ascii()

    def __len__(self):
        return len(self.list)

class Symbol:
    def __init__(self, n, prev=None):
        self.n = n
        self.prev = prev

    def as_ascii(self):
        if self.n==0: return "-"
        if self.n==1: return "^"
        if self.n==2: return "v"
        if self.n==3: return "="
        if self.n==4: return ">"
        if self.n==5: return "("
        if self.n==6: return ")"
        return letters[self.letter_n()]

    def as_unicode(self):
        if self.n==0: return u"\u00AC"
        if self.n==1: return u"\u2227"
        if self.n==2: return u"\u2228"
        if self.n==3: return u"\u21FF"
        if self.n==4: return u"\u21FE"
        if self.n==5: return "("
        if self.n==6: return ")"
        return letters[self.letter_n()]

    def as_machine(self, true):
        if self.n==0: return "NOT"
        if self.n==1: return "AND"
        if self.n==2: return "OR"
        if self.n==3: return "IFF"
        if self.n==4: return "IMP"
        if self.n==5: return "("
        if self.n==6: return ")"
        return str(true[self.letter_n()])

    def after(self):
        if self.n==0: return ([Symbol(i,self) for i in [0,5]],True)
        if self.n==1: return ([Symbol(i,self) for i in [0,5]],True)
        if self.n==2: return ([Symbol(i,self) for i in [0,5]],True)
        if self.n==3: return ([Symbol(i,self) for i in [0,5]],True)
        if self.n==4: return ([Symbol(i,self) for i in [0,5]],True)
        if self.n==5: return ([Symbol(i,self) for i in [0,5]],True)
        if self.n==6: return ([Symbol(i,self) for i in [1,2,3,4,6]],False)
        n = self.prev
        while n is not None and n.n == 0:
            n = n.prev
        if n is not None:
            if n.n==5:
                return ([Symbol(i,self) for i in [1,2,3,4]],False)
            if n.n in [1,2,3,4]:
                return ([Symbol(6,self)],False)
        return ([Symbol(i,self) for i in [1,2,3,4,6]],False)

    def is_letter(self):
        if self.n>6:
            return True
        return False

    def letter_n(self):
        if self.is_letter():
            return self.n-7
        return None
