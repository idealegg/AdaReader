import common.parse_util as cpu
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
    FIELD_TYPE = "Field"
    VAR_TYPE = "Var"
    ENUM_ITEM_TYPE = 'Enum_Item'
    ARRAY_INDEX_TYPE = 'Array_Index'
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
        self.constraint_solved = False
        self.type_chain = []
        self.first = None
        self.last = None
        self.must_print = ['first', 'last', 'size']
        self.to_print = ['discriminant', 'size']
        self.leader_str = "'%s type [%s] in [%s]:' % (self.ttype, self.name, self.package)"
        self.to_solve = []
        self.to_check = []

    def add_discrim(self, fs):
        for f in fs:
            self.discriminant[f.name] = f

    def solve_type_chain(self):
        pass

    def full_name(self):
        return '.'.join([self.package, self.name])

    def solve_a_type_or_expr(self, attr_n, i_expr=None, solved_n=None, mandatory=True, is_type=True):
        if not solved_n:
            solved_n = "%s_solved" % attr_n
        if not getattr(self, solved_n):
            if not mandatory and not i_expr and not getattr(self, attr_n):
                setattr(self, solved_n, True)
            else:
                if i_expr:
                    setattr(self, attr_n, i_expr)
                if is_type:
                    attr_v, solved_v = cpu.solve_type(self.ctx, getattr(self, attr_n))
                else:
                    attr_v, solved_v = cpu.solve_expr(self.ctx, getattr(self, attr_n))
                setattr(self, attr_n, attr_v)
                setattr(self, solved_n, solved_v)

    def solve_size(self, i_size=None):
        self.solve_a_type_or_expr('size', i_size)

    def solve_constraint(self, const=None):
        if const is not None:
            setattr(self, 'constraint', const)
        const = getattr(self, 'constraint', None)
        if self.constraint_solved or not const:
            self.constraint_solved = True
            return
        if const['type'] == 'range':
            if const['range']['type'] == 'range':
                self.first, solved1 = cpu.solve_expr(self.ctx, const['range']['first'])
                self.last, solved2 = cpu.solve_expr(self.ctx, const['range']['last'])
                self.constraint_solved = solved1 and solved2
            elif const['range']['type'] == 'attr':
                solved = True
                if isinstance(const['range']['base'], str):
                    const['range']['base'], solved = cpu.solve_type(self.ctx, const['range']['base'])
                if solved:
                    self.first, solved1 = cpu.solve_expr(self.ctx, const['range']['base'].first)
                    self.last, solved2 = cpu.solve_expr(self.ctx, const['range']['base'].last)
                    self.constraint_solved = solved1 and solved2
        #if self.constraint_solved:
        #    setattr(self, 'constraint', None)

    def check_solved(self):
        for attr in self.to_solve:
            method_n = 'solve_%s' % attr
            solved_n = '%s_solved' % attr
            if not getattr(self, solved_n):
                getattr(self, method_n)()
        ret = True
        if not self.to_check:
            self.to_check = self.to_solve
        for attr in self.to_check:
            solved_n = '%s_solved' % attr
            ret = ret and getattr(self, solved_n)
        if ret:
            self.is_based = True
        return  ret