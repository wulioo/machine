from abc import ABCMeta, abstractmethod

from service.earnings import FutureEarnings, CloseEarnings, OpenEarnings, FileEarnings


class Earnings(metaclass=ABCMeta):
    @abstractmethod
    def make_earnings(self, stime, etime, cal_ear):
        pass

    # @classmethod
    def make_cal_ear(self, price):
        if price == 'close_price':
            return CloseEarnings()
        elif price == 'open_price':
            return OpenEarnings()
        elif price == 'file_price':
            return FileEarnings()
        elif price == "volat_price":
            close_ear = CloseEarnings()
            close_ear.sharpe = True
            return close_ear


class FvFactoryEarnings(Earnings):
    # @classmethod
    def make_earnings(self, stime, etime, price):
        cal_ear = self.make_cal_ear(price)
        return FutureEarnings(stime, etime, cal_ear)
