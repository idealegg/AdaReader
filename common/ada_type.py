import common.parse_util
from common.common_based import CommonBased


class AdaType(CommonBased):
    RECORD_TYPE = "Record"
    ENUM_TYPE = "Enum"
    STR_TYPE = "String"
    ARRAY_TYPE = "Array"
    DERIVED_TYPE = "Derived"
    SUBTYPE = "Subtype"
    INT_TYPE = "Integer"
    REAL_TYPE = "Real"
    FIELD_TYPE = "Field_Type"
    VAR_TYPE = "Var"
    def __init__(self, name, ttype, package=None, ctx=None, is_based=False):
        super(AdaType, self).__init__()
        self.name = name.upper() if name else None
        self.package = package.upper() if package else None
        self.ttype = ttype
        self.is_based = is_based
        self.discriminant = {}
        self.size = None
        self.ctx = ctx
        #self.ctx.cur_type = self
        self.size_solved = False
        self.const_solved = False
        self.type_chain = []
        self.first = None
        self.last = None
        self.must_print = ['first', 'last', 'size']
        self.to_print = ['discriminant', 'size']
        self.leader_str = "'%s type [%s] in [%s]:' % (self.ttype, self.name, self.package)"

    def add_discrim(self, fs):
        for f in fs:
            self.discriminant[f.name] = f

    def solve_size(self, i_size):
        self.size, self.size_solved = common.parse_util.solve_expr(self.ctx, i_size)

    def solve_type_chain(self):
        pass

    def full_name(self):
        return '.'.join([self.package, self.name])

    def solve_constraint(self):
        const = getattr(self, 'constraint', None)
        if self.const_solved or not const:
            return
        if const['type'] == 'range':
            if const['range']['type'] == 'range':
                self.first, solved1 = common.parse_util.solve_expr(self.ctx, const['range']['first'])
                self.last, solved2 = common.parse_util.solve_expr(self.ctx, const['range']['last'])
                self.const_solved = solved1 and solved2
            elif const['range']['type'] == 'attr':
                const['range']['base'], solved = common.parse_util.solve_type(self.ctx, const['range']['base'])
                if solved:
                    self.first, solved1 = common.parse_util.solve_expr(self.ctx, const['range']['base'].first)
                    self.last, solved2 = common.parse_util.solve_expr(self.ctx, const['range']['base'].last)
                    self.const_solved = solved1 and solved2
        if self.const_solved:
            setattr(self, 'constraint', None)