import streamlit as st
import pandas as pd
import numpy as np
import psycopg2
import plotly.graph_objects as go

import candlechart
from TechnicalIndicators import TechnicalIndicators
st.set_page_config(page_title="📊주가 현황", layout="wide")
@st.cache_resource
def init_connection():
    return psycopg2.connect(**st.secrets["postgres"])

#conn = init_connection()

### 그래프 크게 보기 표시 제거
hide_img_fs = '''
<style>
button[title="View fullscreen"]{
    visibility: hidden;}
</style>
'''
st.markdown(hide_img_fs, unsafe_allow_html=True)

# 검색 셀레트 박스에 들어가는 리스트 생성
@st.cache_data
def make_searchlist():
    query='select distinct "itmsNm","srtnCd" from stockprice_info.kospi_stockprice_info order by "srtnCd"'
    with init_connection() as conn:
        df=pd.read_sql_query(query,con=conn)
    df['new']=df['itmsNm']+'  '+df['srtnCd']
    return list(df['new'])

# 검색 셀렉트 박스 & 보조지표 멀티박스
placeholder = st.empty()

option = st.selectbox('종목을 선택하세요',
                make_searchlist(),
                index = 1)



st.sidebar.subheader('주요지표')
macd=st.sidebar.checkbox('MACD')
rsi=st.sidebar.checkbox('RSI')


### 검색 결과 데이터 프레임 생성 
@st.cache_data(ttl=600)
def run_query(query):
    with init_connection() as conn:
        df = pd.read_sql_query(query,con=conn)
    return df
query2=f"SELECT * from stockprice_info.kospi_stockprice_info where \"itmsNm\" = '{option[:-8]}' order by \"basDt\" "
df = run_query(query2)

# df.apply(lambda )


### class 호출
indicators = TechnicalIndicators(df)
indicators.preprocess_data()
main_df=indicators.df.copy()
indicators.compute_macd()

indicators.compute_rsi()
rsi_df=indicators.df

placeholder1 = st.empty()

placeholder1.plotly_chart(candlechart.plot_candlestick(rsi_df, '주식 캔들 차트',macd,rsi),use_container_width=True)



placeholder.title(f'💹{option.split()[0]} 일별 주가') # 종목이름으로 타이틀

