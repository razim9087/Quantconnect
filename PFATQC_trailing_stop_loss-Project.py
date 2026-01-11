# region imports
from AlgorithmImports import *
# endregion

from datetime import datetime

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
        self.sold=False

    def on_data(self,data):
        if not self.portfolio.invested and self.invest:
            self.initial_order=self.market_order(self.stock.symbol,1)
            self.rolling_max=self.securities[self.stock.symbol].close

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
                    self.log("Order was updated")
            else:
                if self.portfolio.invested or self.invest:
                    self.log("No changes to sell order")
                else:
                    self.log("Trade concluded")



    def on_order_event(self,order_event):

        if order_event.fill_quantity==0:
            return
        else:
            fetched=self.transactions.get_order_by_id(order_event.order_id)
            self.log(f"{fetched.type} filled for Quantity {order_event.fill_quantity}")
            if fetched.type==self.initial_order.order_type:
                self.invest=False

            

        
        
        


"""

class PFATQC_Conditional_Purchasing(QCAlgorithm):

    def initialize(self):
        self.set_start_date(2019,1,1)
        self.set_end_date(2023,1,1)
        self.set_cash(10000)
        self.stock=self.add_equity("TSLA",Resolution.DAILY)

        self.schedule.on(self.date_rules.month_start(),
                         self.time_rules.at(9,35),
                         self.Buy)

        self.monthly_buy=200
        self.cash_reserve=200

    def Buy(self):
        open_price=self.securities[self.stock.symbol].open
        if open_price==0:
            return

        if self.portfolio.cash < open_price:
            self.debug("Not Enough Cash")
            return
        elif open_price>self.cash_reserve:
            self.cash_reserve=self.cash_reserve+self.monthly_buy
            self.log("Stock too expensive")
            return
        else:
            shares_to_buy=int(self.cash_reserve/open_price)
            self.market_order(self.stock.symbol,shares_to_buy)
            self.cash_reserve=self.monthly_buy
            self.log("Buying {} of {}".format(shares_to_buy,self.stock.symbol))


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

    
"""
