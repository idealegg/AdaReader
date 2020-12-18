from common.ada_type import AdaType


class AdaStrType(AdaType):
    def __init__(self, name, package=None, ctx=None):
        super(AdaStrType, self).__init__( name, AdaType.STR_TYPE, package, ctx)
        self.length = None
