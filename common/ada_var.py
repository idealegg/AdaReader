import common.parse_util
from common.ada_type import AdaType


class AdaVar(AdaType):
    def __init__(self, name, package=None, ctx=None, value=None):
        super(AdaVar, self).__init__(name, AdaType.VAR_TYPE, package, ctx)
        self.name = name.upper() if name else None
        self.data_type = None
        self.value = value
        self.package = package.upper()
        self.const = False
        self.type_solved = False
        self.value_solved = self.value is not None
        self.ctx = ctx
        #self.ctx.cur_var = self
        self.to_print = ['data_type', 'value', 'const', 'constraint']
        self.leader_str = "'Var [%s] in [%s]:' % (self.name, self.package)"

    def solve_type(self, i_type):
        self.data_type, self.type_solved = common.parse_util.solve_type(self.ctx, i_type)

    def solve_value(self, i_val):
        self.value, self.value_solved = common.parse_util.solve_expr(self.ctx, i_val)

    def copy(self, name):
        av = AdaVar(name, self.package, self.ctx)
        av.data_type = self.data_type
        av.value = self.value
        av.const = self.const
        av.type_solved = self.type_solved
        av.value_solved = self.value_solved
        return av
