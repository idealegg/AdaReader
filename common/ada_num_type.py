from common.ada_type import AdaType


class AdaNumType(AdaType):
    INTEGER = 0
    MODULAR = 1
    FLOAT = 2
    FIXED = 3
    def __init__(self, name, package=None, ctx=None):
        super(AdaNumType, self).__init__(name, AdaType.NUM_TYPE, package, ctx)
        self.first = None
        self.last = None
        self.bits = None
        self.dtype = None