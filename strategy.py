import numpy as np
import pandas as pd
import talib
from indicator import get_indicators



class Strategy:


    def __init__(self,indicator):
        self.indicator = indicator



    def get_signal(self):
        if self.indicator[3] > self.indicator[4] and self.indicator[6] < -100:
            entry_price = self.indicator[4]
            take_profit = entry_price * 1.01
            stop_loss = entry_price * 0.996
            return {'action': True, 'entry_price': entry_price, 'tp': take_profit, 'SL': stop_loss,'type':'LONG','time':self.indicator[5],'open':0}
        
        if self.indicator[4] > self.indicator[2] and self.indicator[6] > 120:
            entry_price = self.indicator[4]
            take_profit = entry_price * 1.011
            stop_loss = entry_price * 0.995
            return {'action': True, 'entry_price': entry_price, 'tp': take_profit, 'SL': stop_loss,'type':'SHORT','time':self.indicator[5],'open':0}
        return {'action':False}



def run_strat():
    price_data = pd.read_csv('result.csv')
    cci_period = 30
    cci = talib.CCI(price_data[' High'], price_data[' Low'], price_data[' Close'], timeperiod=cci_period)
    cci = pd.Series(cci, name='CCI')
    rsibands_lb = get_indicators()
    df = pd.concat([rsibands_lb,cci],ignore_index=True, axis=1)
    actions = []
    action_list = []
    for item in df.itertuples():
        action = Strategy(item).get_signal()
        if action.get('action'):
            actions.append(action)
        action_list.append(action)
    return action_list

if __name__ == '__main__':
    run_strat()