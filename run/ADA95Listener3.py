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

    def enterPackage_specification(self, ctx):
        self.ctx.cur_fm.cur_states.append(FileMng.States.PACKAGE)
        if self.ctx.cur_spec:
            self.ctx.cur_spec_list.append(self.ctx.cur_spec)
        self.ctx.cur_spec = AdaSpec(
                ctx.parser.getTokenStream().tokenSource.inputStream.fileName,
                self.ctx)
        self.ctx.cur_spec.package = cpu.get_texts(ctx.defining_program_unit_name()).upper()

    def exitPackage_specification(self, ctx):
        if self.ctx.cur_spec_list:
            self.ctx.cur_spec = self.ctx.cur_spec_list.pop()
        else:
            self.ctx.cur_spec = None
        self.ctx.cur_fm.cur_states.pop()

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
            self.ctx.cur_fm.cur_states.pop()

    def exitDiscriminant_specification(self, ctx):
        if self.ctx.cur_spec is not None:
            if self.ctx.cur_discrim is not None:
                a_memb = AdaRecordField(self.ctx.cur_idents.pop(), self.ctx.cur_type, self.ctx)
                a_memb.solve_type(cpu.get_texts(ctx.subtype_mark()))
                def_val = ctx.default_expression()
                if def_val is not None:
                    a_memb.solve_default(cpu.get_texts(def_val))
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
            if self.ctx.cur_discrim:
                self.ctx.cur_type.add_discrim(self.ctx.cur_discrim)
            enums = cpu.get_texts(ctx.enumeration_literal_specification())
            my_log.debug("enterEnumeration_type_definition: %s" % enums)
            self.ctx.cur_type.add_enum(enums)
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
                # self.ctx.cur_type.print()
                self.ctx.cur_spec.add_type(self.ctx.cur_type)
                # print("exitType_definition_clause:")
                # pprint.pprint(self.ctx.cur_spec.types)
            self.ctx.cur_type = None
            self.ctx.cur_discrim = None
            self.ctx.cur_fm.cur_states.pop()

    def enterSubtype_indication(self, ctx):
        if self.ctx.cur_spec is not None:
            if self.ctx.cur_fm.cur_states[-1] == FileMng.States.VAR:
                self.ctx.cur_fm.cur_states.append(FileMng.States.VAR_TYPE)
            elif self.ctx.cur_fm.cur_states[-1] == FileMng.States.TYPE:
                self.ctx.cur_fm.cur_states.append(FileMng.States.SUB_DER_TYPE)
            elif self.ctx.cur_fm.cur_states[-1] == FileMng.States.FIELD:
                self.ctx.cur_fm.cur_states.append(FileMng.States.FIELD_TYPE)
            elif self.ctx.cur_fm.cur_states[-1] == FileMng.States.FIELD:
                self.ctx.cur_fm.cur_states.append(FileMng.States.FIELD_TYPE)
            elif self.ctx.cur_fm.cur_states[-1] == FileMng.States.ARRAY_DEFINE:
                self.ctx.cur_fm.cur_states.append(FileMng.States.ARRAY_ELEM)

    @log('ADA95Listener3')
    def exitSubtype_indication(self, ctx):
        if self.ctx.cur_spec is not None:
            #rollback = False
            cur_mark = re.search(self.MARK_PATTERN, cpu.get_texts(ctx.subtype_mark()))
            cur_mark = cur_mark.group()
            if self.ctx.cur_fm.cur_states[-1] == FileMng.States.SUB_DER_TYPE and self.ctx.cur_type:
                if not isinstance(self.ctx.cur_type, str):
                    self.ctx.cur_type.based = cur_mark
                    if self.ctx.cur_const and not self.ctx.cur_type.constraint:
                        self.ctx.cur_type.constraint = self.ctx.cur_const
                    self.ctx.cur_type.solve_constraint()
                else:
                    my_log.error("Type error [%s:%s, %s:%s] %s" % (ctx.start.line,
                                                 ctx.start.column,
                                                 ctx.stop.line,
                                                 ctx.stop.column,
                                                 self.ctx.cur_type
                                                 ))
            elif self.ctx.cur_fm.cur_states[-1] == FileMng.States.VAR_TYPE and self.ctx.cur_var:
                if not isinstance(self.ctx.cur_var, str):
                    self.ctx.cur_var.based = cur_mark
                    self.ctx.cur_var.constraint = self.ctx.cur_const
                    self.ctx.cur_var.solve_type(self.ctx.cur_var.based)
                    self.ctx.cur_var.solve_constraint()
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
                self.ctx.cur_type.elem = cur_mark
            if self.ctx.cur_fm.cur_states[-1] in [FileMng.States.SUB_DER_TYPE,
                                                  FileMng.States.VAR_TYPE,
                                                  FileMng.States.FIELD_TYPE,
                                                  FileMng.States.ARRAY_ELEM,
                                                  ]:
                self.ctx.cur_const = None
                self.ctx.cur_range = None
                self.ctx.cur_fm.cur_states.pop()



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
            self.ctx.cur_fm.cur_states.pop()

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
                self.ctx.cur_const.update({'range': self.ctx.cur_range})
            elif self.ctx.cur_fm.cur_states[-1] == FileMng.States.SUB_DER_TYPE:
                self.ctx.cur_type.constraint = {'type': 'range',
                                                'range': self.ctx.cur_range}
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
            a_memb.based = self.ctx.cur_field['based']
            a_memb.constraint = self.ctx.cur_field['constraint']
            a_memb.solve_type(self.ctx.cur_field['based'])
            a_memb.solve_constraint()
            def_val = ctx.default_expression()
            if def_val is not None:
                a_memb.solve_default(cpu.get_texts(def_val))
            #print("cur_field: %s" % self.ctx.cur_field)
            #self.ctx.cur_field.print()
            #a_memb.print()
            cur_fields.append(a_memb)
            for ident in self.ctx.cur_idents:
                cur_fields.append(a_memb.copy(ident))
            self.ctx.cur_type.add_fields(cur_fields)
            #self.ctx.cur_type.print()
            self.ctx.cur_fm.cur_states.pop()

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

    def exitComponent_clause(self, ctx):
        if self.ctx.cur_spec is not None:
            a_memb = {}
            a_memb['name'] = cpu.get_texts(ctx.component_local_name()).upper()
            a_memb['pos'] = cpu.get_texts(ctx.position())
            a_memb['start'] = cpu.get_texts(ctx.first_bit())
            a_memb['end'] = cpu.get_texts(ctx.last_bit())
            #self.ctx.cur_type.print()
            #pprint.pprint(self.ctx.cur_spec.types)
            self.ctx.cur_spec.types[self.ctx.cur_type.package][
                self.ctx.cur_type.name].add_pos(a_memb)
            #self.ctx.types[self.ctx.cur_type.package][self.ctx.cur_type.name].add_pos(a_memb)

    def exitArray_component_association(self, ctx):
        if self.ctx.cur_spec is not None:
            if self.ctx.cur_type and (not isinstance(self.ctx.cur_type, str)):
                if self.ctx.cur_type.ttype == AdaType.ENUM_TYPE:
                    self.ctx.cur_type.add_val(
                        cpu.get_texts(ctx.discrete_choice_list()),
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
                    #self.ctx.types[self.ctx.cur_type.package][self.ctx.cur_type.name].size = self.ctx.cur_spec.types[self.ctx.cur_type.package][
                    #    self.ctx.cur_type.name].size

    def enterNumber_declaration(self, ctx):
        if self.ctx.cur_spec is not None:
            self.ctx.cur_fm.cur_states.append(FileMng.States.VAR)

    def exitNumber_declaration(self, ctx):
        if self.ctx.cur_spec is not None:
            av = AdaVar(self.ctx.cur_idents.pop(),
                        self.ctx.cur_spec.package,
                        self.ctx)
            av.solve_value(cpu.get_texts(ctx.expression()))
            av.const = True
            self.ctx.cur_spec.add_var(av)
            for ident in self.ctx.cur_idents:
                self.ctx.cur_spec.add_var(av.copy(ident))
            self.ctx.cur_fm.cur_states.pop()

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
            if self.ctx.cur_fm.cur_states[-1] == FileMng.States.ARRAY_DEFINE and self.ctx.cur_type:
                self.ctx.cur_type.solve_elem_type()
                self.ctx.cur_type.is_solved()
            if self.ctx.cur_fm.cur_states[-1] in (FileMng.States.VAR_TYPE, FileMng.States.ARRAY_DEFINE):
                self.ctx.cur_fm.cur_states.pop()

    def exitIndex_subtype_definition(self, ctx):
        if self.ctx.cur_spec is not None:
            if self.ctx.cur_fm.cur_states[-1] == FileMng.States.ARRAY_DEFINE and self.ctx.cur_type:
                a_index = AdaArrayIndex(self.ctx.cur_type,
                                        cpu.get_texts(ctx.subtype_mark()),
                                        self.ctx.cur_const
                                        )
                a_index.solve_based()
                a_index.solve_constraint()
                self.ctx.cur_type.add_index(a_index)

    def enterConstrained_array_definition(self, ctx):
        if self.ctx.cur_spec is not None:
            if self.ctx.cur_fm.cur_states[-1] == FileMng.States.Var:
                self.ctx.cur_fm.cur_states.append(FileMng.States.VAR_TYPE)
            elif self.ctx.cur_fm.cur_states[-1] == FileMng.States.Type:
                self.ctx.cur_fm.cur_states.append(FileMng.States.ARRAY_DEFINE)
                if isinstance(self.ctx.cur_type, str):
                    self.ctx.cur_type = AdaArrayType(self.ctx.cur_type,
                                                               self.ctx.cur_spec.package,
                                                               self.ctx
                                                               )

    def exitConstrained_array_definition(self, ctx):
        if self.ctx.cur_spec is not None:
            if self.ctx.cur_fm.cur_states[-1] == FileMng.States.ARRAY_DEFINE and self.ctx.cur_type:
                self.ctx.cur_type.solve_elem_type()
                self.ctx.cur_type.is_solved()
            if self.ctx.cur_fm.cur_states[-1] in (FileMng.States.VAR_TYPE, FileMng.States.ARRAY_DEFINE):
                self.ctx.cur_fm.cur_states.pop()

    def exitDiscrete_subtype_definition(self, ctx):
        if self.ctx.cur_spec is not None:
            if self.ctx.cur_fm.cur_states[-1] == FileMng.States.ARRAY_DEFINE and self.ctx.cur_type:
                dsi = ctx.discrete_subtype_indication()
                if dsi:
                    a_index = AdaArrayIndex(self.ctx.cur_type, cpu.get_texts(dsi), None)
                    a_index.solve_based()
                    a_index.solve_constraint()
                    self.ctx.cur_type.add_index(a_index)
                else:
                    a_index = AdaArrayIndex(self.ctx.cur_type, None, self.ctx.cur_const)
                    a_index.solve_based()
                    a_index.solve_constraint()
                    self.ctx.cur_type.add_index(a_index)

    def exitSigned_integer_type_definition(self, ctx):
        if self.ctx.cur_spec is not None:
            self.ctx.cur_type = AdaIntType(self.ctx.cur_type,
                                                     self.ctx.cur_spec.package,
                                                     self.ctx,
                                                     )
            self.ctx.cur_type.first, solved1 = cpu.solve_expr(self.ctx,
                                                               cpu.get_texts(ctx.simple_expression(0)))
            self.ctx.cur_type.last, solved2 = cpu.solve_expr(self.ctx,
                                                               cpu.get_texts(ctx.simple_expression(1)))
            if solved1 and solved2:
                self.ctx.cur_type.is_based = True

    def exitModular_type_definition(self, ctx):
        if self.ctx.cur_spec is not None:
            self.ctx.cur_type = AdaIntType(self.ctx.cur_type,
                                                     self.ctx.cur_spec.package,
                                                     self.ctx,
                                                    )
            self.ctx.cur_type.mod, solved = cpu.solve_expr(self.ctx,
                                                               cpu.get_texts(ctx.expression()))
            self.ctx.cur_type.first = '0'
            if solved:
                self.ctx.cur_type.last = str(eval("-".join([self.ctx.cur_type.mod, '1'])))

    def enterFloating_point_definition(self, ctx):
        if self.ctx.cur_spec is not None:
            self.ctx.cur_type = AdaRealType(self.ctx.cur_type,
                                                     self.ctx.cur_spec.package,
                                                     self.ctx)

    def exitFloating_point_definition(self, ctx):
        if self.ctx.cur_spec is not None:
            self.ctx.cur_type.digits = cpu.solve_expr(self.ctx,
                                                               cpu.get_texts(ctx.expression()))[0]

    def enterOrdinary_fixed_point_definition(self, ctx):
        if self.ctx.cur_spec is not None:
            self.ctx.cur_type = AdaRealType(self.ctx.cur_type,
                                                      self.ctx.cur_spec.package,
                                                      self.ctx)

    def exitOrdinary_fixed_point_definition(self, ctx):
        if self.ctx.cur_spec is not None:
            self.ctx.cur_type.delta = cpu.solve_expr(self.ctx,
                                                                cpu.get_texts(ctx.expression()))[0]

    def enterDecimal_fixed_point_definition(self, ctx):
        if self.ctx.cur_spec is not None:
            self.ctx.cur_type = AdaRealType(self.ctx.cur_type,
                                                      self.ctx.cur_spec.package,
                                                      self.ctx)

    def exitDecimal_fixed_point_definition(self, ctx):
        if self.ctx.cur_spec is not None:
            self.ctx.cur_type.delta = cpu.solve_expr(self.ctx,
                                                                cpu.get_texts(ctx.expression(0)))[0]
            self.ctx.cur_type.digits = cpu.solve_expr(self.ctx,
                                                                cpu.get_texts(ctx.expression(1)))[0]

    def exitReal_range_specification(self, ctx):
        if self.ctx.cur_spec is not None:
            self.ctx.cur_type.first = cpu.solve_expr(self.ctx,
                                                               cpu.get_texts(ctx.simple_expression(0)))[0]

            self.ctx.cur_type.last = cpu.solve_expr(self.ctx,
                                                            cpu.get_texts(ctx.simple_expression(1)))[0]

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
            if obj_val:
                self.ctx.cur_var.solve_value(cpu.get_texts(obj_val))
            self.ctx.cur_spec.add_var(self.ctx.cur_var)
            for ident in self.ctx.cur_idents:
                self.ctx.cur_spec.add_var(self.ctx.cur_var.copy(ident))
            self.ctx.cur_var = None
            self.ctx.cur_fm.cur_states.pop()

    #def exitMod_clause(self, ctx):
    #    if self.ctx.cur_spec is not None:
    #        self.cur_mod, dummy = cpu.solve_expr(self.ctx, cpu.get_texts(ctx.expression()))