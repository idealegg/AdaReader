# Generated from ADA95.g4 by ANTLR 4.7.2
from antlr4 import *
from run.ADA95Listener import ADA95Listener
from run.ADA95Parser import ADA95Parser
from common.ada_spec import AdaSpec
from common.ada_record_type import AdaRecordType
from common.ada_record_field import AdaRecordField
from common.ada_enum_type import AdaEnumType
from common.ada_str_type import AdaStrType
from common.ada_int_type import AdaIntType
from common.ada_real_type import AdaRealType
from common.ada_array_type import AdaArrayType
from common.ada_derived_type import AdaDerivedType
from common.ada_subtype import AdaSubtype
from common.ada_type import AdaType
from common.ada_var import AdaVar
import common.parse_util as cpu
import pprint
import re


# This class defines a complete listener for a parse tree produced by ADA95Parser.
class ADA95Listener3(ADA95Listener):
    def __init__(self):
        self.unsolved = set()

    # Enter a parse tree produced by ADA95Parser#compilation_unit_lib.
    def enterCompilation_unit_lib(self, ctx:ADA95Parser.Compilation_unit_libContext):
        ctx.parser.ada_ctx.cur_spec = AdaSpec(
            ctx.parser.getTokenStream().tokenSource.inputStream.fileName,
            ctx.parser.ada_ctx)

    # Exit a parse tree produced by ADA95Parser#compilation_unit_lib.
    def exitCompilation_unit_lib(self, ctx:ADA95Parser.Compilation_unit_libContext):
        ctx.parser.ada_ctx.cur_spec = None

    # Exit a parse tree produced by ADA95Parser#with_clause.
    def exitWith_clause(self, ctx:ADA95Parser.With_clauseContext):
        ctx.parser.ada_ctx.cur_spec.add_with(cpu.get_texts(ctx.library_unit_name()))

    def exitUse_package_clause(self, ctx):
        ctx.parser.ada_ctx.cur_spec.add_use(cpu.get_texts(ctx.package_name()))

    def exitUse_type_clause(self, ctx):
        ctx.parser.ada_ctx.cur_spec.add_use_types(cpu.get_texts(ctx.subtype_mark()))

    def enterPackage_specification(self, ctx):
        ctx.parser.ada_ctx.cur_spec.package = cpu.get_texts(ctx.defining_program_unit_name())

    # Enter a parse tree produced by ADA95Parser#type_definition_clause.
    def enterType_definition_clause(self, ctx: ADA95Parser.Type_definition_clauseContext):
        ctx.parser.ada_ctx.cur_type = cpu.get_texts(ctx.defining_identifier())
        ctx.parser.ada_ctx.cur_discrim = []

    # Exit a parse tree produced by ADA95Parser#type_definition_clause.
    def exitType_definition_clause(self, ctx: ADA95Parser.Type_definition_clauseContext):
        if isinstance(ctx.parser.ada_ctx.cur_type, str):
            print('ignore type: %s' % ctx.parser.ada_ctx.cur_type)
        else:
            #ctx.parser.ada_ctx.cur_type.print()
            ctx.parser.ada_ctx.cur_spec.add_type(ctx.parser.ada_ctx.cur_type)
            #print("exitType_definition_clause:")
            #pprint.pprint(ctx.parser.ada_ctx.cur_spec.types)
        ctx.parser.ada_ctx.cur_type = None
        ctx.parser.ada_ctx.cur_discrim = None

    def exitDiscriminant_specification(self, ctx):
        a_memb = AdaRecordField(ctx.parser.ada_ctx.cur_idents.pop(), ctx.parser.ada_ctx.cur_type, ctx.parser.ada_ctx)
        a_memb.solve_type(cpu.get_texts(ctx.subtype_mark()))
        def_val = ctx.default_expression()
        if def_val is not None:
            a_memb.solve_default(cpu.get_texts(def_val))
        ctx.parser.ada_ctx.cur_discrim.append(a_memb)
        for ident in ctx.parser.ada_ctx.cur_idents:
            ctx.parser.ada_ctx.cur_discrim.append(a_memb.copy(ident))

    def enterEnumeration_type_definition(self, ctx):
        ctx.parser.ada_ctx.cur_type = AdaEnumType(
            ctx.parser.ada_ctx.cur_type,
            ctx.parser.ada_ctx.cur_spec.package,
            ctx.parser.ada_ctx)
        if ctx.parser.ada_ctx.cur_discrim:
            ctx.parser.ada_ctx.cur_type.add_discrim(ctx.parser.ada_ctx.cur_discrim)
        enums = cpu.get_texts(ctx.enumeration_literal_specification())
        ctx.parser.ada_ctx.cur_type.add_enum(enums)
        ctx.parser.ada_ctx.cur_field = None

    def enterDerived_type_definition(self, ctx):
        ctx.parser.ada_ctx.cur_type = AdaDerivedType(
            ctx.parser.ada_ctx.cur_type,
            ctx.parser.ada_ctx.cur_spec.package,
            ctx.parser.ada_ctx)

    def enterSubtype_declaration(self, ctx):
        ctx.parser.ada_ctx.cur_type = AdaSubtype(
            cpu.get_texts(ctx.defining_identifier()),
            ctx.parser.ada_ctx.cur_spec.package,
            ctx.parser.ada_ctx)
    def exitSubtype_declaration(self, ctx):
        if isinstance(ctx.parser.ada_ctx.cur_type, str):
            print('ignore type: %s' % ctx.parser.ada_ctx.cur_type)
        else:
            # ctx.parser.ada_ctx.cur_type.print()
            ctx.parser.ada_ctx.cur_spec.add_type(ctx.parser.ada_ctx.cur_type)
            # print("exitType_definition_clause:")
            # pprint.pprint(ctx.parser.ada_ctx.cur_spec.types)
        ctx.parser.ada_ctx.cur_type = None
        ctx.parser.ada_ctx.cur_discrim = None

    def exitSubtype_indication(self, ctx):
        if ctx.parser.ada_ctx.cur_type and not isinstance(ctx.parser.ada_ctx.cur_type, str):
            ctx.parser.ada_ctx.cur_type.based = cpu.get_texts(ctx.subtype_mark())
            ctx.parser.ada_ctx.cur_type.constraint = ctx.parser.ada_ctx.cur_const
            ctx.parser.ada_ctx.cur_const = None
            ctx.parser.ada_ctx.cur_range = None

    def enterRange_constraint(self, ctx):
        if not ctx.parser.ada_ctx.cur_const:
            ctx.parser.ada_ctx.cur_const = {'type': 'range'}

    def enterDigits_constraint(self, ctx):
        if not ctx.parser.ada_ctx.cur_const:
            ctx.parser.ada_ctx.cur_const = {'type': 'digits'}

    def enterDelta_constraint(self, ctx):
        if not ctx.parser.ada_ctx.cur_const:
            ctx.parser.ada_ctx.cur_const = {'type': 'delta'}

    def enterIndex_constraint(self, ctx):
        if not ctx.parser.ada_ctx.cur_const:
            ctx.parser.ada_ctx.cur_const = {'type': 'index'}

    def enterDiscriminant_constraint(self, ctx):
        if not ctx.parser.ada_ctx.cur_const:
            ctx.parser.ada_ctx.cur_const = {'type': 'discrim', 'choice': {}}

    def exitDigits_constraint(self, ctx):
        ctx.parser.ada_ctx.cur_const.update({
            'digits': cpu.solve_expr(ctx.parser.ada_ctx, cpu.get_texts(ctx.expression()))[0],
            'range': ctx.parser.ada_ctx.cur_range})

    def exitDelta_constraint(self, ctx):
        ctx.parser.ada_ctx.cur_const.update({
            'delta': cpu.solve_expr(ctx.parser.ada_ctx, cpu.get_texts(ctx.expression()))[0],
            'range': ctx.parser.ada_ctx.cur_range})

    def exitIndex_constraint(self, ctx):
        ctx.parser.ada_ctx.cur_const.update({
            'discrete': cpu.get_texts(ctx.discrete_range())})

    def exitDiscriminant_association(self, ctx):
        for n in cpu.get_texts(ctx.discriminant_selector_name()):
            ctx.parser.ada_ctx.cur_const['choice'][n] = cpu.solve_expr(
                ctx.parser.ada_ctx,
                cpu.get_texts(ctx.expression()))[0]

    def exitRange_state(self, ctx):
        ctx.parser.ada_ctx.cur_range = {}
        rar = ctx.range_attribute_reference()
        if rar:
            rar = cpu.get_texts(rar)
            ctx.parser.ada_ctx.cur_range = {'type': 'attr', 'base': rar[:rar.find("'")]}
        else:
            ctx.parser.ada_ctx.cur_range = {'type': 'range',
                                            'first': cpu.solve_expr(ctx.parser.ada_ctx, cpu.get_texts(ctx.simple_expression(0)))[0],
                                            'last': cpu.solve_expr(ctx.parser.ada_ctx, cpu.get_texts(ctx.simple_expression(1)))[0]
                                            }
        if ctx.parser.ada_ctx.cur_const and ctx.parser.ada_ctx.cur_const['type'] == 'range':
            ctx.parser.ada_ctx.cur_const.update({'range': ctx.parser.ada_ctx.cur_range})
        else:
            print("ignore range statement: %s" % ctx.getText())

    def exitEnumeration_type_definition(self, ctx):
        pass

    def enterRecord_type_definition(self, ctx):
        ctx.parser.ada_ctx.cur_type = AdaRecordType(
            ctx.parser.ada_ctx.cur_type,
            ctx.parser.ada_ctx.cur_spec.package,
            ctx.parser.ada_ctx)
        if ctx.parser.ada_ctx.cur_discrim:
            ctx.parser.ada_ctx.cur_type.add_discrim(ctx.parser.ada_ctx.cur_discrim)
        ctx.parser.ada_ctx.cur_field = []

    def exitRecord_type_definition(self, ctx):
        pass

    def exitDefining_identifier_list(self, ctx):
        ctx.parser.ada_ctx.cur_idents = cpu.get_texts(ctx.defining_identifier())

    def exitComponent_declaration(self, ctx):
        ctx.parser.ada_ctx.cur_field = []
        a_memb = AdaRecordField(ctx.parser.ada_ctx.cur_idents.pop(), ctx.parser.ada_ctx.cur_type.name, ctx.parser.ada_ctx)
        a_memb.solve_type(cpu.get_texts(ctx.component_definition()))
        def_val = ctx.default_expression()
        if def_val is not None:
            a_memb.solve_default(cpu.get_texts(def_val))
        #print("cur_field: %s" % ctx.parser.ada_ctx.cur_field)
        #ctx.parser.ada_ctx.cur_field.print()
        #a_memb.print()
        ctx.parser.ada_ctx.cur_field.append(a_memb)
        for ident in ctx.parser.ada_ctx.cur_idents:
            ctx.parser.ada_ctx.cur_field.append(a_memb.copy(ident))
        ctx.parser.ada_ctx.cur_type.add_fields(ctx.parser.ada_ctx.cur_field)
        #ctx.parser.ada_ctx.cur_type.print()
        ctx.parser.ada_ctx.cur_field = None

    def enterRecord_representation_clause(self, ctx):
        ctx.parser.ada_ctx.cur_type = None
        ctx.parser.ada_ctx.cur_field = None

    def enterFirst_subtype_local_name(self, ctx):
        ctx.parser.ada_ctx.cur_type = cpu.find_name(
            cpu.get_texts(ctx.local_name()),
            ctx.parser.ada_ctx,
            'type')[0]

    def exitRecord_representation_clause(self, ctx):
        if not isinstance(ctx.parser.ada_ctx.cur_type, str):
            mod_cls = ctx.mod_clause()
            if mod_cls is not None:
                mod_cls = cpu.get_texts(mod_cls)
            else:
                mod_cls = None
            ctx.parser.ada_ctx.cur_spec.types[ctx.parser.ada_ctx.cur_type.package][ctx.parser.ada_ctx.cur_type.name].mod_clause = mod_cls
            #ctx.parser.ada_ctx.types[ctx.parser.ada_ctx.cur_type.package][ctx.parser.ada_ctx.cur_type.name].mod_clause = mod_cls

    def exitComponent_clause(self, ctx):
        a_memb = {}
        a_memb['name'] = cpu.get_texts(ctx.component_local_name())
        a_memb['pos'] = cpu.get_texts(ctx.position())
        a_memb['start'] = cpu.get_texts(ctx.first_bit())
        a_memb['end'] = cpu.get_texts(ctx.last_bit())
        #ctx.parser.ada_ctx.cur_type.print()
        #pprint.pprint(ctx.parser.ada_ctx.cur_spec.types)
        ctx.parser.ada_ctx.cur_spec.types[ctx.parser.ada_ctx.cur_type.package][
            ctx.parser.ada_ctx.cur_type.name].add_pos(a_memb)
        #ctx.parser.ada_ctx.types[ctx.parser.ada_ctx.cur_type.package][ctx.parser.ada_ctx.cur_type.name].add_pos(a_memb)

    def exitArray_component_association(self, ctx):
        if ctx.parser.ada_ctx.cur_type and (not isinstance(ctx.parser.ada_ctx.cur_type, str)):
            if ctx.parser.ada_ctx.cur_type.ttype == AdaType.ENUM_TYPE:
                ctx.parser.ada_ctx.cur_type.add_val(
                    cpu.get_texts(ctx.discrete_choice_list()),
                    cpu.get_texts(ctx.expression())
                )

    def exitAttribute_definition_clause(self, ctx):
        ctx.parser.ada_ctx.cur_type = cpu.find_name(
            cpu.get_texts(ctx.local_name()),
            ctx.parser.ada_ctx,
            'type')[0]
        if not isinstance(ctx.parser.ada_ctx.cur_type, str):
            attr = cpu.get_texts(ctx.attribute_designator())
            if attr.lower() == 'size':
                ctx.parser.ada_ctx.cur_spec.types[ctx.parser.ada_ctx.cur_type.package][
                    ctx.parser.ada_ctx.cur_type.name].solve_size(cpu.get_texts(ctx.expression()))
                #ctx.parser.ada_ctx.types[ctx.parser.ada_ctx.cur_type.package][ctx.parser.ada_ctx.cur_type.name].size = ctx.parser.ada_ctx.cur_spec.types[ctx.parser.ada_ctx.cur_type.package][
                #    ctx.parser.ada_ctx.cur_type.name].size

    def exitNumber_declaration(self, ctx):
        av = AdaVar(ctx.parser.ada_ctx.cur_idents.pop(),
                    ctx.parser.ada_ctx.cur_spec.package,
                    ctx.parser.ada_ctx)
        av.solve_value(cpu.get_texts(ctx.expression()))
        av.const = True
        ctx.parser.ada_ctx.cur_spec.add_var(av)
        for ident in ctx.parser.ada_ctx.cur_idents:
            ctx.parser.ada_ctx.cur_spec.add_var(av.copy(ident))

    def enterUnconstrained_array_definition(self, ctx):
        ctx.parser.ada_ctx.cur_type = AdaArrayType(ctx.parser.ada_ctx.cur_type,
                                                   ctx.parser.ada_ctx.cur_spec.package,
                                                   ctx.parser.ada_ctx
                                                   )

    def exitUnconstrained_array_definition(self, ctx):
        ctx.parser.ada_ctx.cur_type.elem = cpu.solve_type(ctx.parser.ada_ctx,
                                                          cpu.get_texts(ctx.component_definition))[0]

    def exitIndex_subtype_definition(self, ctx):
        if not ctx.parser.ada_ctx.cur_var and ctx.parser.ada_ctx.cur_type.ttype == AdaType.ARRAY_TYPE:
            ctx.parser.ada_ctx.cur_type.dim.append({'type': 'unconst',
                                                    'base': cpu.solve_type(ctx.parser.ada_ctx,
                                                                           cpu.get_texts(ctx.subtype_mark()))[0]
                                                    })

    def enterConstrained_array_definition(self, ctx):
        ctx.parser.ada_ctx.cur_type = AdaArrayType(ctx.parser.ada_ctx.cur_type,
                                                   ctx.parser.ada_ctx.cur_spec.package,
                                                   ctx.parser.ada_ctx
                                                   )

    def exitConstrained_array_definition(self, ctx):
        ctx.parser.ada_ctx.cur_type.elem = cpu.solve_type(ctx.parser.ada_ctx,
                                                          cpu.get_texts(ctx.component_definition))[0]

    def exitDiscrete_subtype_definition(self, ctx):
        dsi = ctx.discrete_subtype_indication()
        if dsi and not ctx.parser.ada_ctx.cur_var and ctx.parser.ada_ctx.cur_type.ttype == AdaType.ARRAY_TYPE:
            ctx.parser.ada_ctx.cur_type.dim.append({'type': 'const',
                                                    'base': cpu.solve_type(ctx.parser.ada_ctx,
                                                                           cpu.get_texts(dsi))[0]
                                                    })
        else:
            ctx.parser.ada_ctx.cur_type.dim.append({'type': 'range',
                                                    'range': ctx.parser.ada_ctx.cur_range
                                                    })
    def exitSigned_integer_type_definition(self, ctx):
        ctx.parser.ada_ctx.cur_type = AdaIntType(ctx.parser.ada_ctx.cur_type,
                                                 ctx.parser.ada_ctx.cur_spec.package,
                                                 ctx.parser.ada_ctx)
        ctx.parser.ada_ctx.cur_type.first = cpu.solve_expr(ctx.parser.ada_ctx,
                                                           cpu.get_texts(ctx.simple_expression(0)))[0]
        ctx.parser.ada_ctx.cur_type.last = cpu.solve_expr(ctx.parser.ada_ctx,
                                                           cpu.get_texts(ctx.simple_expression(1)))[0]

    def exitModular_type_definition(self, ctx):
        ctx.parser.ada_ctx.cur_type = AdaIntType(ctx.parser.ada_ctx.cur_type,
                                                 ctx.parser.ada_ctx.cur_spec.package,
                                                 ctx.parser.ada_ctx)
        ctx.parser.ada_ctx.cur_type.mod, solved = cpu.solve_expr(ctx.parser.ada_ctx,
                                                           cpu.get_texts(ctx.expression()))
        ctx.parser.ada_ctx.cur_type.first = '0'
        if solved:
            ctx.parser.ada_ctx.cur_type.last = str(eval("-".join([ctx.parser.ada_ctx.cur_type.mod, '1'])))

    def enterFloating_point_definition(self, ctx):
        ctx.parser.ada_ctx.cur_type = AdaRealType(ctx.parser.ada_ctx.cur_type,
                                                 ctx.parser.ada_ctx.cur_spec.package,
                                                 ctx.parser.ada_ctx)

    def exitFloating_point_definition(self, ctx):
        ctx.parser.ada_ctx.cur_type.digits = cpu.solve_expr(ctx.parser.ada_ctx,
                                                           cpu.get_texts(ctx.expression()))[0]

    def enterOrdinary_fixed_point_definition(self, ctx):
        ctx.parser.ada_ctx.cur_type = AdaRealType(ctx.parser.ada_ctx.cur_type,
                                                  ctx.parser.ada_ctx.cur_spec.package,
                                                  ctx.parser.ada_ctx)

    def exitOrdinary_fixed_point_definition(self, ctx):
        ctx.parser.ada_ctx.cur_type.delta = cpu.solve_expr(ctx.parser.ada_ctx,
                                                            cpu.get_texts(ctx.expression()))[0]

    def enterDecimal_fixed_point_definition(self, ctx):
        ctx.parser.ada_ctx.cur_type = AdaRealType(ctx.parser.ada_ctx.cur_type,
                                                  ctx.parser.ada_ctx.cur_spec.package,
                                                  ctx.parser.ada_ctx)

    def exitDecimal_fixed_point_definition(self, ctx):
        ctx.parser.ada_ctx.cur_type.delta = cpu.solve_expr(ctx.parser.ada_ctx,
                                                            cpu.get_texts(ctx.expression(0)))[0]
        ctx.parser.ada_ctx.cur_type.digits = cpu.solve_expr(ctx.parser.ada_ctx,
                                                            cpu.get_texts(ctx.expression(1)))[0]

    def exitReal_range_specification(self, ctx):
        ctx.parser.ada_ctx.cur_type.first = cpu.solve_expr(ctx.parser.ada_ctx,
                                                           cpu.get_texts(ctx.simple_expression(0)))[0]

        ctx.parser.ada_ctx.cur_type.last = cpu.solve_expr(ctx.parser.ada_ctx,
                                                        cpu.get_texts(ctx.simple_expression(1)))[0]