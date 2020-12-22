import common.parse_util
from common.ada_type import AdaType


class AdaEnumItem(AdaType):
    def __init__(self, name, enum_type, ctx=None):
        super(AdaEnumItem, self).__init__(name, AdaType.ENUM_ITEM_TYPE, None, ctx)
        self.type = enum_type
        self.value = None
        self.value_solved = False
        self.ctx = ctx
        #self.ctx.cur_field = self
        self.to_print = ['type', 'value_solved', 'value']
        self.leader_str = "'Enum item [%s]:' % self.name"

    def solve_type(self, i_type):
        self.field_type, self.type_solved = common.parse_util.solve_type(self.ctx, i_type)

    def solve_value(self, i_val):
        self.value, value_solved= common.parse_util.solve_expr(self.ctx, i_val)


