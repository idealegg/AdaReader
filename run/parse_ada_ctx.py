import sys
from antlr4 import *
from run.ADA95Lexer import ADA95Lexer
from run.ADA95Parser import ADA95Parser
from run.ADA95Listener3 import ADA95Listener3
from common.ada_var import AdaVar
from common.ada_type import AdaType
from common.ada_int_type import AdaIntType
from common.ada_real_type import AdaRealType
from common.ada_array_type import AdaArrayType
from common.parse_util import ADA_SYSTEM_DEFINED
from common.ada_enum_type import AdaEnumType
import pprint


class ParseAdaCtx:
    def __init__(self):
        av = AdaVar('OCTET', 'STANDARD_TYPES', self)
        av.solve_value('8')
        ait = AdaIntType('INTEGER', ADA_SYSTEM_DEFINED, self)
        ait.first = str(-0x7fffffff - 1)
        ait.last = str(0x7fffffff)
        ait.is_based = True
        art1 = AdaRealType('SHORT_FLOAT', ADA_SYSTEM_DEFINED, self)
        art2 = AdaRealType('LONG_FLOAT', ADA_SYSTEM_DEFINED, self)
        ast = AdaArrayType('STRING', ADA_SYSTEM_DEFINED, self)
        art1.is_based = True
        art2.is_based = True
        ast.is_based = True
        #self.vars = {'STANDARD_TYPES':{'OCTET': av}}
        self.vars = {}
        self.types = {'ADA_SYSTEM_DEFINED': {'INTEGER': ait, 'SHORT_FLOAT': art1, 'LONG_FLOAT': art2, 'STRING': ast}}
        #self.types = {}
        self.unsolved = {}
        self.cur_spec = None
        self.cur_var = None
        self.cur_type = None
        self.cur_discrim = None
        self.cur_idents = None
        self.cur_field = None
        self.cur_range = None
        self.cur_const = None


def main(argv):
    istream = FileStream(argv[1])
    lexer = ADA95Lexer(istream)
    stream = CommonTokenStream(lexer)
    parser = ADA95Parser(stream)
    tree = parser.compilation()
    #print(tree.toStringTree(recog=parser))

    walker = ParseTreeWalker()
    walker.walk(ADA95Listener3(ParseAdaCtx()), tree)
    for pk in  parser.ada_ctx.types:
        for ty in parser.ada_ctx.types[pk]:
            parser.ada_ctx.types[pk][ty].print()
    for pk in parser.ada_ctx.vars:
        for ty in parser.ada_ctx.vars[pk]:
            parser.ada_ctx.vars[pk][ty].print()

if __name__ == '__main__':
    #main(sys.argv)
    #main([0, r'C:\works\AdaReader\run\iac_flight_plan_types.a'])
    #main([0, r'C:\works\AdaReader\run\iac_flight_plan_types.a'])
    #main([0, r'C:\works\AdaReader\run\standard_types.ads'])
    #main([0, r'C:\works\btma_code\ubss_src\artts.ads'])
    main([0, r'C:\works\AdaReader\java\test_input'])

