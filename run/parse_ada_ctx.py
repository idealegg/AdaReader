import sys
from antlr4 import *
from run.ADA95Lexer import ADA95Lexer
from run.ADA95Parser import ADA95Parser
from run.ADA95Listener3 import ADA95Listener3
from common.ada_var import AdaVar
import pprint


class ParseAdaCtx:
    def __init__(self):
        av = AdaVar('OCTET', 'STANDARD_TYPES', self)
        av.solve_value('8')
        self.vars = {'STANDARD_TYPES':{'OCTET': av}}
        self.types = {}
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
    parser.ada_ctx = ParseAdaCtx()
    tree = parser.compilation()
    #print(tree.toStringTree(recog=parser))

    walker = ParseTreeWalker()
    walker.walk(ADA95Listener3(), tree)
    for pk in  parser.ada_ctx.types:
        for ty in parser.ada_ctx.types[pk]:
            parser.ada_ctx.types[pk][ty].print()
    pprint.pprint(parser.ada_ctx.vars)

if __name__ == '__main__':
    #main(sys.argv)
    #main([0, r'D:\pycharmProject\AdaReader\run\iac_flight_plan_types.a'])
    main([0, r'D:\pycharmProject\AdaReader\run\iac_flight_plan_types.a'])

