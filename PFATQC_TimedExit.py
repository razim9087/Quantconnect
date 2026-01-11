# region imports
from AlgorithmImports import *
# endregion

class PFATQC_TimedExit(QCAlgorithm):

    def initialize(self):
        self.set_start_date(2020, 1, 1)
        self.set_end_date(2021, 1, 1)
        self.set_cash(10000)
        self.add_equity("KO", Resolution.DAILY)
        self.invest=True
      

    def on_data(self, data):
        if not self.portfolio.invested and self.invest:
            self.set_holdings("KO", 0.5)
            self.invested_time=self.time

        time_passed=(self.time-self.invested_time).days

        if time_passed>100:
            self.liquidate("KO")
            self.invest=False
  