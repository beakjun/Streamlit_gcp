import plotly.graph_objects as gop
import streamlit as st
import pandas as pd
import numpy as np
import psycopg2

class TechnicalIndicators:
    def __init__(self,dataframe):
        self.df= dataframe

    def preprocess_data(self):
        self.df['basDt'] = pd.to_datetime(self.df['basDt'], format='%Y%m%d')
        self.df['basDt'] = self.df['basDt'].apply(lambda x:x.date())
        self.df['fltRt']=self.df['fltRt'].astype(float)
        self.df = self.df.astype({'clpr':int,'vs':int,'mkp':int,'hipr':int,'lopr':int,'trqu':int,'trPrc':int,'clpr':int,'lstgStCnt':int,'mrktTotAmt':int,})
        self.df = self.df.sort_values(by=['basDt'])

    def compute_macd(self, macd_short=12, macd_long=26, macd_signal=9):
        self.df['MACD_short']=self.df['clpr'].ewm(span=macd_short).mean()
        self.df['MACD_long'] = self.df['clpr'].ewm(span=macd_long).mean()
        self.df['MACD']=self.df.apply(lambda x: (x['MACD_short']-x['MACD_long']), axis=1)
        self.df['MACD_signal'] = self.df['MACD'].ewm(span=macd_signal).mean()
        self.df['MACD_oscillator'] = self.df.apply(lambda x:(x['MACD'] - x['MACD_signal']),axis=1)
    
    def compute_rsi(self):
        self.df['상승폭'] = np.where(self.df['vs']>=0, self.df['vs'],0)
        self.df['하락폭'] = np.where(self.df['vs']<0, self.df['vs'].abs(),0)

        self.df['AU'] = self.df['상승폭'].ewm(alpha=1/14, min_periods=14).mean()
        self.df['AD'] = self.df['하락폭'].ewm(alpha=1/14, min_periods=14).mean()
        self.df['RSI'] = self.df['AU']/(self.df['AU']+self.df['AD'])*100


if __name__=="__main__":
    conn = psycopg2.connect(host='localhost',port=5431, user='postgres', password='POSTGRES_PASS', database='postgres')
    query = 'SELECT * FROM  airflow.stock_market_tbl where "itmsNm"=\'삼성전자\''
    df= pd.read_sql_query(query, conn)

    indicators = TechnicalIndicators(df)
    indicators.preprocess_data()
    indicators.compute_macd()
    indicators.compute_rsi()

    print(indicators.df)




