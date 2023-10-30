import pandas as pd
from strategy import run_strat
import numpy as np
from threading import Thread
import json
#balance = 104128.10000011948





class Backtester:
    def __init__(self, historical_data):
        self.historical_data = historical_data
        self.balance = 100000  
        self.commission_rate = 0.05 / 100  # Комісія 0.05%
        self.trade_size = 100  

        self.tp = 0
        self.sl = 0

        self.trades = []

    def backtest(self, signal):
        index = self.historical_data[self.historical_data['Open time'] == signal.get('time')].index[0]
        if signal.get('type') == 'LONG':
            tp_time = self.historical_data[(self.historical_data.index > index) & (self.historical_data[" Close"] > signal.get('tp'))]["Open time"]
            sl_time = self.historical_data[(self.historical_data.index > index) & (self.historical_data[" Close"] < signal.get('SL'))]["Open time"]
            if len(tp_time) != 0:
                first_tp_time = tp_time[tp_time.index[0]]
            if len(sl_time) != 0:
                sl_tp_time = sl_time[sl_time.index[0]]
            if len(tp_time) !=0 and len(sl_time) !=0:
                if first_tp_time > sl_tp_time:
                    self.balance = self.balance+self.trade_size*0.01
                    signal['win'] = True
                    signal['lose'] = False
                    self.trades.append(signal)
                else:
                    self.balance = self.balance-self.trade_size*0.004
                    signal['win'] = False
                    signal['lose'] = True
                    self.trades.append(signal)
        else:
            tp_time = self.historical_data[(self.historical_data.index > index) & (self.historical_data[" Close"] < signal.get('tp'))]["Open time"]
            sl_time = self.historical_data[(self.historical_data.index > index) & (self.historical_data[" Close"] > signal.get('SL'))]["Open time"]
            if len(tp_time) != 0:
                first_tp_time = tp_time[tp_time.index[0]]
            if len(sl_time) != 0:
                sl_tp_time = sl_time[sl_time.index[0]]
            if len(tp_time) !=0 and len(sl_time) !=0:
                if first_tp_time > sl_tp_time:
                    self.balance = self.balance+self.trade_size*0.011
                    signal['win'] = True
                    signal['lose'] = False
                    self.trades.append(signal)
                else:
                    self.balance = self.balance-self.trade_size*0.005
                    signal['win'] = False
                    signal['lose'] = True
                    self.trades.append(signal)


# def run_backtester(signals):
#     x=0
#     for signal in signals:
#         print(f'{x}/{len(signals)}')
#         x=x+1
#         backtester.backtest(signal)



# historical_data = pd.read_csv('result.csv')  # Завантажте історичні дані з CSV файлу
# signals = []
# for signal in run_strat():
#     if signal.get('action') == True:
#         signals.append(signal)


# backtester = Backtester(historical_data)

# res = np.array_split(signals, 1000)
# threads = []
# for item in res:
#     thread = Thread(target=run_backtester,args=(item,))
#     threads.append(thread)
# for t in threads:
#     t.start()
# for t in threads:
#     t.join()

wins = []
loses = []

f = open('data.json')
data = json.load(f)

for item in data:
    if item.get('win') == True:
        wins.append(item)
    else:
        loses.append(item)

profit = 0
lose = 0
for item in wins:
    if item.get('type') == 'LONG':
        profit=profit+1
    else:
        profit=profit+1.1

for item in loses:
    if item.get('type') == 'LONG':
        lose=lose+0.4
    else:
        lose=lose+0.5
import pdb;pdb.set_trace()
