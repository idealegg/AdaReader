class AdaSpec:
    def __init__(self, f_name, ctx):
        self.f_name = f_name
        self.package = None
        self.with_list = set()
        self.use_list = set()
        self.use_types = set()
        self.vars = {}
        self.types = {}
        self.ctx = ctx
        self.ctx.cur_spec = self

    def add_with(self, w):
        self.with_list.update(w)

    def add_use(self, u):
        self.use_list.update(u)

    def add_use_types(self, t):
        self.use_types.update(t)

    def add_type(self, stype):
        if not self.types:
            self.types = {}
        if stype.package not in self.types:
            self.types[stype.package] = {}
        if stype.package not in self.ctx.types:
            self.ctx.types[stype.package] = {}
        self.types[stype.package][stype.name] = stype
        self.ctx.types[stype.package][stype.name] = stype

    def add_var(self, svar):
        if not self.vars:
            self.vars = {}
        if svar.package not in self.vars:
            self.vars[svar.package] = {}
        if svar.package not in self.ctx.vars:
            self.ctx.vars[svar.package] = {}
        self.ctx.vars[svar.package][svar.name] = svar