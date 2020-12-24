from common.ada_type import AdaType


class AdaIntType(AdaType):
    INTEGER = 0
    MODULAR = 1
    FLOAT = 2
    FIXED = 3
    def __init__(self, name, package=None, ctx=None, is_based=False, mod=None, first=None, last=None):
        super(AdaIntType, self).__init__(name, AdaType.INT_TYPE, package, ctx, is_based)
        self.mod = mod
        if first:
            self.first = first
        if last:
            self.last = last
        if self.mod:
            self.first = str(0)
            self.last = str(int(self.mod) - 1)
        self.mod_solved = False
        self.first_solved = False
        self.last_solved = False
        self.to_print = ['is_based', 'mod', 'size']
        self.to_solve = ['mod', 'first', 'last']

    def solve_first(self, i_expr=None):
        self.solve_a_type_or_expr('first', i_expr=i_expr, is_type=False)

    def solve_last(self, i_expr=None):
        self.solve_a_type_or_expr('last', i_expr=i_expr, is_type=False)

    def solve_mod(self, i_expr=None):
        self.solve_a_type_or_expr('mod', i_expr=i_expr, mandatory=False, is_type=False)
        if self.mod and self.mod_solved and (not self.first_solved or not self.last_solved):
            self.first = str(0)
            self.last = str(int(self.mod) - 1)
            self.first_solved = True
            self.last_solved = True
