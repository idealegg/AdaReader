from common.ada_type import AdaType
import common.parse_util


class AdaDerivedType(AdaType):
    def __init__(self, name, package=None, ctx=None):
        super(AdaDerivedType, self).__init__(name, AdaType.DERIVED_TYPE, package, ctx)
        self.based = None
        self.based_solved = False
        self.constraint = {}
        self.to_print = ['is_based', 'based_solved', 'based', 'constraint_solved', 'constraint', 'type_chain', ]
        self.to_solve = ['based', 'constraint']
        
    def solve_based(self, based=None): # call solve_constraint first
        if based:
            self.based = based
        try:
            if not self.based_solved:
                if not self.is_based and isinstance(self.based, str):
                    #print("solve_type_chain: %s"%self)
                    self.based, self.based_solved = common.parse_util.solve_type(self.ctx, self.based)
                    if self.based_solved:
                        if not self.constraint:
                            self.first = self.based.first
                            self.last = self.based.last
                        if self.based.is_based:
                            self.is_based = True
                            #print("solve_type_chain1: %s" % self.type_chain)
                            self.type_chain.append(self.based.name)
                            self.type_chain.extend(self.based.type_chain)
                            #print("solve_type_chain2: %s" % self.type_chain)
                            if getattr(self.based, 'based', None):
                                self.based = self.based.based
        except:
            self.print()
            raise

