from common.ada_type import AdaType


class AdaArrayType(AdaType):
    def __init__(self, name, package=None, ctx=None):
        super(AdaArrayType, self).__init__(name, AdaType.ARRAY_TYPE, package, ctx)
        self.subscript = None
        self.val_type = None

    def parse_subscript(self):
        pass