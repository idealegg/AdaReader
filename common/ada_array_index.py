import common.parse_util
from common.ada_type import AdaType


class AdaArrayIndex(AdaType):
    def __init__(self, array_type, based, const):
        super(AdaArrayIndex, self).__init__(based if based else "%s_index_%s"%(array_type.name, array_type.index_num),
                                            AdaType.ARRAY_INDEX_TYPE,
                                            None,
                                            array_type.ctx)
        self.array_type = array_type
        self.index = array_type.index_num
        self.based = based
        self.based_solved = False
        self.constraint = const
        self.constraint_solved = False
        #self.ctx.cur_field = self
        self.to_print = ['index', 'based_solved', 'based', 'constraint_solved', 'constraint']
        self.leader_str = "'Array index [%s]:' % self.name"
        self.to_solve = ['based', 'constraint']

    def solve_based(self, i_type=None):
        self.solve_a_type_or_expr('based', i_expr=i_type, mandatory=False)





