from common.ada_type import AdaType


class AdaArrayType(AdaType):
    def __init__(self, name, package=None, ctx=None, is_based=False):
        super(AdaArrayType, self).__init__(name, AdaType.ARRAY_TYPE, package, ctx, is_based)
        self.dim_list = []
        self.elem = None
        self.to_print = ['dim_list', 'elem']

    def parse_subscript(self):
        pass

    def add_dim(self, dim):
        self.dim_list.append(dim)