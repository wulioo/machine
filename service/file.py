import pandas as pd

from utils.exception import CommonException


class File:
    def __init__(self, file_obj):
        self.__file = file_obj
        self.name = self.__file.name
        self.__check_file_empty()
        self.__check_file_type()
        self.__check_file_size()
        self.__pd_read_file()
        # self.__check_file_column()
        self.__init()

    def __check_file_type(self):
        self.__type = self.__file.name.split('.').pop()

        if self.__type not in ['csv', 'xlsx']:
            raise CommonException(400, f'{self.__file.name},文件类型不符合')

    def __check_file_size(self):
        if self.__file.size > 524288000:
            raise CommonException(400, f"{self.__file.name}文件太大,不能超过500MB")

    def __check_file_empty(self):
        if not self.__file:
            raise CommonException(400, '缺少文件对象，请上传文件')

    def __pd_read_file(self):

        if self.__type == "csv":
            self.df = pd.read_csv(self.__file.file)
        elif self.__type == "xlsx":
            self.df = pd.read_excel(self.__file.file)

    def __check_file_column(self):
        if 'type_name_ab' not in self.df:
            raise CommonException(400, f'文件缺少：type_name_ab')

        if 'trading_date' not in self.df:
            raise CommonException(400, f'文件缺少：trading_date')

    def __init(self):
        self.df.sort_values('trading_date', inplace=True)
        self.df['trading_date'] = pd.to_datetime(self.df['trading_date']).dt.date
