from itertools import product
from string import ascii_lowercase, ascii_uppercase
greek_lowercase = [u'\u03B1',u'\u03B2',u'\u03B3',u'\u03B4',u'\u03B5',u'\u03B6',
                   u'\u03B7',u'\u03B8',u'\u03B9',u'\u03BA',u'\u03BB',u'\u03BC',
                   u'\u03BD',u'\u03BE',u'\u03BF',u'\u03C0',u'\u03C1',u'\u03C3',
                   u'\u03C4',u'\u03C5',u'\u03C6',u'\u03C7',u'\u03C8',u'\u03C9']
letters =  [i for i in ascii_lowercase] + greek_lowercase
tex_letters = ascii_lowercase


def bool_to_machine(b):
    if b:
        return "1"
    return "0"


class InvalidFormula(BaseException):
    pass


class Symbol:
    def __init__(self, n, machine, ascii=None, unicode=None, tex=None):
        self.ascii = ascii
        self.unicode = unicode
        self.machine = machine
        self.tex = tex
        self.n = n
        self.replacements = []

    def __str__(self):
        return self.ascii

    def __eq__(self, other):
        return self.n == other.n


class Bool(Symbol):
    def __init__(self, n, bool):
        if bool:
            super().__init__(n, "1", ascii="1", unicode="1", tex="\\textsc{True}")
        else:
            super().__init__(n, "0", ascii="0", unicode="0", tex="\\textsc{False}")


class UnarySymbol(Symbol):
    def __init__(self, n, truth_table, machine, **kwargs):
        super().__init__(n, machine, **kwargs)
        for i,res in truth_table:
            self.replacements.append((self.machine + bool_to_machine(i),
                                      bool_to_machine(res)))


class BinarySymbol(Symbol):
    def __init__(self, n, truth_table, machine, **kwargs):
        super().__init__(n, machine, **kwargs)
        for i,j,res in truth_table:
            self.replacements.append(("(" + bool_to_machine(i) + self.machine + bool_to_machine(j) + ")",
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
        super().__init__(n, "VAR["+str(var_n)+"]", ascii=ascii, unicode=unicode, tex=tex)
        self.var_n = var_n

class Symbols:
    def __init__(self, allow_true_and_false=False, allow_not_not=True):
        self._next_machine = "A"
        self.symbols = []
        self.add_symbol("(", ascii="(", unicode="(", tex="(")
        self.add_symbol(")", ascii=")", unicode=")", tex=")")
        self._open = self.symbols[0]
        self._close = self.symbols[1]
        self._unary = []
        self._binary = []
        self._bool = []
        self._variables = []

        self.add_unary([(False, True), (True, False)],
                       "NOT", ascii="-", unicode=u"\u00AC", tex="\\lnot")

        self.add_binary([(True, True, True), (True, False, False),
                         (False, True, False), (False, False, False)],
                        "AND", ascii="^", unicode=u"\u2227", tex="\\land")
        self.add_binary([(True, True, True), (True, False, True),
                         (False, True, True), (False, False, False)],
                        "OR", ascii="v", unicode=u"\u2228", tex="\\lor")
        self.add_binary([(True, True, True), (True, False, False),
                         (False, True, False), (False, False, True)],
                        "IFF", ascii="=", unicode=u"\u21FF", tex="\\leftrightarrow")
        self.add_binary([(True, True, True), (True, False, False),
                         (False, True, True), (False, False, True)],
                        "IMP", ascii=">", unicode=u"\u21FE", tex="\\rightarrow")

        if allow_true_and_false:
            self.add_bool(True)
            self.add_bool(False)
        self.allow_not_not = allow_not_not

    def next(self, prev, current):
        follow = self.follow(prev)
        return follow[follow.index(current)+1]

    def follow(self, prev=[]):
        if len(prev) == 0:
            return [self._open] + self._unary
        if prev[-1] == self._open:
            return [self._open] + self._unary + self._bool + self.variables_follow(prev)
        if prev[-1] == self._close:
            return [self._close] + self._binary
        if isinstance(prev[-1], BinarySymbol):
            return [self._open] + self._unary + self._bool + self.variables_follow(prev)
        if isinstance(prev[-1], UnarySymbol):
            if self.allow_not_not:
                return [self._open] + self._unary + self._bool + self.variables_follow(prev)
            else:
                return [self._open] + [i for i in self._unary if i != prev[-1]] + self._bool + self.variables_follow(prev)
        if isinstance(prev[-1], Bool) or isinstance(prev[-1], Variable):
            return [self._close] + self._binary
        raise ValueError("Unknown Symbol.")

    def variables_follow(self, prev):
        used = max([0] + [i.var_n for i in prev if isinstance(i, Variable)])
        return [self.get_variable(i) for i in range(used+1)]

    def __len__(self):
        return len(self.symbols)

    def __getitem__(self, i):
        return self.symbols[i]

    def get_machine_name(self):
        out = _next_machine
        self._next_machine += "A"
        return out

    def get_variable(self, n):
        while len(self._variables) <= n:
            self.add_variable()
        return self._variables[n]

    def add_variable(self):
        self.symbols.append(Variable(len(self.symbols), len(self._variables)))
        self._variables.append(self.symbols[-1])

    def add_symbol(self, machine=None, **kwargs):
        if machine is None:
            machine = self.get_machine_name()
        self.symbols.append(Symbol(len(self.symbols), machine, **kwargs))

    def add_binary(self, truth_table, machine=None, **kwargs):
        if machine is None:
            machine = self.get_machine_name()
        self.symbols.append(BinarySymbol(len(self.symbols), truth_table, machine, **kwargs))
        self._binary.append(self.symbols[-1])

    def add_unary(self, truth_table, machine=None, **kwargs):
        if machine is None:
            machine = self.get_machine_name()
        self.symbols.append(UnarySymbol(len(self.symbols), truth_table, machine, **kwargs))
        self._unary.append(self.symbols[-1])

    def add_bool(self):
        self.symbols.append(Bool(len(self.symbols), bool))
        self._bool.append(self.symbols[-1])


class FormulaFactory:
    def __init__(self, start=None, allow_true_and_false=False, allow_not_not=True):
        self.allow_true_and_false = allow_true_and_false
        self.allow_not_not = allow_not_not
        self.symbols = Symbols(allow_true_and_false, allow_not_not)
        if start is None:
            self.formula = Formula([self.symbols.follow()[0]])
        else:
            self.formula = Formula([self.symbols[i] for i in start])

    def next(self):
        self.move_forward()
        while not self.formula.is_valid():
            self.move_forward()

    def move_forward(self, position=None):
        if position is None:
            position = len(self.symbols) - 1
        if position < 0:
            new_list = [self.symbols.follow()[0]]
            while len(new_list) <= len(self.formula):
                new_list.append(self.symbols.follow(new_list)[0])
            self.formula = Formula(new_list)
            return
        new_list = self.formula[:position]
        try:
            new_list.append(self.symbols.next(new_list, self.formula[position]))
        except IndexError:
            return self.move_forward(position-1)
        while len(new_list) < len(self.formula):
            new_list.append(self.symbols.follow(new_list)[0])
        self.formula = Formula(new_list)
        return

class Formula:
    def __init__(self, list=[]):
        self._list = list

        self._vars = []
        for i in self._list:
            if isinstance(i, Variable) and i not in self._vars:
                self._vars.append(i)
        used = []
        self._reps = []
        for i in self._list:
            if i.machine not in used:
                used.append(i.machine)
                self._reps += i.replacements

    def __getitem__(self, i):
        return self._list[i]

    def __len__(self):
        return len(self._list)

    def has_sub_tautology(self):
        pass

    def brackets_match(self):
        pass

    def get_variables(self):
        return self._vars

    def get_replacements(self):
        return self._reps

    def simplify(self, machine):
        replacements = self.get_replacements()
        while len(machine) > 1:
            pre = machine
            for i,j in replacements:
                machine = j.join(machine.split(i))
            if pre == machine:
                raise InvalidFormula
        return machine == "1"

    def get_truth(self, values):
        vars = self.get_variables()
        assert len(vars) == len(values)
        machine = self.as_machine()
        for v, t in zip(vars, values):
            if t:
                machine = "1".join(machine.split(v.machine))
            else:
                machine = "0".join(machine.split(v.machine))
        return self.simplify(machine)

    def is_tautology(self):
        vars = self.get_variables()
        for values in product([True, False], repeat=len(vars)):
            if not self.get_truth(values):
                return False
        return True

    def is_contradiction(self):
        vars = self.get_variables()
        for values in product([True, False], repeat=len(vars)):
            if self.get_truth(values):
                return False
        return True

    def is_valid(self):
        try:
            self.get_truth([True for i in self.get_variables()])
            return True
        except InvalidFormula:
            return False

    def as_ascii(self):
        return "".join([i.ascii for i in self._list])

    def as_tex(self):
        return "".join([i.tex for i in self._list])

    def as_unicode(self):
        return "".join([i.unicode for i in self._list])

    def as_machine(self):
        return "".join([i.machine for i in self._list])

    def __str__(self):
        return "".join(str(i) for i in self._list)

    def __len__(self):
        return len(self._list)
