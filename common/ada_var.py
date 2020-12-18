import common.parse_util


class AdaVar:
    def __init__(self, name, package=None, ctx=None):
        self.name = name
        self.data_type = None
        self.value = None
        self.package = package
        self.const = False
        self.type_solved = False
        self.value_solved = False
        self.ctx = ctx
        self.ctx.cur_var = self

    def solve_type(self, i_type):
        self.data_type, self.type_solved = common.parse_util.solve_type(self.ctx, i_type)

    def solve_value(self, i_val):
        self.value, self.value_solved = common.parse_util.solve_expr(self.ctx, i_val)