import common.parse_util
from common.common_based import CommonBased


class AdaRecordField(CommonBased):
    def __init__(self, name, record_type, ctx=None):
        super(AdaRecordField, self).__init__()
        self.name = name.upper()
        self.record_type = record_type
        self.field_type = None
        self.default_value = None
        self.const = False
        self.pos = None
        self.start_bit = None
        self.end_bit = None
        self.type_solved = False
        self.pos_solved = False
        self.start_bit_solved = False
        self.end_bit_solved = False
        self.ctx = ctx
        #self.ctx.cur_field = self
        self.to_print = ['field_type', 'default_value', 'pos', 'start_bit', 'end_bit']

    def solve_type(self, i_type):
        self.field_type, self.type_solved = common.parse_util.solve_type(self.ctx, i_type)

    def solve_default(self, i_val):
        self.default_value, dummy= common.parse_util.solve_expr(self.ctx, i_val)

    def solve_pos(self, i_pos):
        self.pos, self.pos_solved = common.parse_util.solve_expr(self.ctx, i_pos)

    def solve_start_bit(self, i_bit):
        self.start_bit, self.start_bit_solved = common.parse_util.solve_expr(self.ctx, i_bit)

    def solve_end_bit(self, i_bit):
        self.end_bit, self.end_bit_solved = common.parse_util.solve_expr(self.ctx, i_bit)

    def update(self, f):
        self.solve_pos(f['pos'])
        self.solve_start_bit(f['start'])
        self.solve_end_bit(f['end'])

    def copy(self, name):
        arf = AdaRecordField(name.upper(), self.record_type, self.ctx)
        arf.field_type = self.field_type
        arf.default_value = self.default_value
        arf.const = self.const
        arf.pos = self.pos
        arf.start_bit = self.start_bit
        arf.end_bit = self.end_bit
        arf.type_solved = self.type_solved
        arf.pos_solved = self.pos_solved
        arf.start_bit_solved = self.start_bit_solved
        arf.end_bit_solved = self.end_bit_solved
        arf.ctx = self.ctx
        return arf

