from common.ada_type import AdaType


class AdaEnumType(AdaType):
    def __init__(self, name, package=None, ctx=None):
        super(AdaEnumType, self).__init__(name, AdaType.ENUM_TYPE, package, ctx)
        self.enums = []
        self.values = {}
        self.is_based = True
        self.to_print = ['is_based', 'enums', 'values:enums']

    def get_pos(self, enum): # pos is index, value is for storing.
        try:
            index = self.enums.index(enum.upper())
        except ValueError:
            index = -1
        return index

    def get_value(self, enum):
        try:
            index = self.enums.index(enum.upper())
        except ValueError:
            index = -1
        return self.values[index]

    def add_enum(self, enums):
        self.enums.extend(map(lambda x: x.upper(), enums))

    def add_val(self, enum, val):
        self.values[enum.upper()] = val

    def add_val2(self, enum, val):
        try:
            index = self.enums.index(enum.upper())
        except ValueError:
            return
        if not self.values:
            self.values = [-1] * len(self.enums)
        self.values[index] = val

