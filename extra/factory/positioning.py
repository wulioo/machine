from abc import ABCMeta, abstractmethod

from service.section.positionning import  FvSecAnalyPositioning
from service.layered import Layered, LayeredPosition, SingleLayered, ManyLayered
from service.periods import ManyPeriods, SinglePeriods


class Positioning(metaclass=ABCMeta):
    @abstractmethod
    def make_factor(self):
        pass

    @abstractmethod
    def make_single_periods(self):
        pass

    @abstractmethod
    def make_many_periods(self):
        pass

    @abstractmethod
    def make_single_layered(self):
        pass

    @abstractmethod
    def make_many_layered(self):
        pass


class FvPositioning(Positioning):
    def make_factor(self):
        return FvSecAnalyPositioning()

    def make_single_periods(self):
        return SinglePeriods()

    def make_many_periods(self):
        return ManyPeriods()

    def make_single_layered(self):
        return SingleLayered()

    def make_many_layered(self):
        return ManyLayered()


class PositioningFactory:
    @staticmethod
    def make_positioning(positioning, periods) -> FvSecAnalyPositioning:
        if periods == 1:
            periods = positioning.make_single_periods()
            layered = positioning.make_single_layered()
        else:
            periods = positioning.make_many_periods()
            layered = positioning.make_many_layered()

        factor = positioning.make_factor()

        factor.layered = layered
        factor.periods = periods

        return factor
