from common.ada_var import AdaVar
from common.ada_type import AdaType
from common.ada_int_type import AdaIntType
from common.ada_real_type import AdaRealType
from common.ada_array_type import AdaArrayType
from common.parse_util import ADA_SYSTEM_DEFINED
from common.ada_enum_type import AdaEnumType

class PreDefined:
    def __init__(self, ctx):
        self.vars = {}
        self.types = {}

        self.add_type(AdaIntType('INTEGER', ADA_SYSTEM_DEFINED, ctx, True, first=str(-0x7fffffff - 1), last=str(0x7fffffff)))
        self.add_type(AdaRealType('SHORT_FLOAT', ADA_SYSTEM_DEFINED, ctx, True))
        self.add_type(AdaRealType('LONG_FLOAT', ADA_SYSTEM_DEFINED, ctx, True))
        self.add_type(AdaRealType('FLOAT', ADA_SYSTEM_DEFINED, ctx, True))
        self.add_type(AdaArrayType('STRING', ADA_SYSTEM_DEFINED, ctx, True))
        self.add_type(AdaEnumType('BOOLEAN', ADA_SYSTEM_DEFINED, ctx, ['FALSE', 'TRUE']))
        self.add_type(AdaEnumType('CHARACTER', ADA_SYSTEM_DEFINED, ctx))
        self.add_type(AdaIntType('ADDRESS', 'SYSTEM', ctx, True, str(2 ** 32)))


        #self.add_var(AdaVar('OCTET', 'STANDARD_TYPES', ctx, '8'))

    def add_type(self, stype):
        if stype.package not in self.types:
            self.types[stype.package] = {}
        self.types[stype.package][stype.name] = stype

    def add_var(self, svar):
        if svar.package not in self.vars:
            self.vars[svar.package] = {}
        self.vars[svar.package][svar.name] = svar
