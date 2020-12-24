from common.ada_type import AdaType
import common.parse_util as cpu

class AdaArrayType(AdaType):
    def __init__(self, name, package=None, ctx=None, is_based=False):
        super(AdaArrayType, self).__init__(name, AdaType.ARRAY_TYPE, package, ctx, is_based)
        self.index_list = []
        self.index_num = 0
        self.elem = None
        self.elem_solved = False
        self.must_print = ['size']
        self.to_print = ['is_based', 'index_num', 'index_list', 'elem', 'elem_solved']

    def parse_subscript(self):
        pass

    def inc_index_num(self):
        self.index_num += 1

    def add_index(self, index):
        self.index_list.append(index)
        self.inc_index_num()

    def solve_elem(self, i_expr=None):
        self.solve_a_type_or_expr('elem', i_expr=i_expr)

    def check_solved(self):
        ret = True
        if not self.elem_solved:
            self.solve_elem()
            ret = self.elem_solved and ret
        for index in self.index_list:
            ret = index.check_solved() and ret
        if ret:
            self.is_based = True
        return True
