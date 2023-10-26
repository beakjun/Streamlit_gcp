import streamlit as st
import pandas as pd
import numpy as np
import psycopg2
import plotly.graph_objects as go

@st.cache_resource
def init_connection():
    return psycopg2.connect(**st.secrets["postgres"])

conn = init_connection()


# 검색 셀레트 박스에 들어가는 리스트 생성 
def make_searchlist():
    query='select distinct "itmsNm","srtnCd" from stockprice_info.kospi_stockprice_info order by "srtnCd"'
    df=pd.read_sql_query(query,con=conn)
    df['new']=df['itmsNm']+'  '+df['srtnCd']
    return list(df['new'])

# 검색 셀렉트 박스 & 보조지표 멀티박스
placeholder = st.empty()
col1, col2 = st.columns(2)
with col1 :
    option = st.selectbox('종목을 선택하세요',
                   make_searchlist(),
                   index = 1)


with col2 : 
    st.write('보조 지표')
    col11,col_gap1,col22=st.columns([0.05,0.0001,0.05])
    
    with col11:
        macd=st.checkbox("MACD")
    with col22:
        rsi=st.checkbox("RSI")




### 검색 결과 데이터 프레임 생성 
@st.cache_data(ttl=600)
def run_query(query):
    df = pd.read_sql_query(query,con=conn)
    return df
query2=f"SELECT * from stockprice_info.kospi_stockprice_info where \"itmsNm\" = '{option[:-8]}' order by \"basDt\" "
df = run_query(query2)

### 검색 결과 데이터 프레임 생성 
@st.cache_data(ttl=600)
def run_query(query):
    df = pd.read_sql_query(query,con=conn)
    return df
query2=f"SELECT * from stockprice_info.kospi_stockprice_info where \"itmsNm\" = '{option[:-8]}' order by \"basDt\" "
df = run_query(query2)

### class 호출
indicators = TechnicalIndicators(df)
indicators.preprocess_data()
main_df=indicators.df.copy()

indicators.compute_macd()

indicators.compute_rsi()
rsi_df=indicators.df

placeholder1 = st.empty()

placeholder1.plotly_chart(candlechart.plot_candlestick(rsi_df, '주식 캔들 차트',macd,rsi))

placeholder.title(f'{option.split()[0]} 일별 주가') # 종목이름으로 타이틀