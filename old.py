# study("RSI Bands [LazyBear]", shorttitle="RSIBANDS_LB", overlay=true)
import talib
import pandas as pd
import numpy
import mplfinance as mpf
import datetime



# def RSIBANDS_LB():
df = pd.read_csv('result.csv')
df = df[[' Close']]

lst = [x for item in df.values.tolist() for x in item]

obLevel = 70 # RSI Overbought
osLevel = 30 #RSI Oversold
length = 14 # RSI Length


src=[lst[0],lst[1]]


#текущий - прошлый и максимум



# for item in lst[:-1]:
#     result = max(item - lst[lst.index(item)+1],0)
#     print(result)
#     auc_list.append(result)
adc_list = []
auc_list = []
lst = lst[-300:]

for item in lst[:-1]:
    result = max(item - lst[lst.index(item)+1],0)
    auc_list.append(result)
    result = max(lst[lst.index(item)+1]-item,0)
    adc_list.append(result)
auc_array = numpy.array(auc_list)
adc_array = numpy.array(adc_list)

print('result1')


ep = 2 * length - 1

auc = talib.EMA(auc_array,ep)
adc = talib.EMA(adc_array,ep)

auc = auc.tolist()
adc = adc.tolist()
print('result2')
x1_dict = []

for item in auc:
    index = auc.index(item)
    x1_dict.append({'auc':item,'adc':adc[index],'src':lst[index]})
print('result3')
for item in x1_dict:
    item['x1']=((length - 1) * ( item.get('adc') * obLevel / (100-obLevel) - item.get('auc')))
    item['x2'] = ((length - 1) * ( item.get('adc') * osLevel / (100-osLevel) - item.get('auc')))
print('result4')
for item in x1_dict:
    if item.get('x1') >=0:
        item['ub'] = item.get('src')+item.get('x1')
    else:
        item['ub'] = item.get('src') + item.get('x1') * (100-obLevel)/obLevel

    if item.get('x2') >=0:
        item['lb'] = item.get('src')+item.get('x2')
    else:
        item['lb'] = item.get('src')+item.get('x2') * (100-osLevel)/osLevel
    
    item['avg'] = (item.get('ub')+item.get('lb'))/2


result = []
print('result5')
for item in x1_dict:
    result.append({'Resistance':item.get('ub'),'Support':item.get('lb'),'RSI Midline':item.get('avg')})
    # ,'Price':item.get('src')
print('result6')
    # return pd.DataFrame.from_records(result)

df = pd.DataFrame.from_records(result)
df.plot(kind='line',style={'Resistance': 'r', 'Support': 'g', 'RSI Midline': '#4f5250'},grid=True,title='RSI Bands [LazyBear]').get_figure().savefig('plot.pdf')
