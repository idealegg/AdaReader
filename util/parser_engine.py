import sys
from antlr4 import *
from run.ADA95Lexer import ADA95Lexer
from run.ADA95Parser import ADA95Parser
from run.ADA95Listener3 import ADA95Listener3

import pprint
from util.perdefined import PreDefined
from util.csci_mng import CsciMng
from util.file_mng import FileMng


class ParseAdaCtx:
    def __init__(self):
        self.vars = {}
        self.types = {}
        self.unsolved = {}
        self.cscis = []
        self.files = []
        self.cur_spec = None
        self.cur_var = None
        self.cur_type = None
        self.cur_discrim = None
        self.cur_idents = None
        self.cur_field = None
        self.cur_range = None
        self.cur_const = None
        self.cur_spec_list = []
        self.cur_fm = None
        self.packages = {}
        self.listener = ADA95Listener3(self)

    def init(self, pred:PreDefined, cscis):
        self.vars = pred.vars
        self.types = pred.types
        self.cscis = cscis

    def init_cur(self):
        self.cur_spec = None
        self.cur_var = None
        self.cur_type = None
        self.cur_discrim = None
        self.cur_idents = None
        self.cur_field = None
        self.cur_range = None
        self.cur_const = None
        self.cur_spec_list = []
        self.cur_fm = None

    def check_with(self, package):
        return  package in self.packages

    def parse(self):
        for csci in self.cscis:
            self.files.extend(csci.get_all_spec())
        print("\n".join(self.files))
        while self.files:
            f = self.files.pop(0)
            if isinstance(f, str):
                fm = FileMng(f, self, self.listener)
            else:
                fm = f
            if not isinstance(f, str) and not self.packages or fm.check_withs():
                print(fm.f_path)
                fm.walk()
                self.packages.update({fm.package: fm.f_path})
            else:
                self.files.append(fm)
            self.init_cur()


    def test(self):
        pe = self
        pe.init(PreDefined(self),
                [
                    #CsciMng(r'G:\MinGW\lib\gcc\mingw32\4.9.3\adainclude', 'adainclude'),
                    CsciMng(r'C:\works\btma_code\ubss_src', 'ubss'),
                    #CsciMng(r'C:\works\btma_code\kinematics\Ada', 'kinematics'),
                    #CsciMng(r'C:\works\btma_code\common', 'common', r'C:\works\btma_code\common\cdc\cdc')
                ]
                )
        pe.parse()

        for pk in  pe.types:
            for ty in pe.types[pk]:
                pe.types[pk][ty].print()
        for pk in pe.vars:
            for ty in pe.vars[pk]:
                pe.vars[pk][ty].print()

if __name__ == '__main__':
    pe = ParseAdaCtx()
    pe.test()

