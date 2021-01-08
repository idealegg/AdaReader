from common.ada_type import AdaType


class AdaEnumType(AdaType):
    def __init__(self, name, package=None, ctx=None):
        super(AdaEnumType, self).__init__(name, AdaType.ENUM_TYPE, package, ctx)
        self.enums = []
        self.items = {}
        self.is_based = True
        self.must_print = ['size']
        self.to_print = ['is_based', 'items:enums']

    def get_pos(self, enum): # pos is index, value is for storing.
        try:
            index = self.enums.index(enum.upper())
        except ValueError:
            index = -1
        return index

    def get_value(self, enum):
        return self.items[enum].value

    def add_enum(self, e):
        self.enums.append(e.name)
        self.items[e.name] = e

    def add_val2(self, enum, val):
        try:
            index = self.enums.index(enum.upper())
        except ValueError:
            return
        if not self.values:
            self.values = [-1] * len(self.enums)
        self.values[index] = val

