import common.parse_util
from common.ada_type import AdaType


class AdaArrayIndex(AdaType):
    def __init__(self, array_type, based, const):
        super(AdaArrayIndex, self).__init__("%s_index_%s"%(array_type.name, array_type.index_num),
                                            AdaType.ARRAY_INDEX_TYPE,
                                            None,
                                            array_type.ctx)
        self.array_type = array_type
        self.index = array_type.index_num
        self.based = based
        self.based_solved = False
        self.constraint = const
        self.const_solved = False
        #self.ctx.cur_field = self
        self.to_print = ['index', 'based_solved','based', 'range_solved', 'range']
        self.leader_str = "'Array index [%s]:' % self.name"

    def solve_based(self, i_type=None):
        if not i_type and not self.based:
            self.based_solved = True
        else:
            self.based, self.based_solved = common.parse_util.solve_type(self.ctx, i_type if i_type else self.based)

    def is_solved(self):
        return self.based_solved and self.const_solved




