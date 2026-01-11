# region imports
from AlgorithmImports import *
# endregion

class PFATQC_Exit(QCAlgorithm):
    def initialize(self):
        self.set_start_date(2010,1,1)
        self.set_end_date(2020,1,1)
        self.set_cash(10000)
        self.apple=self.add_equity("AAPL",Resolution.DAILY)
        self.limit_price=50
        self.invest=True

    def on_data(self,data):
        if not self.portfolio.invested and self.invest:
            self.set_holdings("AAPL",1)

        closing_price=self.portfolio["AAPL"].price

        if closing_price>self.limit_price and self.portfolio.invested:
            self.liquidate("AAPL")
            self.invest=False


