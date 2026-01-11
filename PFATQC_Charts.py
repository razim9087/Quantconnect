# region imports
from AlgorithmImports import *
# endregion

class PFATQC_BuyandHold(QCAlgorithm):

    def initialize(self):
        self.set_start_date(2020,1,1)
        self.set_end_date(2021,1,1)
        self.set_cash(10000)
        self.add_equity("XOM",Resolution.DAILY)

        #Create new chart
        price_data=Chart("Custom Chart")
        price_data.add_series(Series("Price",SeriesType.LINE,0))
        price_data.add_series(Series("Price Open Monthly",SeriesType.SCATTER,0))
        self.add_chart(price_data)

    def on_data(self,data):
        if not self.portfolio.invested:
            self.set_holdings("XOM",1)
            
        #Plot drectly on Strategy Equity chart
        #self.plot("XOM Price",self.securities["XOM"].close)

        self.plot(chart="Custom Chart",series="Price",value=self.securities["XOM"].open)

        if self.time.day==1:
            self.plot(chart="Custom Chart",series="Price Open Monthly",value=self.securities["XOM"].open)
