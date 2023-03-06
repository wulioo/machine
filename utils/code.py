from enum import Enum


class StatusCode(Enum):
    """状态码枚举类"""
    SUCCESS = (0, '成功')
    ERROR = (-1, '错误')

    @property
    def code(self):
        """获取状态码"""
        return self.value[0]

    @property
    def msg(self):
        """获取状态码信息"""
        return self.value[1]


class PlatformCode(Enum):
    """状态码枚举类"""
    FUTURES = 1
    EQUITY = 2


class TableTypeCode(Enum):
    SINGLE = 'single_table'
    MULTI = 'multi_table'


class TableName(Enum):
    FAC_TABLE = 'fac_table'
    FAC_CATEGORY = 'category'


class FileNumber(Enum):
    ONEFILE = 1
    TWOFILE = 2
