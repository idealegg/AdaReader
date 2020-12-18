# Generated from ADA95.g4 by ANTLR 4.7.2
from antlr4 import *
from ADA95Listener import ADA95Listener
from ADA95Parser import ADA95Parser
import pprint
import re


# This class defines a complete listener for a parse tree produced by ADA95Parser.
class ADA95Listener2(ADA95Listener):
    def __init__(self):
        self.INIT = 0
        self.FULL_TYPE = 1
        self.DISCRIM = 2
        self.MEMB = 3
        self.POSITION = 4
        self.SIZE = 5
        self.cur_stat = self.INIT
        self.cur_type_dec = {
            'name' : '',
            'discriminant': {},
            'memb': {},
            'pos': {},
            'size': {},

        }
        self.known_var = {'STANDARD_TYPES.OCTET': '8',
                          }
        self.unsolved = set()

    def try_eval_expr(self, exp):
        out = re.sub('(\d+)_(\d+)', '\\1\\2', exp)
        out = re.sub('(\d+)#(\d+)#', lambda x: str(int(x.group(2), int(x.group(1)))), out)
        for key in self.known_var:
            key_idents = key.split('.')
            for i in range(len(key_idents)):
                out = out.replace(".".join(key_idents[i:]), self.known_var[key])
        try:
            out = eval(out)
        except (NameError, SyntaxError) as ne:
            print('No solved: %s' % ne)
            res = re.findall('[a-zA-Z]\w*(?:\.[a-zA-Z]\w*)*', out)
            res = set(res)
            print ("\t%s" %(res,))
            self.unsolved.update(res)
        return out

    # should the function becomes function of Rule Context?
    def getAllText(self, ctx):  # include hidden channel
        token_stream = ctx.parser.getTokenStream()
        lexer = token_stream.tokenSource
        input_stream = lexer.inputStream
        start = ctx.start.start
        stop = ctx.stop.stop
        return input_stream.getText(start, stop)

    # Enter a parse tree produced by ADA95Parser#type_definition_clause.
    def enterType_definition_clause(self, ctx: ADA95Parser.Type_definition_clauseContext):
        self.cur_type_dec['name'] = ctx.defining_identifier().getText()
        print('type: %s' % self.cur_type_dec['name'])
        print(        'enterType_definition_clause')
        print('enterFull_type_declaration')
        self.cur_stat = self.FULL_TYPE

    # Exit a parse tree produced by ADA95Parser#type_definition_clause.
    def exitType_definition_clause(self, ctx: ADA95Parser.Type_definition_clauseContext):
        print (       'exitType_definition_clause')
        self.cur_stat = self.INIT

    def enterKnown_discriminant_part(self, ctx):
        print('enterKnown_discriminant_part')
        self.cur_stat = self.DISCRIM
        self.cur_type_dec['discriminant'] = {}
        self.cur_type_dec['discriminant']['list'] = {}
        self.cur_type_dec['discriminant']['fields'] = {}

    def exitKnown_discriminant_part(self, ctx):
        print('exitKnown_discriminant_part')
        tmp_idents = []
        for idents in self.cur_type_dec['discriminant']['fields']:
            tmp_idents.extend(idents)
        self.cur_type_dec['discriminant']['fields'] = tmp_idents
        self.cur_stat = self.FULL_TYPE

    def enterDiscriminant_specification(self, ctx):
        print('enterDiscriminant_specification')

    def exitDiscriminant_specification(self, ctx):
        print('exitDiscriminant_specification')
        a_memb = {}
        a_memb['type'] = ctx.subtype_mark().getText()
        def_val = ctx.default_expression()
        if def_val is not None:
            a_memb['default'] = def_val.getText()
        else:
            a_memb['default'] = None
        a_memb['fields'] = self.cur_type_dec['discriminant']['fields'][-1]
        for ident in a_memb['fields']:
            self.cur_type_dec['discriminant']['list'][ident] = a_memb
        self.cur_stat = self.FULL_TYPE

    def enterDefining_identifier_list(self, ctx):
        print('enterDefining_identifier_list')
        if self.cur_stat == self.DISCRIM:
            self.cur_type_dec['discriminant']['fields'] = []

    def exitDefining_identifier_list(self, ctx):
        print('exitDefining_identifier_list')
        i = 0
        idents = []
        ident = ctx.defining_identifier(i)
        while ident:
            idents.append(ident.getText())
            i += 1
            ident = ctx.defining_identifier(i)
        if self.cur_stat == self.DISCRIM:
            self.cur_type_dec['discriminant']['fields'].append(idents)
        elif self.cur_stat == self.MEMB:
            self.cur_type_dec['memb']['fields'].append(idents)

    def enterRecord_definition(self, ctx):
        print  ( 'enterRecord_definition')
        self.cur_stat = self.MEMB
        self.cur_type_dec['memb'] ={}
        self.cur_type_dec['memb']['list'] = {}
        self.cur_type_dec['memb']['fields'] = []

    def exitRecord_definition(self, ctx):
        print      (  'exitRecord_definition')
        tmp_idents = []
        for idents in self.cur_type_dec['memb']['fields']:
            tmp_idents.extend(idents)
        self.cur_type_dec['memb']['fields'] = tmp_idents
        self.cur_stat = self.FULL_TYPE

    def enterComponent_declaration(self, ctx):
        print('enterComponent_declaration')

    def exitComponent_declaration(self, ctx):
        print('exitComponent_declaration')
        if self.cur_stat == self.MEMB:
            a_memb = {}
            a_memb['type'] = ctx.component_definition().getText()
            def_val = ctx.default_expression()
            if def_val is not None:
                a_memb['default'] = def_val.getText()
            else:
                a_memb['default'] = None
            a_memb['fields'] = self.cur_type_dec['memb']['fields'][-1]
            for ident in a_memb['fields']:
                self.cur_type_dec['memb']['list'][ident] = a_memb

    def enterRecord_representation_clause(self, ctx):
        print('enterRecord_representation_clause')
        self.cur_stat = self.POSITION
        self.cur_type_dec['pos'] = {}
        self.cur_type_dec['pos']['list'] = {}
        self.cur_type_dec['pos']['fields'] = []

    def exitRecord_representation_clause(self, ctx):
        print('exitRecord_representation_clause')
        if self.cur_stat == self.POSITION:
            self.cur_type_dec['pos']['name'] = ctx.first_subtype_local_name().getText()
            mod_cls = ctx.mod_clause()
            if mod_cls is not None:
                self.cur_type_dec['pos']['mod_clause'] = mod_cls.getText()
            else:
                self.cur_type_dec['pos']['mod_clause'] = None
        self.cur_stat = self.FULL_TYPE

    def enterComponent_clause(self, ctx):
        print('enterComponent_clause')

    def exitComponent_clause(self, ctx):
        print('exitComponent_clause')
        if self.cur_stat == self.POSITION:
            a_memb = {}
            a_memb['field'] = ctx.component_local_name().getText()
            a_memb['pos'] = self.try_eval_expr(ctx.position().getText())
            a_memb['first'] = self.try_eval_expr(ctx.first_bit().getText())
            a_memb['last'] = self.try_eval_expr(ctx.last_bit().getText())
            self.cur_type_dec['pos']['fields'].append(a_memb['field'])
            self.cur_type_dec['pos']['list'][a_memb['field']] = a_memb

    def enterAttribute_definition_clause(self, ctx):
        print('enterAttribute_definition_clause')
        self.cur_stat = self.SIZE
        self.cur_type_dec['size'] = {}

    def exitAttribute_definition_clause(self, ctx):
        print('exitAttribute_definition_clause')
        if self.cur_stat == self.SIZE:
            a_memb = {}
            a_memb['type'] = ctx.local_name().getText()
            a_memb['attr'] = ctx.attribute_designator().getText()
            a_memb['expr'] = self.try_eval_expr(ctx.expression().getText())
            if a_memb['attr'].lower() == 'size':
                self.cur_type_dec['size'][a_memb['type']] =  a_memb
        self.cur_stat = self.FULL_TYPE
        #pprint.pprint(self.cur_type_dec)
        out =[]
        for memb in self.cur_type_dec['memb']['fields']:
            self.cur_type_dec['memb']['list'][memb].update(self.cur_type_dec['pos']['list'][memb])
        for memb in self.cur_type_dec['pos']['fields']:
            print('%s: %s' % (memb, self.cur_type_dec['memb']['list'][memb]))
        print(self.unsolved)

