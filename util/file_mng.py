import os
import sys
from antlr4 import *
from run.ADA95Lexer import ADA95Lexer
from run.ADA95Parser import ADA95Parser
import common.parse_util as cpu
from common.common_based import CommonBased
from enum import Enum


class FileMng(CommonBased):
    States = Enum('States',
                  ('FILE',
                   'PACKAGE',
                   'VAR',
                   'VAR_TYPE',
                   'VAR_VALUE',
                   'TYPE',
                   'SUB_DER_TYPE',
                   'DISCRIMINANT',
                   'FIELD',
                   'FIELD_TYPE',
    #               'FIELD_VALUE',
                   'POS',
                   'POS_FIELD',
                   'ATTR'))
    def __init__(self, f_path, ctx=None, listener=None):
        super(FileMng, self).__init__()
        self.f_path = f_path
        self.dir_name = os.path.dirname(f_path)
        self.f_name = os.path.basename(f_path)
        self.ctx = ctx
        self.ctx.cur_fm = self
        self.package = None
        self.istream = None
        self.lexer = None
        self.stream = None
        self.parser = None
        self.tree = None
        self.walker = None
        self.withs = set()
        self.solved_withs = {}
        self.uses = set()
        self.use_types = set()
        self.istream = FileStream(self.f_path)
        self.lexer = ADA95Lexer(self.istream)
        self.stream = CommonTokenStream(self.lexer)
        self.parser = ADA95Parser(self.stream)
        self.tree = self.parser.compilation()
        self.cur_states = [FileMng.States.FILE]
        self.to_print = ['f_path', 'cur_states']
        self.leader_str = '[%s:%s]'%(self.tree.start.start, self.tree.stop.stop)
        self.listener = listener

        culs = self.tree.compilation_unit()
        if len(culs) >= 1:
            cis = culs[0].context_item()
            for ci in cis:
                wc = ci.with_clause()
                if wc:
                    map(lambda x: self.solved_withs.update({x.upper(): self.ctx.check_with(x.upper())}),
                            cpu.get_texts(wc.library_unit_name()))
            self.withs = set(self.solved_withs.keys())
            li = culs[0].library_item()
            if li:
                lud = li.library_unit_declaration()
                if lud:
                    pd = lud.package_declaration()
                    if pd:
                        self.package = cpu.get_texts(pd.package_specification().defining_program_unit_name()).upper()

    def add_with(self, w):
        self.withs.update(map(lambda x: x.upper(), w))

    def add_use(self, u):
        self.uses.update(map(lambda x: x.upper(), u))

    def add_use_types(self, t):
        self.use_types.update(map(lambda x: x.upper(), t))

    def check_withs(self):

        unsolved = list(filter(lambda x: not self.solved_withs[x], self.withs))
        return not unsolved

    def walk(self):
        try:
            walker = ParseTreeWalker()
            walker.walk(self.listener, self.tree)
        except:
            self.print()
            raise

