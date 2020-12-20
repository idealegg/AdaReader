from common.ada_var import AdaVar
from common.ada_type import AdaType
from common.ada_int_type import AdaIntType
from common.ada_real_type import AdaRealType
from common.ada_array_type import AdaArrayType
from common.parse_util import ADA_SYSTEM_DEFINED
from common.ada_enum_type import AdaEnumType

class PreDefined:
    def __init__(self, ctx):
        av = AdaVar('OCTET', 'STANDARD_TYPES', ctx)
        av.solve_value('8')

        ait = AdaIntType('INTEGER', ADA_SYSTEM_DEFINED, ctx)
        ait.first = str(-0x7fffffff - 1)
        ait.last = str(0x7fffffff)
        ait.is_based = True

        art1 = AdaRealType('SHORT_FLOAT', ADA_SYSTEM_DEFINED, ctx)
        art2 = AdaRealType('LONG_FLOAT', ADA_SYSTEM_DEFINED, ctx)
        ast = AdaArrayType('STRING', ADA_SYSTEM_DEFINED, ctx)
        art1.is_based = True
        art2.is_based = True
        ast.is_based = True

        self.vars = {}
        self.types = {'ADA_SYSTEM_DEFINED':
                          {'INTEGER': ait,
                           'SHORT_FLOAT': art1,
                           'LONG_FLOAT': art2,
                           'STRING': ast
                           }
                      }