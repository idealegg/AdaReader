from common.ada_type import AdaType


class AdaRecordType(AdaType):
    def __init__(self, name, package=None, ctx=None):
        super(AdaRecordType, self).__init__(name, AdaType.RECORD_TYPE, package, ctx)
        self.fields = {}
        self.fpos = []
        self.mod_clause = None
        self.must_print = ['size']
        self.to_print = ['fpos', 'fields:fpos']
        self.join_char = [',', '\n', '\n']

    def add_fields(self, fs):
        for f in fs:
            self.fields[f.name] = f

    def add_pos(self, fn):
        self.fpos.append(fn)

    def check_solved(self):
        ret = True
        for field in self.fields.keys():
            ret = ret and self.fields[field].check_solved()
        if ret:
            self.is_based = True
        return ret

