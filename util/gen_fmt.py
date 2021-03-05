# -*- coding: utf-8 -*-
from common.ada_type import AdaType
import struct
from functools import reduce
import os
import pickle
from util.parser_engine import ParseAdaCtx
import binascii as bs
import itertools
import pprint
import copy
from util.myLogging import setup_logging
from util.myLogging import logger as my_log
from util.myLogging import log
import time
import json


flag_map = {'@': {'Byte order': u'本机', 'Size': u'本机', 'Alignment': u'本机,凑够4字节'},
            '=': {'Byte order': u'本机', 'Size': u'标准', 'Alignment': u'none,按原字节数'},
            '<': {'Byte order': u'小端', 'Size': u'标准', 'Alignment': u'none,按原字节数'},
            '>': {'Byte order': u'大端', 'Size': u'标准', 'Alignment': u'none,按原字节数'},
            '!': {'Byte order': u'network(大端)', 'Size': u'标准', 'Alignment': u'none,按原字节数'},
            }
format_map = {'x': {'C': u'pad byte(填充字节)', 'Python': 'no value', 'Ada': None, 'size': None},
              'c': {'C': u'char', 'Python': 'string of length 1', 'Ada': 'CHARACTER', 'size': 1},
              'b': {'C': u'signed char', 'Python': 'integer', 'Ada': 'SHORT_SHORT_INTEGER', 'size': 1},
              'B': {'C': u'unsigned char', 'Python': 'integer', 'Ada': None, 'size': 1},
              '?': {'C': u'_Bool', 'Python': 'bool', 'Ada': 'BOOLEAN', 'size': 1},
              'h': {'C': u'short', 'Python': 'integer', 'Ada': 'SHORT_INTEGER', 'size': 2},
              'H': {'C': u'unsigned short', 'Python': 'integer', 'Ada': None, 'size': 2},
              'i': {'C': u'int', 'Python': 'integer', 'Ada': 'INTEGER', 'size': 4},
              'I': {'C': u'unsigned int', 'Python': 'integer', 'Ada': None, 'size': 4},
              'l': {'C': u'long', 'Python': 'integer', 'Ada': 'LONG_INTEGER', 'size': 4},
              'L': {'C': u'unsigned long', 'Python': 'long', 'Ada': None, 'size': 4},
              'q': {'C': u'long long', 'Python': 'long', 'Ada': 'LONG_LONG_INTEGER', 'size': 8},
              'Q': {'C': u'unsigned long long', 'Python': 'long', 'Ada': None, 'size': 8},
              'f': {'C': u'float', 'Python': 'float', 'Ada': 'FLOAT', 'size': 4},
              'd': {'C': u'double', 'Python': 'float', 'Ada': 'LONG_FLOAT', 'size': 8},
              's': {'C': u'char[]', 'Python': 'string', 'Ada': 'STRING', 'size': None},
              'p': {'C': u'char[]', 'Python': 'string', 'Ada': None, 'size': None},
              'P': {'C': u'void *', 'Python': 'long', 'Ada': None, 'size': None},
              }

ada_type_map = {'CHARACTER': {'C': 'char', 'Python': 'string of length 1', 'size': 1, 'struct': 'c'},
                'SHORT_SHORT_INTEGER': {'C': 'signed char', 'Python': 'integer', 'size': 1, 'struct': 'b'},
                'BOOLEAN': {'C': '_Bool', 'Python': 'bool', 'size': 1, 'struct': '?'},
                'SHORT_INTEGER': {'C': 'short', 'Python': 'integer', 'size': 2, 'struct': 'h'},
                'INTEGER': {'C': 'int', 'Python': 'integer', 'size': 4, 'struct': 'i'},
                'LONG_INTEGER': {'C': 'long', 'Python': 'integer', 'size': 4, 'struct': 'l'},
                'LONG_LONG_INTEGER': {'C': 'long long', 'Python': 'long', 'size': 8, 'struct': 'q'},
                'FLOAT': {'C': 'float', 'Python': 'float', 'size': 4, 'struct': 'f'},
                'LONG_FLOAT': {'C': 'double', 'Python': 'float', 'size': 8, 'struct': 'd'},
                'STRING': {'C': 'char[]', 'Python': 'string', 'size': None, 'struct': 's'}}


class GenFmt:
    def __init__(self, base):
        self.base = base
        self.pos_stack = [0]
        self.name_stack = []
        self.result = {'gen_fmt_enums':{}}
        self.enums = {}
        #self.elem_size_stack = []

    @log('GenFmt')
    def get_pos(self, f_p):
        my_log.debug("get_pos: %s" % self.pos_stack)
        return reduce(lambda x, y: x+y, self.pos_stack) + f_p

    @log('GenFmt')
    def get_name(self, f_n):
        my_log.debug("get_name: %s" % self.name_stack)
        #return "%s.%s" % (reduce(lambda x, y: ".".join([x, y]), self.name_stack), f_n) if self.name_stack else f_n
        return f_n

    @staticmethod
    def get_struct(ot, ch_num=None):
        if ot == 'STRING':
            return '<%ss' % ch_num, ch_num
        else:
            return '<%s' % ada_type_map[ot]['struct'], ada_type_map[ot]['size']

    def set_result(self, value, name):
        tmp = self.result
        for f in self.name_stack:
            if f not in tmp:
                tmp[f] = {}
            tmp = tmp[f]
        tmp[name] = value

    @log('GenFmt')
    def walk_a_base_type(self, field, typ, i_size=None, i_name=None, enum_type=None):
        my_log.debug("walk_a_base_type: [%s][%s][%s]" % (field, typ, i_size))
        num = None
        if typ == 'STRING':
            num = (i_size - 1) // 8 +1
            #if getattr(field, 'size', None) is None:
            #    setattr(field, 'size', 8 *num)
        elif typ == 'FLOAT':
            size = i_size or (int(field.end_bit) - int(field.start_bit))
            if size  > 32:
                typ = 'LONG_FLOAT'
        elif typ == 'INTEGER':
            size = i_size or (int(field.end_bit) - int(field.start_bit))
            if size <= 8:
                typ = 'SHORT_SHORT_INTEGER'
            elif size <=16:
                typ = 'SHORT_INTEGER'
            elif size > 32:
                typ = 'LONG_LONG_INTEGER'
        struc, leng = GenFmt.get_struct(typ, num)
        pos = self.get_pos(int(field.pos))
        name = self.get_name(i_name or getattr(field, 'tmp_name_in_array', None) or field.name)
        my_log.debug("name: [%s], pos: [%s], struct: [%s], length: [%s]"
              %(name, pos, struc, leng))
        tmp = {'pos': pos,
               'length': leng,
               'leaf': True,
               'struct': struc,
               }
        if (getattr(field, 'start_bit', None) is not None) and (
                    getattr(field, 'end_bit', None) is not None) and (
                    ((int(field.end_bit) - int(field.start_bit)+1) % 8) in range(1, 8)):
            tmp['start_bit'] = field.start_bit
            tmp['end_bit'] = field.end_bit
        if enum_type is not None:
            tmp['enum_type'] = enum_type
        self.set_result(tmp, name)


    @log('GenFmt')
    def walk_a_record(self, rec=None):
        if rec is None:
            rec = self.base
        my_log.debug("walk_a_record: %s" % rec.name)
        my_log.debug("rec fields: %s" % rec.fpos)
        for field in rec.fpos:
            self.walk_a_field(rec.fields[field])

    @log('GenFmt')
    def walk_an_array(self, arr,  i_size=None):
        my_log.debug("walk_an_array: %s, %s" % (i_size, arr))
        elem_num =  1
        array_index = []
        try:
            for index in arr.index_list:
                for attr in ['first', 'last']:
                    if getattr(index, attr, None) is None:
                        if getattr(index.based, attr, None) is not None:
                            setattr(index, attr, getattr(index.based, attr))
                based = index.based
                while based is not None and based.ttype in [AdaType.DERIVED_TYPE, AdaType.SUBTYPE]:
                    based = based.based
                if  based is not None and based.ttype == AdaType.ENUM_TYPE:
                    setattr(index, 'enums', based.enums)
                    if getattr(index, 'first', None) is None:
                        setattr(index, 'first', 0)
                    if getattr(index, 'last', None) is None:
                        setattr(index, 'last', len(based.enums)-1)
                    if (isinstance(index.first, str) and not index.first.isdigit()
                     ) and (isinstance(index.last, str) and not index.last.isdigit()):
                        start = index.enums.index(index.first)
                        last = index.enums.index(index.last)
                        elem_num *= last - start + 1
                        array_index.append(index.enums[start : last +1])
                        my_log.debug("hd1: %s" % array_index)
                    else:
                        start = int(index.first)
                        last = int(index.last)
                        elem_num *= last - start + 1
                        array_index.append(index.enums[start: last + 1])
                        my_log.debug("hd2: %s" % array_index)
                else:
                    start = int(index.first)
                    last = int(index.last)
                    elem_num *= last - start + 1
                    array_index.append(list(map(str, range(start, last+1))))
                    my_log.debug("hd3: %s" % array_index)
        except TypeError:
            elem_num = int(arr.last) - int(arr.first) + 1
            array_index.append(list(map(str, range(int(arr.first), int(arr.last) + 1))))
            my_log.debug("hd4: %s" % array_index)
        my_log.debug("hd5: %s" % array_index)
        cur_elem_name = arr.elem.name
        #array_index_names = list(map(lambda x: '_'.join(x), zip(*array_index)))
        array_index_names = list(map(lambda x: '_'.join(x), itertools.product(*array_index)))
        my_log.debug("array: %s"% arr)
        my_log.debug('array index names: %s' % list(array_index_names))
        my_log.debug("elem_num: %s" % elem_num)
        for i in range(elem_num):
            for attr in ['size', ]:
                if getattr(arr.elem, attr, None) is None:
                    if hasattr(arr.elem, 'based') and hasattr(arr.elem.based, attr):
                        setattr(arr.elem, attr, getattr(arr.elem.based, attr))
            if isinstance(arr.elem.size, str):
                arr.elem.size = eval(arr.elem.size.replace('STANDARD_TYPES.OCTET', '8').replace('OCTET', '8'))
            if (arr.elem.size is None or arr.elem.size < 8) and i_size:
                setattr(arr.elem, 'size', i_size // elem_num)
            if arr.elem.size is not None:
                setattr(arr.elem, 'pos', i * arr.elem.size // 8)
            elif i == 0:
                setattr(arr.elem, 'pos', 0)
            my_log.debug("hd test size: %s, %s, %s, %s" % (arr.elem.size, arr.elem.size_solved, i, arr.elem.pos))
            #arr.elem.name = "%s_%s" % (cur_elem_name, i)
            setattr(arr.elem, 'tmp_name_in_array', array_index_names[i])
            self.walk_a_field(arr.elem, is_field=False)
            delattr(arr.elem, 'tmp_name_in_array')
        if getattr(arr, 'size', None) is None:
            if getattr(arr.elem, 'size', None) is not None:
                setattr(arr, 'size', arr.elem.size * elem_num)
            else:
                based = arr.elem
                while based.ttype in [AdaType.DERIVED_TYPE, AdaType.SUBTYPE] \
                        and getattr(based, 'based', None) is not None \
                        and getattr(based, 'size', None) is None:
                    based = based.based
                if getattr(based, 'size', None) is not None:
                    setattr(arr, 'size', based.size * elem_num)
                elif i_size:
                    setattr(arr, 'size', i_size)
        arr.elem.name = cur_elem_name

    @log('GenFmt')
    def walk_a_field(self, field, is_field=True):
        my_log.debug("walk_a_field: %s" % field)
        ft = field.field_type if is_field else field
        if ft.ttype in [AdaType.DERIVED_TYPE, AdaType.SUBTYPE]:
            ft2 = ft.based
            for attr in ['first', 'last', 'size']:
                if getattr(ft2, attr, None) is None:
                    if hasattr(ft, attr):
                        setattr(ft2, attr, getattr(ft, attr))
                    elif hasattr(field, attr):
                        setattr(ft2, attr, getattr(field, attr))
            ft2 = copy.deepcopy(ft2)
            for attr in ['pos', 'end_bit', 'start_bit']:
                if getattr(ft2, attr, None) is None:
                    if hasattr(ft, attr):
                        setattr(ft2, attr, getattr(ft, attr))
                    elif hasattr(field, attr):
                        setattr(ft2, attr, getattr(field, attr))
            ft = ft2
        my_log.debug("ttype: %s" % ft.ttype)
        if ft.name == 'STRING':
            if is_field:
                for attr in ['first', 'last', 'size', 'pos', 'end_bit', 'start_bit']:
                    if getattr(field, attr, None) is None:
                        if hasattr(ft, attr):
                            setattr(field, attr, getattr(ft, attr))
                if getattr(field, 'size', None) is None:
                    setattr(field, 'size', (int(field.last) - int(field.first) + 1) * 8)
            self.walk_a_base_type(field, 'STRING',
                                  i_size=field.size or (int(ft.last) - int(ft.first) + 1) * 8)
        elif ft.ttype == AdaType.RECORD_TYPE:
            self.pos_stack.append(int(field.pos))
            self.name_stack.append(field.name)
            self.walk_a_record(ft)
            self.name_stack.pop()
            self.pos_stack.pop()
            return
        elif ft.ttype == AdaType.ARRAY_TYPE:
            self.pos_stack.append(int(field.pos))
            self.name_stack.append(field.name)
            i_size = getattr(field, 'size', None)
            if not i_size and getattr(field, 'start_bit', None) is not None and getattr(field, 'end_bit', None) is not None:
                try:
                    i_size = int(field.end_bit) - int(field.start_bit) + 1
                except TypeError:
                    i_size = None
            self.walk_an_array(ft, i_size=i_size)
            self.name_stack.pop()
            self.pos_stack.pop()
        elif ft.ttype == AdaType.REAL_TYPE:
            self.walk_a_base_type(field, 'FLOAT', field.size)
        elif ft.ttype == AdaType.INT_TYPE:
            self.walk_a_base_type(field, 'INTEGER', field.size)
        elif ft.ttype == AdaType.ENUM_TYPE:
            enum_type = '.'.join([ft.package, ft.name])
            if enum_type not in self.result['gen_fmt_enums']:
                enums = {}
                t_val = 0
                for e in ft.items.keys():
                    enums[ft.items[e].value or str(t_val)] = e
                    t_val += 1
                self.result['gen_fmt_enums'][enum_type] = enums
            self.walk_a_base_type(field, 'INTEGER', field.size, enum_type=enum_type)



if __name__ == "__main__":
    start_time = time.time()
    setup_logging()
    #i_csci = 'common_cdc'
    i_csci = 'test'
    with open(os.path.join('run', '%s.dump' % i_csci), 'rb') as fd:
        pe = pickle.load(fd)
    if 0:
        rec_lg = 56
        rec_file = 'ident0745'
        package = 'IAC_IDENTIFICATION_TYPES'
        typ = 'IDENTIFICATION_T'
    else:
        rec_lg = 8392
        rec_file = 'REC_FPL_201029_0345.cupd'
        if 1:
            package = 'IAC_FLIGHT_PLAN_TYPES'
            typ = 'FLIGHT_PLAN_T'
        else:
            package = 'HD_TEST'
            typ = 'TEST_TYPE'
    with open(os.path.join('data', rec_file), 'rb') as fd:
        fd.seek(32)
        buf = fd.read(rec_lg)
    if 0:
        #my_log.debug(pe.vars['STANDARD_TYPES']['OCTET'])
        pe.types['IAC_FLIGHT_PLAN_TYPES']['FLIGHT_PLAN_T'].fields['TOTAL_DELAY'].print()
    else:
        ur = GenFmt(pe.types[package][typ])
        ur.walk_a_record()
        #my_log.debug("Result: %s" % ur.result)
        #my_log.debug(json.dumps(ur.result))
        pprint.pprint(ur.result)
        end_time = time.time()
        with open(os.path.join('run', '.'.join([package, typ, 'json'])), 'w') as f1:
            json.dump(ur.result, f1)
        print("Use time: %.02f seconds" % (end_time - start_time))
