import pandas as pd
import numpy as np
import talib


def get_indicators():
    data = pd.read_csv('result.csv')
    obLevel = 70
    osLevel = 30
    length = 14

    src = data[' Close']

    ep = 2*length-1
    auc = talib.EMA(np.maximum(src-src.shift(1),0), timeperiod=ep)
    adc = talib.EMA(np.maximum(src.shift(1)-src,0),timeperiod=ep)

    x1 = (length-1)*(adc*obLevel/(100-obLevel)-auc)
    ub = np.where(x1>=0,src+x1,src+x1*(100 - obLevel)/obLevel)

    x2 = (length-1)*(adc*osLevel/(100-osLevel)-auc)
    lb = np.where(x2>=0,src+x2,src+x2*(100-osLevel)/osLevel)

    rsi_middle = (ub+lb)/2

    indicators = pd.DataFrame({'RSI Midline': rsi_middle, 'Resistance': ub, 'Support': lb,'Price':src,'Time':data["Open time"]})
    return indicators

if __name__ == '__main__':
    indicators = get_indicators()
    indicators.plot(kind='line',style={'Resistance': 'r', 'Support': 'g', 'RSI Midline': '#4f5250'},grid=True,title='RSI Bands [LazyBear]').get_figure().savefig('plot.pdf')

