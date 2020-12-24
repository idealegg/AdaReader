from common.ada_type import AdaType


class AdaRealType(AdaType):
    INTEGER = 0
    MODULAR = 1
    FLOAT = 2
    FIXED = 3
    def __init__(self, name, package=None, ctx=None, is_based=False):
        super(AdaRealType, self).__init__(name, AdaType.REAL_TYPE, package, ctx, is_based)
        self.delta = None
        self.digits = None
        self.delta_solved = False
        self.digits_solved = False
        self.first_solved = False
        self.last_solved = False
        self.to_print = ['delta', 'digits']
        self.to_solve = ['delta', 'digits', 'first', 'last']

    def solve_first(self, i_expr=None):
        self.solve_a_type_or_expr('first', i_expr=i_expr, mandatory=False, is_type=False)

    def solve_last(self, i_expr=None):
        self.solve_a_type_or_expr('last', i_expr=i_expr, mandatory=False, is_type=False)

    def solve_delta(self, i_expr=None):
        self.solve_a_type_or_expr('delta', i_expr=i_expr, mandatory=False, is_type=False)

    def solve_digits(self, i_expr=None):
        self.solve_a_type_or_expr('digits', i_expr=i_expr, mandatory=False, is_type=False)
