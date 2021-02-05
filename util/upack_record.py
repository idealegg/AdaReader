# -*- coding: utf-8 -*-
from common.ada_type import AdaType
import struct
from functools import reduce


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


class UpackRecord:

    enum_type = {}
    def __init__(self, ctx, buf, offset):
        self.ctx = ctx
        self.buf = buf
        self.pos_stack = [offset]
        self.name_stack = []
        self.result = {}
        self.enums = {}

    def get_pos(self, f_p):
        return reduce(lambda x, y: x+y, self.pos_stack) + f_p

    def get_name(self, f_n):
        return reduce(lambda x, y: ".".join([x, y]), self.name_stack) + f_n

    @staticmethod
    def get_struct(ot, ch_num=None):
        if ot == 'STRING':
            return '>%ss' % ch_num, ch_num
        else:
            return '>%s' % ada_type_map[ot]['struct'], ada_type_map[ot]['size']

    def set_result(self, value, name):
        tmp = self.result
        for f in self.name_stack:
            if f not in tmp:
                tmp[f] = {}
            tmp = tmp[f]
        tmp[name] = value

    def walk_a_base_type(self, field, typ, size=None):
        num = None
        if typ == 'STRING':
            num = field.last - field.first + 1
        elif typ == 'FLOAT':
            size = size or (field.end_bit - field.start_bit)
            if size  > 32:
                typ = 'LONG_FLOAT'
        elif typ == 'INTEGER':
            size = size or (field.end_bit - field.start_bit)
            if size <= 8:
                typ = 'SHORT_SHORT_INTEGER'
            elif size <=16:
                typ = 'SHORT_INTEGER'
            elif size > 32:
                typ = 'LONG_LONG_INTEGER'
        struc, leng = UpackRecord.get_struct(typ, num)
        pos = self.get_pos(field.pos)
        name = self.get_name(field.name)
        tmp = struct.unpack(struc, self.buf[pos: pos + leng + 1])
        if self.enums:
            self.set_result(self.enums[tmp[0]], name)
        else:
            self.set_result(tmp[0], name)

    def walk_a_record(self, rec):
        for field in rec.fpos:
            self.walk_a_field(rec.fields[field])

    def walk_an_array(self, arr):
        for index in arr.index_list:
            if not isinstance(index.based, str):
                pass


            
    def walk_a_field(self, field, offset):
        ft = field.field_type
        if ft.ttype == AdaType.RECORD_TYPE:
            self.pos_stack.append(field.pos)
            self.name_stack.append(field.name)
            self.walk_a_record(ft)
            self.name_stack.pop()
            self.pos_stack.pop()
            return
        elif ft.ttype == AdaType.ARRAY_TYPE:
            self.pos_stack.append(field.pos)
            self.name_stack.append(field.name)
            self.walk_an_array(ft)
            self.name_stack.pop()
            self.pos_stack.pop()
        elif ft.ttype == AdaType.REAL_TYPE:
            self.walk_a_base_type(field, 'FLOAT', field.size)
        elif ft.ttype == AdaType.INT_TYPE:
            self.walk_a_base_type(field, 'INTEGER', field.size)
        elif ft.ttype == AdaType.ENUM_TYPE:
            self.enums = {}
            t_val = 0
            for e in ft.items.keys():
                self.enums[ft.items[e].value | t_val] = e
                t_val += 1
            self.walk_a_base_type(field, 'INTEGER', field.size)
            self.enums = {}


