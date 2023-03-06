from abc import ABCMeta, abstractmethod

from service.earnings import FutureEarnings
from service.factor import FactorICIR
from service.varieties import Varieties, VarietiesFactory


class ICIR(metaclass=ABCMeta):
    @abstractmethod
    def make_factor(self):
        pass

    @abstractmethod
    def make_varieties(self, vits_fu):
        pass

    @abstractmethod
    def make_earnings(self, stime, etime, cal_ear):
        pass


class FvICIR(ICIR):
    def make_factor(self):
        return FactorICIR()

    def make_varieties(self, vits_fun):
        return VarietiesFactory.create_varieties(vits_fun)

    def make_earnings(self, stime, etime, cal_ear):
        return FutureEarnings(stime, etime, cal_ear)


class FactorIcIrFactory:
    @staticmethod
    def make_positioning(fvicir, periods):
        factor = fvicir.make_factor()
