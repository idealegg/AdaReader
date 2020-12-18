from common.ada_type import AdaType


class AdaSubtype(AdaType):
    def __init__(self, name, package=None, ctx=None):
        super(AdaSubtype, self).__init__(name, AdaType.SUBTYPE, package, ctx)
        self.based = None
        self.constraint = None
        self.to_print = ['based', 'constraint', 'size']

    def parse_subscript(self):
        pass