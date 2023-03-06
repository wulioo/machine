from service.table_name import TableNames, Category, Table
from service.table_type import TableType, FactorSingleTable, FactorMultiTable, SignalSingleTable, SignalMultiTable
from utils.code import TableName


#


class TableTypeFactory:
    _Table = {
        'fac_table': FactorSingleTable,
        'fac_category': FactorMultiTable,
        "sga_table": SignalSingleTable,
        "sga_category": SignalMultiTable
    }

    @classmethod
    def make_table(cls, table, factor):
        return cls._Table.get(table)(factor)
