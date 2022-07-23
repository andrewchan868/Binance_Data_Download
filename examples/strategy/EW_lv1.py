import numpy as np
import numba as nb
from numba.typed import Dict, List
from numba import types
from numba.experimental import jitclass
from quantcycle.app.signal_generator.base_strategy import defaultjitclass, BaseStrategy
from quantcycle.app.pms_manager.portfolio_manager import PorfolioManager
from examples.util.indicator import MA
try:
    pms_type = PorfolioManager.class_type.instance_type
except:
    pms_type = "PMS_type"


@defaultjitclass()
class EW_strategy(BaseStrategy):

    def init(self):
        self.p_entry_therhold,self.p_exit_therhold = self.strategy_param[0],self.strategy_param[1]
        self.spot2future_ticker = {"QC_ETHUSDT":"QC_ETHUSDT_prep","QC_BTCUSDT":"QC_BTCUSDT_prep",\
                                    "QC_ADAUSDT":"QC_ADAUSDT_prep","QC_BNBUSDT":"QC_BNBUSDT_prep",\
                                    "QC_DOTUSDT":"QC_DOTUSDT_prep","QC_XRPUSDT":"QC_XRPUSDT_prep",\
                                    "QC_DOGEUSDT":"QC_DOGEUSDT_prep","QC_LTCUSDT":"QC_LTCUSDT_prep"}
        self.signal = {k:0 for k,v in self.spot2future_ticker.items()}
        symbol_batch = self.metadata["main"]["symbols"]
        self.ma_dict = {}
        self.var_dict = {}
        self.on_live_pair = 0
        for k,v in self.spot2future_ticker.items():
            if k in symbol_batch:
                self.on_live_pair += 1
                self.ma_dict[k] = MA(1000,1)
                self.var_dict[k] = MA(500,1)

    def on_data(self, data_dict: dict, time_dict: dict, ref_data_dict: dict, ref_time_dict: dict):
        symbol_batch = list(self.metadata["main"]["symbols"])
        remark = {}
        z_score_dict = {}
        basis_dict = {}
        cur_hour = time_dict["main"][-1][6]
        for k,v in self.spot2future_ticker.items():
            if k not in symbol_batch:
                continue
            spot_id = list(symbol_batch).index(k)
            future_id = list(symbol_batch).index(v)
            basis = data_dict["main"][:,future_id,0] / data_dict["main"][:,spot_id,0]
            if np.isnan(basis).any():
                continue
            self.ma_dict[k].on_data(basis)
            if not self.ma_dict[k].ready:
                continue
            self.var_dict[k].on_data((basis-self.ma_dict[k].value)**2)
            if not self.var_dict[k].ready:
                continue
            sd = (self.var_dict[k].value[-1])**0.5
            #z_score_dict[k] = (basis[-1] - self.ma_dict[k].value) / sd
            z_score_dict[k] = (basis[-1] - 1) / sd
            basis_dict[k] = basis[-1]
        

        target = np.zeros(len(symbol_batch)) * np.nan
        amount_on_each_pair = self.portfolio_manager.pv / self.on_live_pair
        for spot_ticker,z_score in z_score_dict.items():
            future_ticker = self.spot2future_ticker[spot_ticker]
            spot_id = list(symbol_batch).index(spot_ticker)
            future_id = list(symbol_batch).index(future_ticker)
            ref_data_id = self.metadata["funding_rate"]['symbols'].index(f"{future_ticker}_funding_rate")
            funding_rate = ref_data_dict['funding_rate'][-1][ref_data_id,0]
            is_funding_too_negative = cur_hour in [7,15,23] and funding_rate > 0
            if cur_hour in [7,15,23]:
                remark[spot_ticker+"|basis"] = basis_dict[spot_ticker]
                remark[spot_ticker+"|z_score"] = z_score_dict[spot_ticker]
                remark[spot_ticker+"|funding_rate"] = funding_rate
            if self.signal[spot_ticker] == 0 and z_score > self.p_entry_therhold :
                target[future_id] = -1*amount_on_each_pair/2
                target[spot_id] = amount_on_each_pair/2
                self.signal[spot_ticker] = 1
            #if self.signal[spot_ticker] == 0 and z_score < -2 :
            #    target[future_id] = amount_on_each_pair/2
            #    target[spot_id] = -1*amount_on_each_pair/2
            #    self.signal[spot_ticker] = -1
            elif self.signal[spot_ticker] != 0:
                if self.signal[spot_ticker] == 1 and (z_score < self.p_exit_therhold):
                    target[future_id] = 0
                    target[spot_id] = 0
                    self.signal[spot_ticker] = 0
                elif self.signal[spot_ticker] == -1 and (z_score > -1):
                    target[future_id] = 0
                    target[spot_id] = 0
                    self.signal[spot_ticker] = 0
        self.save_signal_remark(remark)
        return self.return_reserve_target_base_ccy(target).reshape(1, -1)
