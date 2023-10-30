from binance.client import AsyncClient,Client
import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
import asyncio



def generate_dates():
    dates = []
    for i in range(0,4*12):
        year = i//12
        month = i-year*12
        end_date = datetime.datetime.now(tz=None) - relativedelta(years=year,months=month)
        start_date = datetime.datetime.now(tz=None) - relativedelta(years=year,months=month+1)
        dates.append({'start_date':start_date.strftime('%d %b %Y'),'end_date':end_date.strftime('%d %b %Y')})
    return dates





async def get_klines(date):
    client = await AsyncClient.create()    
    klines = await client.get_historical_klines(symbol="BTCUSDT", interval=AsyncClient.KLINE_INTERVAL_1MINUTE,start_str=date.get('start_date'),end_str=date.get('end_date'))
    await client.close_connection()
    klines.reverse()
    return klines




async def main():
    dates = generate_dates()
    kline_tasks = []
    for item in dates:
        kline_tasks.append(asyncio.create_task(get_klines(item)))
    results = await asyncio.gather(*kline_tasks)
    columns='Open time, Open, High, Low, Close, Volume, Close time, Quote asset volume, Number of trades, Taker buy base asset volume, Taker buy quote asset volume, Ignore'.split(',')
    result = [x for item in results for x in item]
    result_with_timestamp = []
    for item in result:
        # item[0]=str(datetime.datetime.fromtimestamp(int(str(item[0])[:10])))
        item[0] = int(str(item[0])[:10])
        result_with_timestamp.append(item)
    result_with_timestamp.reverse()
    df = pd.DataFrame(result_with_timestamp,columns = columns)    
    df.to_csv("result.csv")




if __name__ == "__main__":
    asyncio.run(main())
