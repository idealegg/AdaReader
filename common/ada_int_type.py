from common.ada_type import AdaType


class AdaIntType(AdaType):
    INTEGER = 0
    MODULAR = 1
    FLOAT = 2
    FIXED = 3
    def __init__(self, name, package=None, ctx=None):
        super(AdaIntType, self).__init__(name, AdaType.INT_TYPE, package, ctx)
        self.mod = None
        self.to_print = ['mod']