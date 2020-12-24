from common.common_based import CommonBased


class AdaSpec(CommonBased):
    def __init__(self, f_name, ctx):
        super(AdaSpec, self).__init__()
        self.f_name = f_name
        self.package = None
        self.withs = set()
        self.uses = set()
        self.use_types = set()
        self.vars = {}
        self.types = {}
        self.enums = {}
        self.ctx = ctx
        #self.ctx.cur_spec = self
        self.to_print = ['f_name', 'package', 'withs', 'uses']

    def add_with(self, w):
        self.withs.update(map(lambda x: x.upper(), w))

    def add_use(self, u):
        self.uses.update(map(lambda x: x.upper(), u))

    def add_use_types(self, t):
        self.use_types.update(map(lambda x: x.upper(), t))

    def add_type(self, stype):
        if not self.types:
            self.types = {}
        if stype.package not in self.types:
            self.types[stype.package] = {}
        if stype.package not in self.ctx.types:
            self.ctx.types[stype.package] = {}
        stype.check_solved()
        self.types[stype.package][stype.name] = stype
        self.ctx.types[stype.package][stype.name] = stype

    def add_var(self, svar):
        if not self.vars:
            self.vars = {}
        if svar.package not in self.vars:
            self.vars[svar.package] = {}
        if svar.package not in self.ctx.vars:
            self.ctx.vars[svar.package] = {}
        svar.check_solved()
        self.vars[svar.package][svar.name] = svar
        self.ctx.vars[svar.package][svar.name] = svar

    def add_enum(self, senum):
        if not self.enums:
            self.enums = {}
        if senum.package not in self.enums:
            self.enums[senum.package] = {}
        if senum.package not in self.ctx.enums:
            self.ctx.enums[senum.package] = {}
        self.enums[senum.package][senum.name] = senum
        self.ctx.enums[senum.package][senum.name] = senum