from common.ada_type import AdaType


class AdaDerivedType(AdaType):
    def __init__(self, name, package=None, ctx=None):
        super(AdaDerivedType, self).__init__(name, AdaType.DERIVED_TYPE, package, ctx)
        self.based = None
        self.constraint = None
        self.to_print = ['based', 'constraint', 'size']

    def parse_subscript(self):
        pass