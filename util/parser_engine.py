import os
from antlr4 import *
from run.ADA95Lexer import ADA95Lexer
from run.ADA95Parser import ADA95Parser
from run.ADA95Listener3 import ADA95Listener3

import pprint
from util.perdefined import PreDefined
from util.csci_mng import CsciMng
from util.file_mng import FileMng
import pickle


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
        self.package_num_1_round = 0
        self.num_in_csci = None
        self.listener = ADA95Listener3(self)

    def init(self, pred:PreDefined, cscis):
        self.vars = pred.vars
        self.types = pred.types
        for package in self.vars:
            self.packages.update({package: {'fm': None, 'walked': True}})
        for package in self.types:
            self.packages.update({package: {'fm': None, 'walked': True}})
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
        return  package in self.packages and self.packages[package]['walked']

    def pop_next_fm(self):
        unsolved_package_of_files = set([x.package for x in self.files])
        depend_max = 0
        for fm in self.files:
            unsolved_withs_a_file = set(fm.unsolved_withs())
            for t_p in unsolved_withs_a_file & unsolved_package_of_files^unsolved_withs_a_file:
                fm.solve_with(t_p)
            for t_p in unsolved_withs_a_file & set(self.packages.keys()):
                fm.solve_with(t_p)
        max_depend_fm = None
        for fm in self.files:
            unsolved_withs_a_file = set(fm.unsolved_withs())
            if unsolved_withs_a_file & unsolved_package_of_files:
                self.files.remove(fm)
                return fm
            if depend_max < len(unsolved_withs_a_file):
                depend_max = len(unsolved_withs_a_file)
                max_depend_fm = fm
        if max_depend_fm:
            self.files.remove(max_depend_fm)
            return max_depend_fm
        else:
            return self.files.pop(0)


    def parse(self):
        for csci in self.cscis:
            self.files = csci.get_all_spec()
            self.num_in_csci = len(self.files)
            print("Csci[%s]All files[%s][%s]"% (csci.csci, self.num_in_csci, "\n".join(self.files)))
            self.package_num_1_round = len(self.files)
            while self.files:
                f = self.files.pop(0)
                if isinstance(f, str):
                    fm = FileMng(f, self, self.listener)
                    self.packages.update({fm.package: {'fm': fm,'walked': False}})
                else:
                    fm = f
                all_withs_solved = fm.check_withs()
                if not all_withs_solved and self.package_num_1_round == 0:
                    self.files.append(fm)
                    fm = self.pop_next_fm()
                if all_withs_solved or self.package_num_1_round == 0:
                    print("Current walk file: [%s], [%s/%s/%s]" % (fm.f_path, self.package_num_1_round, len(self.files)+1, self.num_in_csci))
                    self.cur_fm = fm
                    fm.walk()
                    self.packages.update({fm.package: {'fm': None,'walked': True}})
                    for ofm in self.files:
                        if not isinstance(ofm, str):
                            ofm.solve_with(fm.package)
                    self.package_num_1_round = len(self.files)
                else:
                    self.package_num_1_round -= 1
                    self.files.append(fm)
                self.init_cur()
            self.save(csci.csci)

    def save(self, csci):
        with open(os.path.join('run', "%s.dump" % csci), 'wb') as fd:
            pickle.dump(self, fd)

    def test(self):
        pe = self
        pe.init(PreDefined(self),
                [
                    #CsciMng(r'G:\MinGW\lib\gcc\mingw32\4.9.3\adainclude', 'adainclude'),
                    CsciMng(r'D:\sourceCode\1_eurocat\btma_ada\ubss_src', 'ubss'),
                    #CsciMng(r'D:\pycharmProject\AdaReader\java', 'test'),
                    CsciMng(r'D:\sourceCode\1_eurocat\btma_ada\kinematics\Ada', 'kinematics'),
                    CsciMng(r'D:\sourceCode\1_eurocat\btma_ada\common', 'common', r'C:\works\btma_code\common\cdc\cdc')
                ]
                )
        pe.parse()

        if 0:
            for pk in  pe.types:
                for ty in pe.types[pk]:
                    pe.types[pk][ty].print()
            for pk in pe.vars:
                for ty in pe.vars[pk]:
                    pe.vars[pk][ty].print()
        else:
            pe.types['IAC_FLIGHT_PLAN_TYPES']['FLIGHT_PLAN_T'].print()

if __name__ == '__main__':
    pe = ParseAdaCtx()
    pe.test()

