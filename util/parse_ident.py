#*--coding:utf8--*
#!/bin/env python

import sys
import struct
import time
import pprint
import time
import binascii as bs


def debug_p(s):
    if debug:
        print(s)
        
def strip_zero(s):
    s = s.strip()
    t = s.find('\0')
    if t!=-1:
        return s[:s.find('\0')]
    else:
        return s
    
    
def conv_field(field, struc, typ=None):
    if struc.count('s'):
        return strip_zero(field)
    if typ in enum_type:
        #print '%s: %s' % (typ, field)
        return enum_type[typ][field]
    return field
    
def conv_name(obj, typ):
    if typ == 'str':
        return conv_field(obj, 's')
    elif typ == 'delta':
        out=''
        if obj['p']:
            if obj['s']:
                out=''.join([out, '-'])
            min = obj['v_s']/60
            hour = min / 60
            min = min % 60
            sec = obj['v_s'] % 60
            out=''.join([out, "%02d:%02d:%02d.%03d" % (hour, min, sec, obj['v_ms'])])
        return out
    elif typ == 'date':
        out=''
        if obj is list:
            sec = obj[0]
            usec = obj[1]
        else:
            sec = obj['s']
            usec = obj['us']
        out = '.'.join([time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(sec)), '%06d' % usec])
        return out
    elif typ == 'level':
        out=''
        if obj['p']:
            if obj['u_t'] and obj['u_t'] != len(enum_type['level_type']):
                out="%s%d" % (enum_type['level_type'][obj['u_t']-1], obj['u_v'])
            else:
                out="%.02f%s" % (obj['v'], 'ft')
        return out
    elif typ == 'speed':
        out=''
        if obj['p']:
            if obj['u_t'] and obj['u_t'] != len(enum_type['speed_type']):
                out="%s%d" % (enum_type['speed_type'][obj['u_t']-1], obj['u_v'])
            else:
                out="%.02f%s" % (obj['v'], 'knot')
        return out 
    elif typ == 'pilot':
        out=0
        if obj['p']:
            out = obj['id']
        return out           
    elif typ == 'ssr':
        out=''
        if obj['p']:
            if 'a' in obj:
                out='A'
            else:
                out='B'
            out += '%o' % obj['v']
        return out   
    elif typ in enum_type:
        return enum_type[typ][obj]
    else:
        return obj
  
def get_len(struc):
    offset1=0
    out_len = 0
    tmp_len = ''
    while offset1 < len(struc):
        if struc[offset1].isdigit():
            tmp_len += struc[offset1]
        elif struc[offset1].isalpha() or struc[offset1] == '?':
            attr = format_map[struc[offset1]]              
            out_len += attr['size'] if attr['size'] else (1 if not tmp_len else int(tmp_len))
            tmp_len = ''
        offset1 += 1 
    return out_len
    
def parse_a_field(name, struc, offset_len=0, typ=None):
    global offset
    debug_p("parse_a_field: name=%s, struct=[%s], offset_len=%s, type=%s" % (name, struc, offset_len, typ))
    debug_p("offset: %s" % offset)
    buf_len = get_len(struc)
    debug_p("buf: %s" % bs.hexlify(buf[offset:offset+buf_len]))
    tmp, = struct.unpack(struc, buf[offset:offset+buf_len])
    offset += offset_len or buf_len
    output[key][name] = conv_field(tmp, struc, typ)
        
def parse_a_list(name, sub_name_list, struc, offset_len=0, typ=None):
    global offset
    debug_p("parse_a_list: name=%s, sub_name_list=%s, struct=[%s], offset_len=%s, type=%s" % (name, sub_name_list, struc, offset_len, typ))
    debug_p("offset: %s" % offset)
    buf_len = get_len(struc)
    debug_p("buf: %s" % bs.hexlify(buf[offset:offset+buf_len]))
    tmp = list(struct.unpack(struc, buf[offset:offset+buf_len]))
    offset += offset_len or buf_len
    output[key][name] = {}
    for sn in sub_name_list:
        output[key][name][sn] = tmp.pop(0)
    output[key][name] = conv_name(output[key][name], typ)
    
def parse_an_array(name, struc, array_len, elem_len=None, elem_prefix=None, elem_start_index=1, array_index_prefix=None, array_start_index=1, offset_len=0, typ=None):
    global offset
    debug_p("parse_an_array: name=%s, struct=[%s], array_len=%s, elem_len=%s, elem_prefix=%s, elem_start_index=%s, array_index_prefix=%s, array_start_index=%s, offset_len=%s, typ=%s" %
        (name, struc, array_len, elem_len, elem_prefix, elem_start_index, array_index_prefix, array_start_index, offset_len, typ))
    struc_len = get_len(struc)
    elem_len = elem_len or get_len(struc)
    buf_len = elem_len*array_len
    debug_p("offset: %s" % offset)
    debug_p("buf: %s" % bs.hexlify(buf[offset:offset+buf_len]))
    old_struc = struc
    if struc_len < elem_len:
        struc += "%dx" % (elem_len - struc_len)
    if struc[0] in flag_map:
        struc = struc[0] + struc[1:] * array_len
    else:
        struc *= array_len 
    tmp = struct.unpack(struc, buf[offset:offset+buf_len])
    offset += offset_len or buf_len
    debug_p('unpack: %s' % (tmp,))
    elem_atoms = len(tmp)/array_len
    if elem_atoms != 1:
        tmp_out = []
        for i in range(array_len):
            tmp_out.append([])
            for j in range(elem_atoms):
                tmp_out[i].append(tmp[i*elem_atoms+j])
            debug_p('rerange1: %s' % (tmp_out,))
            tmp_out[i] = conv_name(tmp_out[i], typ)
        tmp = tmp_out
    else:
        tmp_out = []
        for val in tmp:
            tmp_out.append(conv_field(val, old_struc, typ))
        tmp = tmp_out
        debug_p('rerange2: %s' % (tmp,))
    if array_index_prefix:
        tmp_out = []
        for val in tmp:
            tmp_out.append('%s_%d: %s' % (array_index_prefix, array_start_index, val))
            array_start_index += 1
        tmp = tmp_out
    if elem_prefix:
        tmp_out = {}
        for val in tmp:
            tmp_out['%s_%d' % (elem_prefix, elem_start_index)] = val
            elem_start_index += 1
        tmp = tmp_out
    output[key]['_'.join([name,elem_prefix]) if elem_prefix else name] = tmp
        
def parse_status():
    parse_an_array('STATUS', '<?', 10, elem_prefix='ACT', array_index_prefix='G', offset_len=12)
    parse_an_array('STATUS', '<iii', 10, elem_prefix='ACT_TIME', array_index_prefix='G', typ='date')
    
    
flag_map = {'@': {'Byte order': u'本机',          'Size': u'本机', 'Alignment': u'本机,凑够4字节'}, 
            '=': {'Byte order': u'本机',          'Size': u'标准', 'Alignment': u'none,按原字节数'}, 
            '<': {'Byte order': u'小端',          'Size': u'标准', 'Alignment': u'none,按原字节数'}, 
            '>': {'Byte order': u'大端',          'Size': u'标准', 'Alignment': u'none,按原字节数'}, 
            '!': {'Byte order': u'network(大端)', 'Size': u'标准', 'Alignment': u'none,按原字节数'}, 
            }
format_map = {  'x': {'C': u'pad byte(填充字节)', 'Python': 'no value',           'size': None},
                'c': {'C': u'char',               'Python': 'string of length 1', 'size': 1},
                'b': {'C': u'signed char',        'Python': 'integer',            'size': 1},
                'B': {'C': u'unsigned char',      'Python': 'integer',            'size': 1},
                '?': {'C': u'_Bool',              'Python': 'bool',               'size': 1},
                'h': {'C': u'short',              'Python': 'integer',            'size': 2},
                'H': {'C': u'unsigned short',     'Python': 'integer',            'size': 2},
                'i': {'C': u'int',                'Python': 'integer',            'size': 4},
                'I': {'C': u'unsigned int',       'Python': 'integer',            'size': 4},
                'l': {'C': u'long',               'Python': 'integer',            'size': 4},
                'L': {'C': u'unsigned long',      'Python': 'long',               'size': 4},
                'q': {'C': u'long long',          'Python': 'long',               'size': 8},
                'Q': {'C': u'unsigned long long', 'Python': 'long',               'size': 8},
                'f': {'C': u'float',              'Python': 'float',              'size': 4},
                'd': {'C': u'double',             'Python': 'float',              'size': 8},
                's': {'C': u'char[]',             'Python': 'string',             'size': None},
                'p': {'C': u'char[]',             'Python': 'string',             'size': None},
                'P': {'C': u'void *',             'Python': 'long',               'size': None},
}
        

enum_type = {
    'level_type': ('F','S','A','M','VFR', 'NONE'),
    'speed_type': ('Knot','Mach','KM', 'NONE'),
    'fpl_mes_type': ('ICAO', 'AIDC', 'OLDI', 'ADEXP'),
    'unit_type':('METRIC', 'IMPERIAL'),
    'cdc_event_t':('NONE', 'UPDATED', 'DELETED', 'ALL_DELETED'),
    'coupling_status_t':('AUTO', 'MANUAL', 'UNCOUPLED'),
    'coupling_mode_t':  ( 'PSSR_COUPLING', 'ASSR_COUPLING', 'ICAO_CODE', 'CALLSIGN','NONE' ),
    'proximity_result_t':       ( 'IN_SIDE', 'OUT_SIDE' ),
    'ram_result_t'             : ( 'ON_ROUTE', 'OFF_ROUTE', 'NOT_CHECKED' ),
    'clam_result_t'           : ( 'ADHERED', 'NOT_ADHERED', 'NOT_CHECKED' ),
    'cstd_result_t'            : ( 'NOT_COASTED', 'COASTED' ),
    'dup_status_t' : ( 'NO_DUP' , 'DUP' ),
}


count=0
offset=0
debug=0
header_lg = 32
rec_lg = 56
output={}
fd=open(sys.argv[1],'rb')

if len(sys.argv) > 2 and '-debug' in sys.argv:
    debug=1
    
if len(sys.argv) > 2:
    count=int(sys.argv[2])

while True:
    buf=fd.read(4)
    if not buf:
        break
    offset = 0
    count += 1
    key = count
    output[key]={}
    parse_a_field('CDC_EVENT', '<i', typ='cdc_event_t')
    if output[key]['CDC_EVENT'] in enum_type['cdc_event'][1:]:
        offset = 0
        buf=fd.read(12)
        parse_a_list('TIMESTAMP', ['s', 'us'], '<?ii4x', typ='date')
    if output[key]['CDC_EVENT'] in enum_type['cdc_event'][1:3]:
        offset = 0
        buf=fd.read(16)
        parse_a_field('IDENT', '<i8x')
        #parse_a_field('IDENT', '<ix', 16)
    if output[key]['CDC_EVENT'] == 'UPDATED':
        offset = 0
        buf=fd.read(rec_lg)
        parse_a_field('FLIGHT_PLAN_NUMBER', '<h')
        parse_a_field('SURV_TRACK_NUMBER', '<h')
        parse_a_field('COUPLING_STATUS', '<b', typ='coupling_status_t')
        parse_a_field('COUPLING_MODE', '<b', typ='coupling_mode_t')
        parse_a_field('COMPOSED_OF_INFO_VALID', '<?')
        parse_a_field('NEXT_FIX', '<b')
        parse_a_field('PROXIMITY_RESULT', '<b', typ='proximity_result_t')
        parse_a_field('RAM_RESULT', '<b', typ='ram_result_t')
        parse_a_field('CLAM_RESULT', '<b', typ='clam_result_t')
        parse_a_field('DUP_STATUS', '<b', typ='dup_status_t')
        parse_a_field('NB_CONFLICT_TRACKS', '<h')
        parse_an_array('CONFLICT_TRACKS', '<h', 10, elem_prefix='', array_index_prefix='')
        parse_a_field('NB_CONFLICT_FLIGHT_PLANS', '<h2x')
        parse_an_array('CONFLICT_FLIGHT_PLANS', '<h', 10, elem_prefix='', array_index_prefix='', offset_len=12)
        parse_a_list('RECORD_UPDATE_TIME', ['s', 'us'], '<?ii4x', typ='date')
        parse_a_field('CSTD_RESULT', '<b', 4, 'cstd_result_t')
        
print("count: %s" % count)
pprint.pprint(output)
