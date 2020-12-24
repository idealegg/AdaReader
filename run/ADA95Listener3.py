# Generated from ADA95.g4 by ANTLR 4.7.2
from antlr4 import *
from run.ADA95Listener import ADA95Listener
from run.ADA95Parser import ADA95Parser
from common.ada_spec import AdaSpec
from common.ada_record_type import AdaRecordType
from common.ada_record_field import AdaRecordField
from common.ada_enum_type import AdaEnumType
from common.ada_array_index import AdaArrayIndex
from common.ada_int_type import AdaIntType
from common.ada_real_type import AdaRealType
from common.ada_array_type import AdaArrayType
from common.ada_derived_type import AdaDerivedType
from common.ada_subtype import AdaSubtype
from common.ada_type import AdaType
from common.ada_var import AdaVar
from common.ada_enum_item import AdaEnumItem
import common.parse_util as cpu
from util.file_mng import FileMng
import pprint
import re
from util.myLogging import logger as my_log
from util.myLogging import log


# This class defines a complete listener for a parse tree produced by ADA95Parser.
class ADA95Listener3(ADA95Listener):
    def __init__(self, ctx):
        self.ctx = ctx
        self.MARK_PATTERN = re.compile('[\w.]+')
        #self.cur_mod = None

    def get_cur_submark(self, ctx):
        cur_mark = re.search(self.MARK_PATTERN, cpu.get_texts(ctx.subtype_mark()))
        cur_mark = cur_mark.group()
        return cur_mark

    def check_state(self, state, ctx):
        is_set = isinstance(state, (list, tuple, set))
        if is_set and self.ctx.cur_fm.cur_states[-1] not in state or not is_set and self.ctx.cur_fm.cur_states[-1] != state:
            my_log.error("State error, Current: [%s], Stored: [%s], Rule: [%s]" %
                         (state, self.ctx.cur_fm.cur_states[-1], ADA95Parser.ruleNames[ctx.getRuleIndex()]))

    def exit_state(self, state, ctx):
        self.check_state(state, ctx)
        self.ctx.cur_fm.cur_states.pop()
    # Enter a parse tree produced by ADA95Parser#compilation_unit_lib.
    #def enterCompilation_unit_lib(self, ctx:ADA95Parser.Compilation_unit_libContext):
    #    self.ctx.cur_spec = AdaSpec(
    #        ctx.parser.getTokenStream().tokenSource.inputStream.fileName,
    #        self.ctx)

    # Exit a parse tree produced by ADA95Parser#compilation_unit_lib.
    #def exitCompilation_unit_lib(self, ctx:ADA95Parser.Compilation_unit_libContext):
    #    self.ctx.cur_spec = None
        #pass

    # Exit a parse tree produced by ADA95Parser#with_clause.
    def exitWith_clause(self, ctx:ADA95Parser.With_clauseContext):
        if self.ctx.cur_spec:
            self.ctx.cur_spec.add_with(cpu.get_texts(ctx.library_unit_name()))
        else:
            self.ctx.cur_fm.add_with(cpu.get_texts(ctx.library_unit_name()))

    def exitUse_package_clause(self, ctx):
        if self.ctx.cur_spec:
            self.ctx.cur_spec.add_use(cpu.get_texts(ctx.package_name()))
        else:
            self.ctx.cur_fm.add_use(cpu.get_texts(ctx.package_name()))

    def exitUse_type_clause(self, ctx):
        if self.ctx.cur_spec:
            self.ctx.cur_spec.add_use_types(cpu.get_texts(ctx.subtype_mark()))
        else:
            self.ctx.cur_fm.add_use_types(cpu.get_texts(ctx.subtype_mark()))

    @log('ADA95Listener3')
    def enterPackage_specification(self, ctx):
        self.ctx.cur_fm.cur_states.append(FileMng.States.PACKAGE)
        if self.ctx.cur_spec:
            self.ctx.cur_spec_list.append(self.ctx.cur_spec)
        self.ctx.cur_spec = AdaSpec(
                ctx.parser.getTokenStream().tokenSource.inputStream.fileName,
                self.ctx)
        self.ctx.cur_spec.uses.update(map(lambda x: x.package, self.ctx.cur_spec_list))
        self.ctx.cur_spec.package = cpu.get_texts(ctx.defining_program_unit_name()).upper()
        if self.ctx.cur_spec_list:
            self.ctx.cur_spec.package = ".".join([self.ctx.cur_spec_list[-1].package, self.ctx.cur_spec.package])
            self.ctx.cur_spec.withs.add(self.ctx.cur_spec_list[0].package)
        self.ctx.cur_spec.uses.update(self.ctx.cur_fm.uses)
        self.ctx.cur_spec.withs.update(self.ctx.cur_fm.withs)
        self.ctx.cur_spec.use_types.update(self.ctx.cur_fm.use_types)
        my_log.debug("enterPackage_specification: %s" % self.ctx.cur_spec.package)
        my_log.debug("withs: %s" % self.ctx.cur_spec.withs)
        my_log.debug("uses: %s" % self.ctx.cur_spec.uses)

    def exitPackage_specification(self, ctx):
        if self.ctx.cur_spec_list:
            self.ctx.cur_fm.withs.add(self.ctx.cur_spec.package)
            self.ctx.cur_spec = self.ctx.cur_spec_list.pop()
        else:
            self.ctx.cur_spec = None
        self.exit_state(FileMng.States.PACKAGE, ctx)

    # Enter a parse tree produced by ADA95Parser#type_definition_clause.
    def enterType_definition_clause(self, ctx: ADA95Parser.Type_definition_clauseContext):
        if self.ctx.cur_spec is not None:
            self.ctx.cur_fm.cur_states.append(FileMng.States.TYPE)
            self.ctx.cur_type = cpu.get_texts(ctx.defining_identifier())
            self.ctx.cur_discrim = []

    # Exit a parse tree produced by ADA95Parser#type_definition_clause.
    @log('ADA95Listener3')
    def exitType_definition_clause(self, ctx: ADA95Parser.Type_definition_clauseContext):
        if self.ctx.cur_spec is not None:
            if isinstance(self.ctx.cur_type, str):
                my_log.info('ignore type: %s' % self.ctx.cur_type)
            else:
                #self.ctx.cur_type.print()
                self.ctx.cur_spec.add_type(self.ctx.cur_type)
                #print("exitType_definition_clause:")
                #pprint.pprint(self.ctx.cur_spec.types)
            self.ctx.cur_type = None
            self.ctx.cur_discrim = None
            self.exit_state(FileMng.States.TYPE, ctx)

    def exitDiscriminant_specification(self, ctx):
        if self.ctx.cur_spec is not None:
            if self.ctx.cur_discrim is not None:
                a_memb = AdaRecordField(self.ctx.cur_idents.pop(), self.ctx.cur_type, self.ctx)
                a_memb.solve_field_type(self.get_cur_submark(ctx))
                def_val = ctx.default_expression()
                a_memb.solve_default(cpu.get_texts(def_val) if def_val else None)
                self.ctx.cur_discrim.append(a_memb)
                for ident in self.ctx.cur_idents:
                    self.ctx.cur_discrim.append(a_memb.copy(ident))

    @log('Ada95listener')
    def enterEnumeration_type_definition(self, ctx):
        if self.ctx.cur_spec is not None:
            self.ctx.cur_type = AdaEnumType(
                self.ctx.cur_type,
                self.ctx.cur_spec.package,
                self.ctx)
            #if self.ctx.cur_discrim:
            #    self.ctx.cur_type.add_discrim(self.ctx.cur_discrim)
            enums = cpu.get_texts(ctx.enumeration_literal_specification())
            my_log.debug("enterEnumeration_type_definition: %s" % enums)
            for e in enums:
                e_item = AdaEnumItem(e, self.ctx.cur_type, self.ctx)
                self.ctx.cur_type.add_enum(e_item)
                self.ctx.cur_spec.add_enum(e_item)
            my_log.debug(self.ctx.cur_type)
            self.ctx.cur_field = None

    def enterDerived_type_definition(self, ctx):
        if self.ctx.cur_spec is not None:
            self.ctx.cur_type = AdaDerivedType(
                self.ctx.cur_type,
                self.ctx.cur_spec.package,
                self.ctx)

    def enterSubtype_declaration(self, ctx):
        if self.ctx.cur_spec is not None:
            self.ctx.cur_fm.cur_states.append(FileMng.States.TYPE)
            self.ctx.cur_type = AdaSubtype(
                cpu.get_texts(ctx.defining_identifier()),
                self.ctx.cur_spec.package,
                self.ctx)

    @log('ADA95Listener3')
    def exitSubtype_declaration(self, ctx):
        if self.ctx.cur_spec is not None:
            if isinstance(self.ctx.cur_type, str):
                my_log.info('ignore type: %s' % self.ctx.cur_type)
            else:
                #self.ctx.cur_type.print()
                self.ctx.cur_type.solve_constraint(self.ctx.cur_const)
                self.ctx.cur_spec.add_type(self.ctx.cur_type)
                #print("exitType_definition_clause:")
                #pprint.pprint(self.ctx.cur_spec.types)
            self.ctx.cur_type = None
            self.ctx.cur_discrim = None
            self.exit_state(FileMng.States.TYPE, ctx)

    def enterSubtype_indication(self, ctx):
        if self.ctx.cur_spec is not None:
            if self.ctx.cur_fm.cur_states[-1] == FileMng.States.VAR:
                self.ctx.cur_fm.cur_states.append(FileMng.States.VAR_TYPE)
            elif self.ctx.cur_fm.cur_states[-1] == FileMng.States.TYPE:
                self.ctx.cur_fm.cur_states.append(FileMng.States.SUB_DER_TYPE)
            elif self.ctx.cur_fm.cur_states[-1] == FileMng.States.FIELD:
                self.ctx.cur_fm.cur_states.append(FileMng.States.FIELD_TYPE)
            elif self.ctx.cur_fm.cur_states[-1] == FileMng.States.ARRAY_DEFINE:
                self.ctx.cur_fm.cur_states.append(FileMng.States.ARRAY_ELEM)

    @log('ADA95Listener3')
    def exitSubtype_indication(self, ctx):
        if self.ctx.cur_spec is not None:
            cur_mark = self.get_cur_submark(ctx)
            if self.ctx.cur_fm.cur_states[-1] == FileMng.States.SUB_DER_TYPE and self.ctx.cur_type:
                if not isinstance(self.ctx.cur_type, str):
                    my_log.debug("exitSubtype_indication1: %s" % self.ctx.cur_type)
                    my_log.debug('cur_const: %s' % self.ctx.cur_const)
                    self.ctx.cur_type.solve_constraint(self.ctx.cur_const)
                    my_log.debug("exitSubtype_indication2: %s" % self.ctx.cur_type)
                    self.ctx.cur_type.solve_based(cur_mark)
                    my_log.debug("exitSubtype_indication3: %s" % self.ctx.cur_type)
                else:
                    my_log.error("Type error [%s:%s, %s:%s] %s" % (ctx.start.line,
                                                 ctx.start.column,
                                                 ctx.stop.line,
                                                 ctx.stop.column,
                                                 self.ctx.cur_type
                                                 ))
            elif self.ctx.cur_fm.cur_states[-1] == FileMng.States.VAR_TYPE and self.ctx.cur_var:
                if not isinstance(self.ctx.cur_var, str):
                    self.ctx.cur_var.solve_data_type(cur_mark)
                    self.ctx.cur_var.solve_constraint(self.ctx.cur_const)
                else:
                    my_log.error("Var error [%s:%s, %s:%s] %s" % (ctx.start.line,
                                                 ctx.start.column,
                                                 ctx.stop.line,
                                                 ctx.stop.column,
                                                 self.ctx.cur_var
                                                 ))
            elif self.ctx.cur_fm.cur_states[-1] == FileMng.States.FIELD_TYPE:
                self.ctx.cur_field = {'based': cur_mark,
                                      'constraint': self.ctx.cur_const}
            elif self.ctx.cur_fm.cur_states[-1] == FileMng.States.ARRAY_ELEM:
                self.ctx.cur_type.solve_elem(cur_mark)
            if self.ctx.cur_fm.cur_states[-1] in [FileMng.States.SUB_DER_TYPE,
                                                  FileMng.States.VAR_TYPE,
                                                  FileMng.States.FIELD_TYPE,
                                                  FileMng.States.ARRAY_ELEM,
                                                  ]:
                self.ctx.cur_const = None
                self.ctx.cur_range = None
                self.exit_state([FileMng.States.SUB_DER_TYPE,
                                                  FileMng.States.VAR_TYPE,
                                                  FileMng.States.FIELD_TYPE,
                                                  FileMng.States.ARRAY_ELEM,
                                                  ], ctx)



    def enterRange_constraint(self, ctx):
        if self.ctx.cur_spec is not None:
            if not self.ctx.cur_const:
                self.ctx.cur_const = {'type': 'range'}

    def enterDigits_constraint(self, ctx):
        if self.ctx.cur_spec is not None:
            if not self.ctx.cur_const:
                self.ctx.cur_const = {'type': 'digits'}

    def enterDelta_constraint(self, ctx):
        if self.ctx.cur_spec is not None:
            if not self.ctx.cur_const:
                self.ctx.cur_const = {'type': 'delta'}

    def enterIndex_constraint(self, ctx):
        if self.ctx.cur_spec is not None:
            if not self.ctx.cur_const:
                self.ctx.cur_const = {'type': 'index'}

    def enterKnown_discriminant_part(self, ctx):
        if self.ctx.cur_spec is not None:
            self.ctx.cur_fm.cur_states.append(FileMng.States.DISCRIMINANT)

    def exitKnown_discriminant_part(self, ctx):
        if self.ctx.cur_spec is not None:
            self.exit_state(FileMng.States.DISCRIMINANT, ctx)

    def enterDiscriminant_constraint(self, ctx):
        if self.ctx.cur_spec is not None:
            if not self.ctx.cur_const:
                self.ctx.cur_const = {'type': 'discrim', 'choice': {}}

    def exitDigits_constraint(self, ctx):
        if self.ctx.cur_spec is not None:
            self.ctx.cur_const.update({
                'digits': cpu.solve_expr(self.ctx, cpu.get_texts(ctx.expression()))[0],
                'range': self.ctx.cur_range})

    def exitDelta_constraint(self, ctx):
        if self.ctx.cur_spec is not None:
            self.ctx.cur_const.update({
                'delta': cpu.solve_expr(self.ctx, cpu.get_texts(ctx.expression()))[0],
                'range': self.ctx.cur_range})

    def exitIndex_constraint(self, ctx):
        if self.ctx.cur_spec is not None:
            self.ctx.cur_const.update({
                'discrete': cpu.get_texts(ctx.discrete_range())})

    def exitDiscriminant_association(self, ctx):
        if self.ctx.cur_spec is not None:
            for n in cpu.get_texts(ctx.discriminant_selector_name()):
                self.ctx.cur_const['choice'][n] = cpu.solve_expr(
                    self.ctx,
                    cpu.get_texts(ctx.expression()))[0]

    @log('ADA95Listener3')
    def exitRange_state(self, ctx):
        if self.ctx.cur_spec is not None:
            self.ctx.cur_range = {}
            rar = ctx.range_attribute_reference()
            if rar:
                rar = cpu.get_texts(rar)
                self.ctx.cur_range = {'type': 'attr', 'base': rar[:rar.find("'")]}
            else:
                self.ctx.cur_range = {'type': 'range',
                                                'first': cpu.solve_expr(self.ctx, cpu.get_texts(ctx.simple_expression(0)))[0],
                                                'last': cpu.solve_expr(self.ctx, cpu.get_texts(ctx.simple_expression(1)))[0]
                                                }
            if self.ctx.cur_const and self.ctx.cur_const['type'] == 'range':
                self.ctx.cur_const.update({'range': self.ctx.cur_range})  # always here
                my_log.debug("exitRange_state1: %s" % self.ctx.cur_type)
                my_log.debug("exitRange_state2: %s" % self.ctx.cur_const)
            elif self.ctx.cur_fm.cur_states[-1] == FileMng.States.SUB_DER_TYPE:
                self.ctx.cur_const = {'type': 'range',
                                                    'range': self.ctx.cur_range}
                my_log.debug("exitRange_state3: %s" % self.ctx.cur_type)
                my_log.debug("exitRange_state4: %s" % self.ctx.cur_const)
            elif self.ctx.cur_fm.cur_states[-1] in (FileMng.States.FIELD_TYPE, FileMng.States.VAR_TYPE, FileMng.States.ARRAY_DEFINE):
                self.ctx.cur_const = {'type': 'range',
                                      'range': self.ctx.cur_range}
            else:
                my_log.error("ignore range statement: %s" % ctx.getText())

    def exitEnumeration_type_definition(self, ctx):
        pass

    def enterRecord_type_definition(self, ctx):
        if self.ctx.cur_spec is not None:
            self.ctx.cur_type = AdaRecordType(
                self.ctx.cur_type,
                self.ctx.cur_spec.package,
                self.ctx)
            if self.ctx.cur_discrim:
                self.ctx.cur_type.add_discrim(self.ctx.cur_discrim)
                self.ctx.cur_type.add_fields(self.ctx.cur_discrim)
            self.ctx.cur_field = []

    def exitRecord_type_definition(self, ctx):
        pass

    def exitDefining_identifier_list(self, ctx):
        if self.ctx.cur_spec is not None:
            self.ctx.cur_idents = cpu.get_texts(ctx.defining_identifier())

    def enterComponent_declaration(self, ctx):
        if self.ctx.cur_spec is not None:
            self.ctx.cur_fm.cur_states.append(FileMng.States.FIELD)

    def exitComponent_declaration(self, ctx):
        if self.ctx.cur_spec is not None:
            cur_fields = []
            a_memb = AdaRecordField(self.ctx.cur_idents.pop(), self.ctx.cur_type.name, self.ctx)
            #a_memb.solve_type(cpu.get_texts(ctx.component_definition()))
            a_memb.solve_constraint(self.ctx.cur_field['constraint'])
            a_memb.solve_field_type(self.ctx.cur_field['based'])
            def_val = ctx.default_expression()
            a_memb.solve_default(cpu.get_texts(def_val) if def_val else None)
            cur_fields.append(a_memb)
            for ident in self.ctx.cur_idents:
                cur_fields.append(a_memb.copy(ident))
            self.ctx.cur_type.add_fields(cur_fields)
            #self.ctx.cur_type.print()
            self.exit_state(FileMng.States.FIELD, ctx)

    #def enterComponent_definition(self, ctx):
    #    self.ctx.cur_fm.cur_states.append(FileMng.States.FIELD_TYPE)

    #def exitComponent_definition(self, ctx):
    #    self.ctx.cur_fm.cur_states.pop()

    def enterRecord_representation_clause(self, ctx):
        if self.ctx.cur_spec is not None:
            self.ctx.cur_type = None
            self.ctx.cur_field = None

    def enterFirst_subtype_local_name(self, ctx):
        if self.ctx.cur_spec is not None:
            self.ctx.cur_type = cpu.find_name(
                cpu.get_texts(ctx.local_name()),
                self.ctx,
                'type')[0]

    def exitRecord_representation_clause(self, ctx):
        if self.ctx.cur_spec is not None:
            if not isinstance(self.ctx.cur_type, str):
                mod_cls = ctx.mod_clause()
                if mod_cls is not None:
                    mod_cls = cpu.get_texts(mod_cls)
                else:
                    mod_cls = None
                self.ctx.cur_spec.types[self.ctx.cur_type.package][self.ctx.cur_type.name].mod_clause = mod_cls
                #self.ctx.types[self.ctx.cur_type.package][self.ctx.cur_type.name].mod_clause = mod_cls

    @log('ADA95Listener3')
    def exitComponent_clause(self, ctx):
        if self.ctx.cur_spec is not None:
            field_n = cpu.get_texts(ctx.component_local_name()).upper()
            my_log.debug("exitComponent_clause: %s" % field_n)
            cur_type = self.ctx.cur_spec.types[self.ctx.cur_type.package][self.ctx.cur_type.name]
            my_log.debug(self.ctx.cur_type.package)
            my_log.debug(self.ctx.cur_type.name)
            cur_type.fields[field_n].solve_pos(cpu.get_texts(ctx.position()))
            cur_type.fields[field_n].solve_start_bit(cpu.get_texts(ctx.first_bit()))
            cur_type.fields[field_n].solve_end_bit(cpu.get_texts(ctx.last_bit()))
            cur_type.add_pos(field_n)
            my_log.debug(cur_type.fields[field_n])
            my_log.debug(cur_type.fpos)


    def exitArray_component_association(self, ctx):
        if self.ctx.cur_spec is not None:
            if self.ctx.cur_type and (not isinstance(self.ctx.cur_type, str)):
                if self.ctx.cur_type.ttype == AdaType.ENUM_TYPE:
                    self.ctx.cur_type.items[(cpu.get_texts(ctx.discrete_choice_list()).upper())].solve_value(
                        cpu.get_texts(ctx.expression())
                    )

    def exitAttribute_definition_clause(self, ctx):
        if self.ctx.cur_spec is not None:
            self.ctx.cur_type = cpu.find_name(
                cpu.get_texts(ctx.local_name()),
                self.ctx,
                'type')[0]
            if not isinstance(self.ctx.cur_type, str):
                attr = cpu.get_texts(ctx.attribute_designator())
                if attr.lower() == 'size':
                    self.ctx.cur_spec.types[self.ctx.cur_type.package][
                        self.ctx.cur_type.name].solve_size(cpu.get_texts(ctx.expression()))

    def enterNumber_declaration(self, ctx):
        if self.ctx.cur_spec is not None:
            self.ctx.cur_fm.cur_states.append(FileMng.States.VAR)

    @log('ADA95Listener3')
    def exitNumber_declaration(self, ctx):
        if self.ctx.cur_spec is not None:
            av = AdaVar(self.ctx.cur_idents.pop(),
                        self.ctx.cur_spec.package,
                        self.ctx)
            av.solve_value(cpu.get_texts(ctx.expression()))
            self.ctx.cur_spec.add_var(av)
            my_log.debug("exitNumber_declaration: %s" % av)
            for ident in self.ctx.cur_idents:
                self.ctx.cur_spec.add_var(av.copy(ident))
            self.exit_state(FileMng.States.VAR, ctx)

    def enterUnconstrained_array_definition(self, ctx):
        if self.ctx.cur_spec is not None:
            if self.ctx.cur_fm.cur_states[-1] == FileMng.States.VAR:
                self.ctx.cur_fm.cur_states.append(FileMng.States.VAR_TYPE)
            elif self.ctx.cur_fm.cur_states[-1] == FileMng.States.TYPE:
                self.ctx.cur_fm.cur_states.append(FileMng.States.ARRAY_DEFINE)
                if isinstance(self.ctx.cur_type, str):
                    self.ctx.cur_type = AdaArrayType(self.ctx.cur_type,
                                                           self.ctx.cur_spec.package,
                                                           self.ctx
                                                           )

    def exitUnconstrained_array_definition(self, ctx):
        if self.ctx.cur_spec is not None:
            if self.ctx.cur_fm.cur_states[-1] in (FileMng.States.VAR_TYPE, FileMng.States.ARRAY_DEFINE):
                self.exit_state((FileMng.States.VAR_TYPE, FileMng.States.ARRAY_DEFINE), ctx)

    def exitIndex_subtype_definition(self, ctx):
        if self.ctx.cur_spec is not None:
            if self.ctx.cur_fm.cur_states[-1] == FileMng.States.ARRAY_DEFINE and self.ctx.cur_type:
                a_index = AdaArrayIndex(self.ctx.cur_type,
                                        self.get_cur_submark(ctx),
                                        self.ctx.cur_const
                                        )
                a_index.solve_constraint()
                a_index.solve_based()
                self.ctx.cur_type.add_index(a_index)
                self.ctx.cur_const = None

    def enterConstrained_array_definition(self, ctx):
        if self.ctx.cur_spec is not None:
            if self.ctx.cur_fm.cur_states[-1] == FileMng.States.VAR:
                self.ctx.cur_fm.cur_states.append(FileMng.States.VAR_TYPE)
            elif self.ctx.cur_fm.cur_states[-1] == FileMng.States.TYPE:
                self.ctx.cur_fm.cur_states.append(FileMng.States.ARRAY_DEFINE)
                if isinstance(self.ctx.cur_type, str):
                    self.ctx.cur_type = AdaArrayType(self.ctx.cur_type,
                                                               self.ctx.cur_spec.package,
                                                               self.ctx
                                                               )

    def exitConstrained_array_definition(self, ctx):
        if self.ctx.cur_spec is not None:
            if self.ctx.cur_fm.cur_states[-1] in (FileMng.States.VAR_TYPE, FileMng.States.ARRAY_DEFINE):
                self.exit_state((FileMng.States.VAR_TYPE, FileMng.States.ARRAY_DEFINE), ctx)

    def exitDiscrete_subtype_definition(self, ctx):
        if self.ctx.cur_spec is not None:
            if self.ctx.cur_fm.cur_states[-1] == FileMng.States.ARRAY_DEFINE and self.ctx.cur_type:
                dsi = ctx.discrete_subtype_indication()
                if dsi:
                    cur_mark = re.search(self.MARK_PATTERN, cpu.get_texts(dsi))
                    cur_mark = cur_mark.group()
                    a_index = AdaArrayIndex(self.ctx.cur_type, cur_mark, None)
                    a_index.solve_constraint()
                    a_index.solve_based()
                    self.ctx.cur_type.add_index(a_index)
                else:
                    a_index = AdaArrayIndex(self.ctx.cur_type, None, self.ctx.cur_const)
                    a_index.solve_constraint()
                    a_index.solve_based()
                    self.ctx.cur_type.add_index(a_index)
                    self.ctx.cur_const = None

    def exitSigned_integer_type_definition(self, ctx):
        if self.ctx.cur_spec is not None:
            self.ctx.cur_type = AdaIntType(self.ctx.cur_type,
                                                     self.ctx.cur_spec.package,
                                                     self.ctx,
                                                     )
            self.ctx.cur_type.solve_first(cpu.get_texts(ctx.simple_expression(0)))
            self.ctx.cur_type.solve_last(cpu.get_texts(ctx.simple_expression(1)))

    def exitModular_type_definition(self, ctx):
        if self.ctx.cur_spec is not None:
            self.ctx.cur_type = AdaIntType(self.ctx.cur_type,
                                                     self.ctx.cur_spec.package,
                                                     self.ctx,
                                                    )
            self.ctx.cur_type.solve_mod(cpu.get_texts(ctx.expression()))
            self.ctx.cur_type.print()

    def enterFloating_point_definition(self, ctx):
        if self.ctx.cur_spec is not None:
            self.ctx.cur_type = AdaRealType(self.ctx.cur_type,
                                                     self.ctx.cur_spec.package,
                                                     self.ctx)

    def exitFloating_point_definition(self, ctx):
        if self.ctx.cur_spec is not None:
            self.ctx.cur_type.solve_digits(cpu.get_texts(ctx.expression()))

    def enterOrdinary_fixed_point_definition(self, ctx):
        if self.ctx.cur_spec is not None:
            self.ctx.cur_type = AdaRealType(self.ctx.cur_type,
                                                      self.ctx.cur_spec.package,
                                                      self.ctx)

    def exitOrdinary_fixed_point_definition(self, ctx):
        if self.ctx.cur_spec is not None:
            self.ctx.cur_type.solve_delta(cpu.get_texts(ctx.expression()))

    def enterDecimal_fixed_point_definition(self, ctx):
        if self.ctx.cur_spec is not None:
            self.ctx.cur_type = AdaRealType(self.ctx.cur_type,
                                                      self.ctx.cur_spec.package,
                                                      self.ctx)

    def exitDecimal_fixed_point_definition(self, ctx):
        if self.ctx.cur_spec is not None:
            self.ctx.cur_type.solve_delta(cpu.get_texts(ctx.expression(0)))
            self.ctx.cur_type.solve_digits(cpu.get_texts(ctx.expression(1)))

    def exitReal_range_specification(self, ctx):
        if self.ctx.cur_spec is not None:
            self.ctx.cur_type.solve_first(cpu.get_texts(ctx.simple_expression(0)))

            self.ctx.cur_type.solve_last(cpu.get_texts(ctx.simple_expression(1)))

    def enterObject_declaration(self, ctx):
        if self.ctx.cur_spec is not None:
            self.ctx.cur_fm.cur_states.append(FileMng.States.VAR)
            self.ctx.cur_var = AdaVar(None,
                        self.ctx.cur_spec.package,
                        self.ctx)

    def exitObject_declaration(self, ctx):
        if self.ctx.cur_spec is not None:
            self.ctx.cur_var.set_name(self.ctx.cur_idents.pop())
            obj_val = ctx.object_value()
            self.ctx.cur_var.solve_value(cpu.get_texts(obj_val) if obj_val else None)
            self.ctx.cur_spec.add_var(self.ctx.cur_var)
            for ident in self.ctx.cur_idents:
                self.ctx.cur_spec.add_var(self.ctx.cur_var.copy(ident))
            self.ctx.cur_var = None
            self.exit_state(FileMng.States.VAR, ctx)

    #def exitMod_clause(self, ctx):
    #    if self.ctx.cur_spec is not None:
    #        self.cur_mod, dummy = cpu.solve_expr(self.ctx, cpu.get_texts(ctx.expression()))