# region imports
from AlgorithmImports import *
# endregion

from datetime import datetime

class PFATQC_brokerage_model(QCAlgorithm):

    def initialize(self):
        self.set_start_date(2020,1,1)
        self.set_end_date(2021,1,1)
        self.set_cash(10000)
        self.stock=self.add_equity("SPY",Resolution.DAILY)
        self.set_brokerage_model(BrokerageName.INTERACTIVE_BROKERS_FIX,AccountType.MARGIN)
        

    def on_data(self,data):
        if not self.portfolio.invested:
            self.set_holdings(self.stock.symbol,3)






"""

class PFATQC_price_comparison(QCAlgorithm):

    def initialize(self):
        self.set_start_date(2018,1,1)
        self.set_end_date(2020,1,1)
        self.set_cash(10000)
        self.vnq=self.add_equity("VNQ",Resolution.DAILY)
        self.vnqi=self.add_equity("VNQI",Resolution.DAILY)
        self.sell_ticket=None
        self.rolling_max=None
        self.invest=True
        self.loss_limit=0.9

    def on_data(self,data):

        # Daily gain

        dg_vnq= (self.vnq.close-self.vnq.open)/self.vnq.open
        dg_vnqi=(self.vnqi.close-self.vnqi.open)/self.vnqi.open

        if dg_vnq>0.02 and dg_vnq>dg_vnqi:
            self.set_holdings(self.vnq.symbol,1,True)
            self.log("VNQ GAIN: {}".format(dg_vnq*100))

        elif dg_vnqi>0.02 and dg_vnqi>dg_vnq:
            self.set_holdings(self.vnqi.symbol,1,True)
            self.log("VNQI GAIN: {}".format(dg_vnqi*100))

        else:

            self.log("No Actions")
            return


class PFATQC_trailing_stop_loss(QCAlgorithm):

    def initialize(self):
        self.set_start_date(2018,1,1)
        self.set_end_date(2019,1,1)
        self.set_cash(100000)
        self.stock=self.add_equity("SPY",Resolution.DAILY)
        self.sell_ticket=None
        self.rolling_max=None
        self.invest=True
        self.loss_limit=0.9

    def on_data(self,data):
        if not self.portfolio.invested and self.invest:
            self.initial_order=self.market_order(self.stock.symbol,1)
            self.rolling_max=self.securities[self.stock.symbol].close
            self.invest=False

        if self.sell_ticket is None:
            
            self.sell_ticket=self.stop_market_order(self.stock.symbol,-1,
                                   self.rolling_max*self.loss_limit,tag="Initial Order")
            
    def on_end_of_day(self):
        if self.sell_ticket is None:
            return
        else:
            if self.securities[self.stock.symbol].close>self.rolling_max:
                self.rolling_max=self.securities[self.stock.symbol].close
                self.log("New Rolling Maximum {}".format(self.rolling_max))
                update_settings=UpdateOrderFields()
                update_settings.stop_price=self.rolling_max*self.loss_limit
                update_settings.tag="Reference Closing Price {}".format(self.rolling_max)
                response=self.sell_ticket.update(update_settings)
                if response.is_success:
                    self.debug("Order was updated")
            else:
                self.log("No changes to sell order")


    def on_order_event(self,order_event):

        if order_event.fill_quantity==0:
            return

        fetched=self.transactions.get_order_by_id(order_event.order_id)
        self.log(f"{fetched.type} filled for Quantity {order_event.fill_quantity}")

"""