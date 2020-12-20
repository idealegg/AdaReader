import os
import sys
from antlr4 import *
from run.ADA95Lexer import ADA95Lexer
from run.ADA95Parser import ADA95Parser
from run.ADA95Listener3 import ADA95Listener3

class FileMng:
    def __init__(self, f_path, ctx=None):
        self.f_path = f_path
        self.dir_name = os.path.dirname(f_path)
        self.f_name = os.path.basename(f_path)
        self.ctx = ctx
        self.package = None
        self.istream = None
        self.lexer = None
        self.stream = None
        self.parser = None
        self.tree = None
        self.walker = None
        self.withs =[]

    def parse(self):
        self.istream = FileStream(self.f_path)
        self.lexer = ADA95Lexer(self.istream)
        self.stream = CommonTokenStream(self.lexer)
        self.parser = ADA95Parser(self.stream)
        self.parser.ada_ctx = self.ctx
        self.tree = self.parser.compilation()

    def get_withs(self):
        culs = self.tree.compilation_unit_lib()
        if len(culs) == 1:
            cis = culs[0].context_item()
            for ci in cis:
                wcs = ci.with_clause()
                for wc in wcs:
                    self.withs.extend(map(lambda x: x.upper(), wc.library_unit_name()))

    def walk(self):
        walker = ParseTreeWalker()
        walker.walk(ADA95Listener3(), self.tree)
        self.package = self.ctx.cur_spec.package