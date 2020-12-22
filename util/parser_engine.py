# -*- coding: utf-8 -*-
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
import util.myLogging as myLogging
from util.myLogging import logger as my_log
from util.myLogging import log


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

    @log('ParseAdaCtx')
    def pop_next_fm(self):
        unsolved_package_of_files = set([x.package for x in self.files])
        depend_max = 0
        for fm in self.files:
            unsolved_withs_a_file = set(fm.unsolved_withs())
            for t_p in unsolved_withs_a_file & unsolved_package_of_files^unsolved_withs_a_file:
                fm.solve_with(t_p)
            for t_p in unsolved_withs_a_file & set(self.packages.keys()):
                fm.solve_with(t_p)
        max_depend_fm = {}
        for fm in self.files:
            unsolved_withs_a_file = set(fm.unsolved_withs())
            my_log.info("never solved withs in [%s][%s]"%(fm.f_path,
                                                          (unsolved_withs_a_file & unsolved_package_of_files) ^ unsolved_withs_a_file))
            if not(unsolved_withs_a_file & unsolved_package_of_files):
                self.files.remove(fm)
                return fm
            for t_p in unsolved_withs_a_file & unsolved_package_of_files:
                max_depend_fm [self.packages[t_p]['fm']] += 1
        return sorted(max_depend_fm.keys(), key=lambda x: max_depend_fm[x]).pop(0)

    @log('ParseAdaCtx')
    def parse(self):
        for csci in self.cscis:
            self.files = csci.get_all_spec()
            self.num_in_csci = len(self.files)
            my_log.info("Csci[%s], All files[%s][%s]"% (csci.csci, self.num_in_csci, "\n".join(self.files)))
            self.package_num_1_round = len(self.files)
            while self.files:
                f = self.files.pop(0)
                if isinstance(f, str):
                    fm = FileMng(f, self, self.listener)
                    self.packages.update({fm.package: {'fm': fm,'walked': fm.skip_walk}})
                    if fm.skip_walk:
                        self.package_num_1_round -= 1
                        my_log.info("Skip file: [%s]" % fm.f_path)
                        continue
                else:
                    fm = f
                all_withs_solved = fm.check_withs()
                if not all_withs_solved and self.package_num_1_round == 0:
                    self.files.append(fm)
                    fm = self.pop_next_fm()
                if all_withs_solved or self.package_num_1_round == 0:
                    my_log.info("Current walk file: [%s], [%s/%s/%s]" % (fm.f_path, self.package_num_1_round, len(self.files)+1, self.num_in_csci))
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

    @log('ParseAdaCtx')
    def test(self, init=True, init_pred=True, init_csci=None):
        pe = self
        if init:
            if not init_csci:
                init_csci = []
            pe.init(PreDefined(self, null=not init_pred),
                    list(map(lambda x: CsciMng(*x), init_csci))
                )
        if not init and init_csci:
            pe.cscis = list(map(lambda x: CsciMng(*x), init_csci))
        try:
            pe.parse()
        except Exception as exce:
            my_log.exception(exce)
            raise

    def print_all(self):
        for pk in  pe.types:
            for ty in pe.types[pk]:
                pe.types[pk][ty].print()
        for pk in pe.vars:
            for ty in pe.vars[pk]:
                pe.vars[pk][ty].print()

    def print_fp(self):
        pe.types['IAC_FLIGHT_PLAN_TYPES']['FLIGHT_PLAN_T'].print()


if __name__ == '__main__':
    myLogging.setup_logging()
    cscis = {'standard95': (r'D:\sourceCode\1_eurocat\standard95', 'standard95'),
             'adainclude': (r'G:\MinGW\lib\gcc\mingw32\4.9.3\adainclude', 'adainclude'),
             'ubss'      : (r'D:\sourceCode\1_eurocat\btma_ada\ubss_src', 'ubss'),
             'kinematics': (r'D:\sourceCode\1_eurocat\btma_ada\kinematics\Ada', 'kinematics', r'.'),
             'common'    : (r'D:\sourceCode\1_eurocat\btma_ada\common', 'common', r'cdc\cdc'),
             'test'      : (r'D:\pycharmProject\AdaReader\java', 'test'),
             'common_util': (r'D:\sourceCode\1_eurocat\btma_ada\common\util', 'common_util'),
             'common_cdc': (r'D:\sourceCode\1_eurocat\btma_ada\common\cdc', 'common_cdc', r'cdc'),
             }
    if 1:
        pe = ParseAdaCtx()
        pe.test(True, False, [
            #cscis['standard95'],
            #cscis['ubss'],
            #cscis['kinematics'],
            #cscis['common'],
            cscis['test'],
        ])
        pe.print_all()
    else:
        #i_csci = 'ubss'
        #i_csci = 'kinematics'
        i_csci = 'common_util'
        with open(os.path.join('run','%s.dump'%i_csci), 'rb') as fd:
            pe = pickle.load(fd)
        pe.test(False, False, [
            #cscis['common'],
            #cscis['common_util'],
            #cscis['common_cdc'],
            cscis['test'],
        ])
        if 0:
            pe.print_all()
        else:
            pe.print_fp()


