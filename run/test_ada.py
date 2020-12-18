import sys
from antlr4 import *
from ADA95Lexer import ADA95Lexer
from ADA95Parser import ADA95Parser
from ADA95Listener2 import ADA95Listener2

def main(argv):
    istream = FileStream(argv[1])
    lexer = ADA95Lexer(istream)
    stream = CommonTokenStream(lexer)
    parser = ADA95Parser(stream)
    tree = parser.compilation()
    #print(tree.toStringTree(recog=parser))

    walker = ParseTreeWalker()
    walker.walk(ADA95Listener2(), tree)
    print()

if __name__ == '__main__':
    #main(sys.argv)
    #main([0, r'D:\pycharmProject\AdaReader\ada_parser\iac_flight_plan_types.a'])
    main([0, r'D:\pycharmProject\AdaReader\ada_parser\python\iac_flight_plan_types'])

