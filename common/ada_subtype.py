from common.ada_type import AdaType
import common.parse_util


class AdaSubtype(AdaType):
    def __init__(self, name, package=None, ctx=None):
        super(AdaSubtype, self).__init__(name, AdaType.SUBTYPE, package, ctx)
        self.based = None
        self.constraint = {}
        self.to_print = ['based', 'constraint', 'type_chain', 'is_based']

    def solve_type_chain(self):
        if not self.is_based and isinstance(self.based, str):
            self.based, solved = common.parse_util.solve_type(self.ctx, self.based)
        if not isinstance(self.based, str):
            if not self.constraint and not self.const_solved:
                self.first = self.based.first
                self.last = self.based.last
                self.const_solved = True
            if self.based.is_based:
                self.is_based = True
                self.type_chain.append(self.based.name)
                self.type_chain.extend(self.based.type_chain)

