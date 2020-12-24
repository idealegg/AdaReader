import common.parse_util
from common.ada_type import AdaType


class AdaVar(AdaType):
    def __init__(self, name, package=None, ctx=None, value=None):
        super(AdaVar, self).__init__(name, AdaType.VAR_TYPE, package, ctx)
        self.name = name.upper() if name else None
        self.data_type = None
        self.value = value
        self.package = package.upper()
        self.data_type_solved = False
        self.value_solved = self.value is not None
        self.ctx = ctx
        #self.ctx.cur_var = self
        self.must_print = []
        self.to_print = ['data_type', 'value', 'constraint']
        self.leader_str = "'Var [%s] in [%s]:' % (self.name, self.package)"
        self.to_solve = ['constraint', 'data_type', 'value']

    def solve_data_type(self, i_type=None):
        self.solve_a_type_or_expr('data_type', i_expr=i_type, mandatory=False)

    def solve_value(self, i_val=None):
        self.solve_a_type_or_expr('value', i_expr=i_val, mandatory=False, is_type=False)

    def copy(self, name):
        av = AdaVar(name, self.package, self.ctx)
        av.copy_from_class(self, ['data_type', 'value', 'data_type_solved', 'value_solved'])
        return av
