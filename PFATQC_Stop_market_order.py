# region imports
from AlgorithmImports import *
# endregion

from datetime import datetime

class PFATQC_stop_market_order(QCAlgorithm):

    def initialize(self):
        self.set_start_date(2019, 1, 1)
        self.set_cash(100000)
        self.stock = self.add_equity("BA", Resolution.DAILY)
        self.invest = True
        self.sell_ticket = None
        self.entry_price = None
 

    def on_data(self, data):
        if not self.portfolio.invested and self.invest:
            self.market_order(self.stock.symbol, 10)
            self.entry_price = self.securities[self.stock.symbol].price
            self.invest = False

        # Place stop market order after entry, using entry price
        if self.portfolio.invested and self.sell_ticket is None and self.entry_price is not None:
            stop_price = float(self.entry_price * 0.6)
            self.sell_ticket = self.stop_market_order(self.stock.symbol, -10, stop_price)

