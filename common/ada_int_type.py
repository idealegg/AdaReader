from common.ada_type import AdaType


class AdaIntType(AdaType):
    INTEGER = 0
    MODULAR = 1
    FLOAT = 2
    FIXED = 3
    def __init__(self, name, package=None, ctx=None, is_based=False, mod=None, first=None, last=None):
        super(AdaIntType, self).__init__(name, AdaType.INT_TYPE, package, ctx, is_based)
        self.mod = mod
        if first:
            self.first = first
        if last:
            self.last = last
        if self.mod:
            self.first = str(0)
            self.last = str(int(self.mod) - 1)
        self.to_print = ['mod']