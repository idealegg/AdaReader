from common.ada_type import AdaType


class AdaRealType(AdaType):
    INTEGER = 0
    MODULAR = 1
    FLOAT = 2
    FIXED = 3
    def __init__(self, name, package=None, ctx=None):
        super(AdaRealType, self).__init__(name, AdaType.REAL_TYPE, package, ctx)
        self.delta = None
        self.digits = None
        self.to_print = ['delta', 'digits']