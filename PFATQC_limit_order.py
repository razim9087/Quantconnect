# region imports
from AlgorithmImports import *
# endregion

from datetime import datetime

class PFATQC_limit_order(QCAlgorithm):

    def initialize(self):
        self.set_start_date(2018, 1, 1)
        self.set_cash(100000)
        self.stock = self.add_equity("AAPL", Resolution.DAILY)
        self.invest = True
 

    def on_data(self, data):
        if not self.portfolio.invested and self.invest:
            self.limit_order(self.stock.symbol,10,50)
            self.limit_order(self.stock.symbol,-10,125)
            self.invest=False

