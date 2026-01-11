# region imports
from AlgorithmImports import *
# endregion

from datetime import datetime

class PFATQC_market_order(QCAlgorithm):

    def initialize(self):
        self.set_start_date(2010, 1, 1)
        self.set_end_date(2015,1,1)
        self.set_cash(100000)
        self.stock = self.add_equity("AAPL", Resolution.DAILY)
        self.invest = True
        self.liquidated = False

    def on_data(self, data):
        if not self.portfolio.invested and self.invest:
            self.market_order(self.stock.symbol,1000)
            self.invest=False

        # Liquidate on January 1, 2014 (executes on next trading day if holiday)
        if self.time.date() >= datetime(2014, 1, 1).date() and not self.liquidated:
            self.market_order(self.stock.symbol, -1000)
            self.liquidated = True
