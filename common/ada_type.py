import common.parse_util


class AdaType:
    RECORD_TYPE = "Record"
    ENUM_TYPE = "Enum"
    STR_TYPE = "String"
    NUM_TYPE = "Number"
    ARRAY_TYPE = "Array"
    DERIVED_TYPE = "Derived"
    SUBTYPE = "Subtype"
    def __init__(self, name, ttype, package=None, ctx=None):
        self.name = name
        self.package = package
        self.ttype = ttype
        self.discriminant = {}
        self.size = None
        self.ctx = ctx
        self.ctx.cur_type = self
        self.size_solved = False
        self.to_print = ['discriminant', 'size']

    def add_discrim(self, f):
        self.discriminant[f.name] = f

    def solve_size(self, i_size):
        self.size, self.size_solved = common.parse_util.solve_expr(self.ctx, i_size)

    def __str__(self):
        out = []
        for attr in self.to_print:
            key = None
            if attr.count(':'):
                attr, key = attr.split(":")
            if attr == 'size' and not self.size_solved:
                continue
            if attr == 'discriminant' and not self.discriminant:
                continue
            attr_v = getattr(self, attr, None)
            if isinstance(attr_v, (list, set, tuple)):
                out.append("%s: [%s]" %(attr, ",".join(map(str, attr_v))))
            elif isinstance(attr_v, dict):
                keys = attr_v.keys()
                if key:
                    keys = getattr(self, key, None)
                    if not keys or len(key) != len(attr_v.keys()):
                        keys = attr_v.keys()
                out.append("%s:\n{%s}" % (attr, "\n".join(map(lambda x: "%s: %s" %(x, attr_v[x]), keys))))
            else:
                out.append("%s: %s" % (attr, attr_v))
        return "%s type [%s] in [%s]:\n{%s}" % (self.ttype, self.name, self.package, "\n".join(out))

    def print(self):
        print(self)