from quantcycle.utils.strategy_pool_generator import strategy_pool_generator
from quantcycle.engine.backtest_engine import BacktestEngine
from datetime import datetime
import json
from quantcycle.app.result_exporter.result_reader import ResultReader
import numpy as np
import os

if __name__ == "__main__":
    pool_setting = {"symbol": {"FUTURES": ['QC_ETHUSDT','QC_BTCUSDT','QC_BNBUSDT','QC_ADAUSDT','QC_DOTUSDT','QC_XRPUSDT','QC_DOGEUSDT','QC_LTCUSDT'],\
                                "FX":['QC_ETHUSDT_prep',"QC_BTCUSDT_prep",'QC_BNBUSDT_prep',"QC_ADAUSDT_prep",'QC_DOTUSDT_prep',"QC_XRPUSDT_prep",'QC_DOGEUSDT_prep',"QC_LTCUSDT_prep"]},
                    "strategy_module": "examples.strategy.EW_lv1",
                    "strategy_name": "EW_strategy",
                    "params": {
                        "entry_therhold": [2.0, 1.0, 0.0],
                        "exit_therhold": [0.0, -1.0, -2.0]
                    }}
    strategy_pool_df = strategy_pool_generator(pool_setting, save=False)
    json_path = "examples/config/EW_stock_hourly_local.json"



    #start backtest
    ts0 = datetime.now()
    backtest_engine = BacktestEngine()
    backtest_engine.load_config(json.load(open(json_path)), strategy_pool_df)
    ts = datetime.now()
    backtest_engine.prepare()
    te = datetime.now()
    print("回测准备与导入数据用时", te-ts)
    ts = datetime.now()
    backtest_engine.start_backtest()
    te = datetime.now()
    print("回测+编译用时", te-ts)
    ts = datetime.now()
    backtest_engine.export_results()
    te = datetime.now()
    print("保存回测结果和策略状态用时", te-ts)
    te0 = datetime.now()
    print("回测总用时", te0-ts0)

    #read result
    path_name = os.path.join("examples/results/BTCUSD/", f"BTCUSD.hdf5")
    result_reader = ResultReader(path_name)
    result_reader.to_csv(export_folder='examples/results/BTCUSD/', id_list=list(range(9)))

