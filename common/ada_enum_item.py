import common.parse_util
from common.ada_type import AdaType


class AdaEnumItem(AdaType):
    def __init__(self, name, enum_type, ctx=None):
        super(AdaEnumItem, self).__init__(name, AdaType.ENUM_ITEM_TYPE, enum_type.package, ctx)
        self.type = enum_type
        self.value = None
        self.value_solved = False
        self.to_print = ['value']
        self.leader_str = "'Enum item [%s]:' % self.name"

    def solve_value(self, i_val=None):
        self.solve_a_type_or_expr('value', i_expr=i_val, mandatory=False, is_type=False)



