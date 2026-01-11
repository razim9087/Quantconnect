# region imports
from AlgorithmImports import *
# endregion

class UniverseSelection(QCAlgorithm):

    def initialize(self):
        self.set_start_date(2022, 8, 25)
        self.set_end_date(2022,10,5)
        self.set_cash(100000000)
        self.settings.seed_initial_prices = True
        self.universe_settings.resolution = Resolution.DAILY
        self.add_universe(self.coarse_selection,self.fine_selection) 

    def coarse_selection(self, coarse):
        # Multi-Condition Coarse selection
        self.coarse_filtered_stocks=[x.symbol for x in coarse if x.Price>20 \
                              and x.DollarVolume>10000000 \
                                and x.HasFundamentalData]
        return self.coarse_filtered_stocks

    def fine_selection(self,fine):
        self.fine_filtered_stocks=[sec for sec in fine if sec.ValuationRatios.PERatio < 100]
        sorted_by_ebit = sorted(self.fine_filtered_stocks,key=lambda x:x.FinancialStatements.IncomeStatement.EBIT.TwelveMonths,reverse=True)
        return [x.symbol for x in sorted_by_ebit][:10]

    def on_data(self, data):
        
        self.log(self.time)
        
        for sec in self.securities.values():

            if not data.ContainsKey(sec.symbol):
                return
            else:
                self.log(f"{data[sec.symbol].symbol} opened at:{data[sec.symbol].open}")

        self.log("----------------------")

    def on_securities_changed(self,changes):
        self.log("Change in Universe")
        self.sec_change=True
        for sec in changes.RemovedSecurities:
            self.liquidate(sec)
            self.log(f"SOLD: {sec.symbol} at {sec.Price}")

        for sec in changes.AddedSecurities:       
            self.set_holdings(sec.symbol,0.1)
            self.log(f"Bought: {sec.symbol} at {sec.Price}")
            

