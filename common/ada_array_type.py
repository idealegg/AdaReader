from common.ada_type import AdaType
import common.parse_util as cpu

class AdaArrayType(AdaType):
    def __init__(self, name, package=None, ctx=None, is_based=False):
        super(AdaArrayType, self).__init__(name, AdaType.ARRAY_TYPE, package, ctx, is_based)
        self.index_list = []
        self.index_num = 0
        self.elem = None
        self.elem_solved = False
        self.to_print = ['is_based', 'index_num', 'index_list', 'elem', 'elem_solved']

    def parse_subscript(self):
        pass

    def inc_index_num(self):
        self.index_num += 1

    def add_index(self, index):
        self.index_list.append(index)
        self.inc_index_num()

    def solve_elem_type(self, i_expr=None):
        self.elem, self.elem_solved = cpu.solve_type(self.ctx, i_expr if i_expr else self.elem)

    def is_solved(self):
        if not self.elem_solved:
            return False
        for index in self.index_list:
            if not index.is_solved():
                return False
        self.is_based = True
        return True
