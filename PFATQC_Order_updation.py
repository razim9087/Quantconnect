# region imports
from AlgorithmImports import *
# endregion

from datetime import datetime

class PFATQC_Order_ticket(QCAlgorithm):

    def initialize(self):
        self.set_start_date(2007,1,1)
        self.set_cash(100000)
        self.stock=self.add_equity("C",Resolution.DAILY)
        self.stock.set_data_normalization_mode(DataNormalizationMode.RAW)
        self.sell_ticket=None
        self.first_day_close=None
        self.invest=True
        self.loss_limit=0.5

    def on_data(self,data):
        if not self.portfolio.invested and self.invest:
            self.initial_order=self.market_order(self.stock.symbol,10)
            self.first_day_close=self.securities[self.stock.symbol].close
            self.invest=False

        if self.sell_ticket is None:
            self.sell_ticket=self.stop_market_order(self.stock.symbol,-10,
                             self.securities[self.stock.symbol].close*self.loss_limit)
            
    def on_end_of_day(self):
        if self.sell_ticket is None:
            return
        else:
            self.log(str(self.securities[self.stock.symbol].close))

        if ((self.securities[self.stock.symbol].open-self.securities[self.stock.symbol].close)/self.securities[self.stock.symbol].open)>0.05:

            update_settings=UpdateOrderFields()
            update_settings.stop_price=self.first_day_close*0.75

            response=self.sell_ticket.update(update_settings)
            if response.is_success:
                self.debug("Order was updated")


    def on_order_event(self,order_event):

        if order_event.fill_quantity==0:
            return

        fetched=self.transactions.get_order_by_id(order_event.order_id)
        self.log(f"{fetched.type} filled for Quantity {order_event.fill_quantity}")

    

