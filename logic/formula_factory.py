from .formula import Formula
from .symbols import Symbols


class FormulaFactory:
    def __init__(self, **params):
        self.symbols = Symbols(**params)
        self.formula = Formula([self.symbols.follow()[0]])

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
            new_list.append(self.symbols.next(new_list,
                                              self.formula[position]))
        except IndexError:
            return self.move_forward(position-1)
        while len(new_list) < len(self.formula):
            new_list.append(self.symbols.follow(new_list)[0])
        self.formula = Formula(new_list)
        return

    def set_ascii(self, ascii):
        self.formula = Formula([self.symbols.get_from_ascii(a) for a in ascii])
