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


class ParseRec():
    cdc_event_t = ('NONE', 'UPDATED', 'DELETED', 'ALL_DELETED')
    def __init__(self, rec_file=None, fmt_file=None, rec_size=None):
        self.rec_file = rec_file
        self.fmt_file = fmt_file
        self.rec_size = rec_size
        self.fmt_obj = None
        self.buf = None
        with open(self.fmt_file, 'r') as fd:
            self.fmt_obj = json.load(fd)
        self.names = []
        self.result = {}

    def set_result(self, value, name):
        tmp = self.result
        for f in self.names:
            if f not in tmp:
                tmp[f] = {}
            tmp = tmp[f]
        tmp[name] = value

    def parse_a_leaf(self, n, v):
        print("%s: %s" %(n, v))
        print('buf: %s' % bs.hexlify(self.buf[v['pos']: v['pos'] + v['length']]))
        tmp = struct.unpack(v['struct'], self.buf[v['pos']: v['pos'] + v['length']])
        val = tmp[0]
        if 'start_bit' in v and 'end_bit' in v:
            val = (val >> int(v['start_bit']))
            val = (val & ( 2 ** (int(v['end_bit']) - int(v['start_bit']) +1) - 1))
        if 'enum_type' in v:
            val = self.fmt_obj['gen_fmt_enums'][v['enum_type']][str(val)]
        self.set_result(val, n)

    def parse(self, fmt_obj=None):
        if fmt_obj is None:
            self.parse(self.fmt_obj)
            #pprint.pprint(self.result)
        else:
            for key, value in fmt_obj.items():
                if key != "gen_fmt_enums":
                    if 'leaf' in value:
                        self.parse_a_leaf(key, value)
                    else:
                        self.names.append(key)
                        self.parse(value)
                        self.names.pop()

    @staticmethod
    def parse_data(sec, usec):
        return '.'.join([time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(sec)), '%06d' % usec])

    def parse_rec(self):
        with open(self.rec_file, 'rb') as fd:
            count = 0
            output = {}
            while True:
                buf = fd.read(4)
                if not buf:
                    break
                count += 1
                key = count
                output[key] = {}
                tmp, = struct.unpack('<i', buf)
                output[key]['CDC_EVENT'] = ParseRec.cdc_event_t[tmp]
                buf = fd.read(12)
                sec, usec = struct.unpack('<ii4x', buf)
                output[key]['TIMESTAMP'] = ParseRec.parse_data(sec, usec)
                buf = fd.read(16)
                tmp, = struct.unpack('<i12x', buf)
                output[key]['IDENT'] = tmp
                if 1:
                #if output[key]['CDC_EVENT'] == 'UPDATED':
                    self.names = []
                    self.result = {}
                    self.buf = fd.read(self.rec_size)
                    self.parse()
                    output[key].update(self.result)
            pprint.pprint(output)

if __name__ == "__main__":
    rec_lg = 8392
    rec_file = 'REC_FPL_201029_0345.cupd'
    if 1:
        package = 'IAC_FLIGHT_PLAN_TYPES'
        typ = 'FLIGHT_PLAN_T'
    else:
        package = 'HD_TEST'
        typ = 'TEST_TYPE'
    pb = ParseRec(os.path.join('data', rec_file), os.path.join('run', ".".join([package, typ, 'json'])), rec_lg)
    pb.parse_rec()