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
        self.enums = {}
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
        for fm in self.files:
            unsolved_withs_a_file = set(fm.unsolved_withs())
            never_solved_withs = (unsolved_withs_a_file & unsolved_package_of_files)^unsolved_withs_a_file
            if never_solved_withs:
                my_log.info("never solved withs in [%s][%s]" % (fm.f_path, never_solved_withs))
            for t_p in never_solved_withs:
                fm.solve_with(t_p)
            for t_p in unsolved_withs_a_file & set(self.packages.keys()):
                fm.solve_with(t_p)
        max_depend_fm = {}
        for fm in self.files:
            unsolved_withs_a_file = set(fm.unsolved_withs())
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
            tmp_files = []
            for f in self.files:
                fm = FileMng(f, self, self.listener)
                self.packages.update({fm.package: {'fm': fm, 'walked': fm.skip_walk}})
                if fm.skip_walk:
                    my_log.info("Skip file: [%s]" % fm.f_path)
                tmp_files.append(fm)

            self.files = tmp_files
            files_num_to_walk = len(self.files)
            package_num_1_round = files_num_to_walk
            while self.files:
                fm = self.files.pop(0)
                all_withs_solved = fm.check_withs()
                if not all_withs_solved and package_num_1_round == 0:
                    self.files.append(fm)
                    fm = self.pop_next_fm()
                if all_withs_solved or package_num_1_round == 0:
                    my_log.info("Current walk file: [%s], [%s/%s/%s]" % (fm.f_path, len(self.files)+1, files_num_to_walk, self.num_in_csci))
                    self.cur_fm = fm
                    fm.walk()
                    self.packages.update({fm.package: {'fm': None,'walked': True}})
                    for ofm in self.files:
                        if not isinstance(ofm, str):
                            ofm.solve_with(fm.package)
                    package_num_1_round = len(self.files)
                else:
                    package_num_1_round -= 1
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

    def check_fp(self):
        for field in pe.types['IAC_FLIGHT_PLAN_TYPES']['FLIGHT_PLAN_T'].fpos:
            a_f = pe.types['IAC_FLIGHT_PLAN_TYPES']['FLIGHT_PLAN_T'].fields[field]
            field_type_solved = not isinstance(a_f.field_type, str)
            if not field_type_solved or not a_f.field_type.is_based:
                print('unsolved field [%s]'% a_f)
            else:
                print("filed name: [%s], filed type: [%s][%s], based:[%s], pos: [%s], start: [%s[, end; [%s]" %
                      (a_f.name,
                       isinstance(a_f.field_type, str),
                       a_f.field_type.name if field_type_solved else a_f.field_type,
                       a_f.field_type.type_chain if field_type_solved else '',
                       a_f.pos, a_f.start_bit, a_f.end_bit))



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
    if 0:
        pe = ParseAdaCtx()
        pe.test(True, False, [
            cscis['standard95'],
            cscis['ubss'],
            cscis['kinematics'],
            cscis['common_util'],
            cscis['common_cdc'],
            #cscis['test'],
        ])
        if 0:
            pe.print_all()
        else:
            #pe.print_fp()
            pe.check_fp()
    else:
        #i_csci = 'ubss'
        #i_csci = 'kinematics'
        #i_csci = 'common_util'
        i_csci = 'common_cdc'
        with open(os.path.join('run','%s.dump'%i_csci), 'rb') as fd:
            pe = pickle.load(fd)
        if 0:
            pe.test(False, False, [
                cscis['kinematics'],
                cscis['common_util'],
                cscis['common_cdc'],
                #cscis['test'],
            ])
            if 0:
                pe.print_all()
            else:
                pe.print_fp()
        else:
            if 0:
                pe.check_fp()
            else:
                pe.test(False, False, [
                    cscis['test'],
                ])
                pe.types['HD_TEST']['TEST_TYPE'].print()


