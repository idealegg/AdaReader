import common.parse_util
from common.ada_type import AdaType


class AdaRecordField(AdaType):
    def __init__(self, name, record_type, ctx=None):
        super(AdaRecordField, self).__init__(name, AdaType.FIELD_TYPE, None, ctx)
        self.record_type = record_type
        self.field_type = None
        self.default = None
        self.default_solved = False
        self.pos = None
        self.start_bit = None
        self.end_bit = None
        self.field_type_solved = False
        self.pos_solved = False
        self.start_bit_solved = False
        self.end_bit_solved = False
        self.based = None
        self.constraint= None
        #self.ctx.cur_field = self
        self.to_print = ['field_type', 'pos', 'start_bit', 'end_bit', 'constraint']
        self.leader_str = "'Field [%s]:' % self.name"
        #self.to_solve = ['field_type', 'pos', 'start_bit', 'end_bit', 'default']
        self.to_solve = ['field_type', 'default']
        self.to_check =['field_type']

    def solve_field_type(self, i_type=None):
        self.solve_a_type_or_expr('field_type', i_expr=i_type)

    def solve_default(self, i_val=None):
        self.solve_a_type_or_expr('default', i_expr=i_val, mandatory=False, is_type=False)

    def solve_pos(self, i_pos=None):
        self.solve_a_type_or_expr('pos', i_expr=i_pos, mandatory=False, is_type=False)

    def solve_start_bit(self, i_bit=None):
        self.solve_a_type_or_expr('start_bit', i_expr=i_bit, mandatory=False, is_type=False)

    def solve_end_bit(self, i_bit=None):
        self.solve_a_type_or_expr('end_bit', i_expr=i_bit, mandatory=False, is_type=False)

    def copy(self, name):
        arf = AdaRecordField(name.upper(), self.record_type, self.ctx)
        arf.copy_from_class(self, ['field_type', 'default', 'type_solved', 'based', 'constraint', 'first', 'last'])
        return arf

