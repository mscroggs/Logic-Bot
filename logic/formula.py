from itertools import product
from .symbols import Variable, bool_to_machine


class InvalidFormula(BaseException):
    pass


class Formula:
    def __init__(self, list=[], replacements=None):
        self._list = list

        self._vars = []
        for i in self._list:
            if isinstance(i, Variable) and i not in self._vars:
                self._vars.append(i)
        used = []
        if replacements is None:
            self._reps = []
            for i in self._list:
                if i.machine not in used:
                    used.append(i.machine)
                    self._reps += i.replacements
        else:
            self._reps = replacements

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
            for i, j in replacements:
                machine = j.join(machine.split(i))
            if pre == machine:
                raise InvalidFormula
        return machine == "1"

    def get_truth(self, values):
        vars = self.get_variables()
        assert len(vars) == len(values)
        machine = self.as_machine()
        for v, t in zip(vars, values):
            machine = bool_to_machine(t).join(machine.split(v.machine))
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
        return " ".join([i.tex for i in self._list])

    def as_unicode(self):
        return "".join([i.unicode for i in self._list])

    def as_machine(self):
        return "".join([i.machine for i in self._list])

    def __str__(self):
        return "".join(str(i) for i in self._list)
