# -*- coding: utf-8 -*-
from common.ada_type import AdaType
import struct


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

ada_type_map = {'CHARACTER': {'C': 'char', 'Python': 'string of length 1', 'Ada': 'CHARACTER', 'size': 1},
                'SHORT_SHORT_INTEGER': {'C': 'signed char', 'Python': 'integer', 'Ada': 'SHORT_SHORT_INTEGER', 'size': 1},
                'BOOLEAN': {'C': '_Bool', 'Python': 'bool', 'Ada': 'BOOLEAN', 'size': 1},
                'SHORT_INTEGER': {'C': 'short', 'Python': 'integer', 'Ada': 'SHORT_INTEGER', 'size': 2},
                'INTEGER': {'C': 'int', 'Python': 'integer', 'Ada': 'INTEGER', 'size': 4},
                'LONG_INTEGER': {'C': 'long', 'Python': 'integer', 'Ada': 'LONG_INTEGER', 'size': 4},
                'LONG_LONG_INTEGER': {'C': 'long long', 'Python': 'long', 'Ada': 'LONG_LONG_INTEGER', 'size': 8},
                'FLOAT': {'C': 'float', 'Python': 'float', 'Ada': 'FLOAT', 'size': 4},
                'LONG_FLOAT': {'C': 'double', 'Python': 'float', 'Ada': 'LONG_FLOAT', 'size': 8},
                'STRING': {'C': 'char[]', 'Python': 'string', 'Ada': 'STRING', 'size': None}}

class UpackRecord:

    enum_type = {}
    def __init__(self, ctx, buf, offset):
        self.ctx = ctx
        self.buf = buf
        self.offset = offset
        self.pos_list = [0]
        self.fns = []
        self.result = {}

    def get_pos(self):
        pass

    def walk_a_record(self, rec):
        for field in rec.fpos:
            self.walk_a_field(rec.fields[field])

    def walk_a_field(self, field, offset):
        ft = field.field_type
        if ft.ttype == AdaType.RECORD_TYPE:
            self.pos_list.append(field.pos)
            self.fns.append(field.name)
            self.walk_a_record(ft)
        elif ft.ttype == AdaType.REAL_TYPE:
            bits = field.end_bit - field.start_bit
            if bits <= 32:
                otype = 'FLOAT'
            else:
                otype = 'LONG_FLOAT'
            self.walk_a_step(otype)

    def walk_a_step(self):
        tmp = struct.unpack('>', self.buf[self.get_pos(): self.get_lenght()])
        self.set_result(tmp)
