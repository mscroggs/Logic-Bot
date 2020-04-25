from string import ascii_lowercase

ascii_lowercase = [i for i in ascii_lowercase]
greek_lowercase = [u'\u03B1', u'\u03B2', u'\u03B3', u'\u03B4', u'\u03B5',
                   u'\u03B6', u'\u03B7', u'\u03B8', u'\u03B9', u'\u03BA',
                   u'\u03BB', u'\u03BC', u'\u03BD', u'\u03BE', u'\u03BF',
                   u'\u03C0', u'\u03C1', u'\u03C3', u'\u03C4', u'\u03C5',
                   u'\u03C6', u'\u03C7', u'\u03C8', u'\u03C9']
letters = ascii_lowercase + greek_lowercase
tex_letters = ascii_lowercase


def bool_to_machine(b):
    if b:
        return "1"
    return "0"


def bool_to_str(b):
    if b:
        return "True"
    return "False"


class Symbol:
    def __init__(self, n, machine, ascii=None, unicode=None, tex=None,
                 name=None):
        self.ascii = ascii
        self.unicode = unicode
        self.machine = machine
        self.tex = tex
        self.n = n
        self.replacements = []
        self.name = name

    def __str__(self):
        return self.ascii

    def __eq__(self, other):
        return self.n == other.n


class Bool(Symbol):
    def __init__(self, n, bool):
        super().__init__(n, bool_to_machine(bool), ascii="1", unicode="1",
                         tex="\\textsc{" + bool_to_str(bool) + "}")


class UnarySymbol(Symbol):
    def __init__(self, n, truth_table, machine, **kwargs):
        super().__init__(n, machine, **kwargs)
        for i, res in truth_table:
            self.replacements.append((self.machine + bool_to_machine(i),
                                      bool_to_machine(res)))


class BinarySymbol(Symbol):
    def __init__(self, n, truth_table, machine, **kwargs):
        super().__init__(n, machine, **kwargs)
        for i, j, res in truth_table:
            self.replacements.append(("(" + bool_to_machine(i)
                                      + self.machine
                                      + bool_to_machine(j) + ")",
                                      bool_to_machine(res)))


class Variable(Symbol):
    def __init__(self, n, var_n):
        if var_n < len(ascii_lowercase):
            ascii = ascii_lowercase[var_n]
        else:
            ascii = None
        if var_n < len(letters):
            unicode = letters[var_n]
        else:
            unicode = None
        if var_n < len(tex_letters):
            tex = tex_letters[var_n]
        else:
            tex = None
        super().__init__(n, "VAR["+str(var_n)+"]", ascii=ascii,
                         unicode=unicode, tex=tex)
        self.var_n = var_n


class Symbols:
    def __init__(self, **params):
        self._next_machine = "A"
        self._symbols = []
        self._unary = []
        self._binary = []
        self._bool = []
        self._variables = []

        self.add_unary([(False, True), (True, False)],
                       "NOT", ascii="-", unicode=u"\u00AC", tex="\\lnot",
                       name="not")

        self.add_binary([(True, True, True), (True, False, False),
                         (False, True, False), (False, False, False)],
                        "AND", ascii="+", unicode=u"\u2227", tex="\\land",
                        name="and")
        self.add_binary([(True, True, True), (True, False, True),
                         (False, True, True), (False, False, False)],
                        "OR", ascii="/", unicode=u"\u2228", tex="\\lor",
                        name="or")
        self.add_binary([(True, True, True), (True, False, False),
                         (False, True, False), (False, False, True)],
                        "IFF", ascii="=", unicode=u"\u21FF",
                        tex="\\leftrightarrow", name="if and only if")
        self.add_binary([(True, True, True), (True, False, False),
                         (False, True, True), (False, False, True)],
                        "IMP", ascii=">", unicode=u"\u21FE",
                        tex="\\rightarrow", name="implies")

        self.add_symbol("(", ascii="(", unicode="(", tex="(")
        self._open = self._symbols[-1]
        self.add_symbol(")", ascii=")", unicode=")", tex=")")
        self._close = self._symbols[-1]

        if "include_bools" in params and params["include_bools"]:
            self.add_bool(True)
            self.add_bool(False)
        if "allow_not_not" in params:
            self.allow_not_not = params["allow_not_not"]
        else:
            self.allow_not_not = True

        self.replacements = []
        for i in self._symbols:
            self.replacements += i.replacements

    def ascii_key(self):
        key = "# KEY\n"
        for s in self._unary:
            key += "#  " + s.ascii + " " + s.name + "\n"
        for s in self._binary:
            key += "#  " + s.ascii + " " + s.name + "\n"
        key += "#  a-z represent variables"
        return key

    def next(self, prev, current):
        follow = self.follow(prev)
        return follow[follow.index(current)+1]

    def follow(self, prev=[]):
        """Returns a list of characters that could follow prev."""
        # If this is the first character
        if len(prev) == 0:
            return self._unary + [self._open]
        # If no brackets have been opened
        if prev.count(self._open) == 0:
            if self.allow_not_not:
                return self._unary + [self._open]
            else:
                return [i for i in self._unary if i != prev[-1]] + [self._open]

        # If all brackets are closed, this is invalid, so just return )
        if prev.count(self._open) <= prev.count(self._close):
            return [self._close]

        # If last character is (
        if prev[-1] == self._open:
            return (self._unary + self._bool + [self._open]
                    + self.variables_follow(prev))
        # If last character is a binary symbol
        if isinstance(prev[-1], BinarySymbol):
            return (self._unary + self._bool + [self._open]
                    + self.variables_follow(prev))
        # If last character is a unary symbol
        if isinstance(prev[-1], UnarySymbol):
            if self.allow_not_not:
                return (self._unary + self._bool + [self._open]
                        + self.variables_follow(prev))
            else:
                return ([i for i in self._unary if i != prev[-1]]
                        + self._bool + [self._open]
                        + self.variables_follow(prev))
        # If the last character is a variable, bool or )
        assert (isinstance(prev[-1], Bool) or isinstance(prev[-1], Variable)
                or prev[-1] == self._close)
        op = 0
        for i in prev[::-1]:
            if i == self._open:
                if op == 0:
                    break
                op -= 1
            if i == self._close:
                op += 1
            if op == 0 and isinstance(i, BinarySymbol):
                return [self._close]
        return self._binary

    def variables_follow(self, prev):
        used = max([-1] + [i.var_n for i in prev if isinstance(i, Variable)])
        return [self.get_variable(i) for i in range(used+2)]

    def __len__(self):
        return len(self._symbols)

    def __getitem__(self, i):
        return self._symbols[i]

    def get_machine_name(self):
        out = self._next_machine
        self._next_machine += "A"
        return out

    def get_variable(self, n):
        while len(self._variables) <= n:
            self.add_variable()
        return self._variables[n]

    def add_variable(self):
        self._symbols.append(Variable(len(self._symbols),
                                      len(self._variables)))
        self._variables.append(self._symbols[-1])

    def add_symbol(self, machine=None, **kwargs):
        if machine is None:
            machine = self.get_machine_name()
        self._symbols.append(Symbol(len(self._symbols), machine, **kwargs))

    def add_binary(self, truth_table, machine=None, **kwargs):
        if machine is None:
            machine = self.get_machine_name()
        self._symbols.append(BinarySymbol(len(self._symbols), truth_table,
                                          machine, **kwargs))
        self._binary.append(self._symbols[-1])

    def add_unary(self, truth_table, machine=None, **kwargs):
        if machine is None:
            machine = self.get_machine_name()
        self._symbols.append(UnarySymbol(len(self._symbols), truth_table,
                                         machine, **kwargs))
        self._unary.append(self._symbols[-1])

    def add_bool(self):
        self._symbols.append(Bool(len(self._symbols), bool))
        self._bool.append(self._symbols[-1])

    def get_from_ascii(self, a):
        if a in letters:
            return self.get_variable(letters.index(a))
        for s in self._symbols:
            if s.ascii == a:
                return s
        raise ValueError("Unknown character " + a)
