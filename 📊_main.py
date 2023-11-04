import streamlit as st
import pandas as pd
import numpy as np
import psycopg2
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import datetime

# 페이지 설정
st.set_page_config(page_title="📊주가 현황", layout="wide")

### 그래프 크게 보기 표시 제거
hide_img_fs = '''
<style>
button[title="View fullscreen"]{
    visibility: hidden;}
</style>
'''
st.markdown(hide_img_fs, unsafe_allow_html=True)


# 메인 페이지 타이틀
st.title("📊주가 현황")

# 공백 생성
st.write("")

# DB 연결 함수
@st.cache_resource
def init_connection():
    return psycopg2.connect(**st.secrets["postgres"])

# 쿼리 생성 함수
@st.cache_data
def run_query(query):
    df = pd.read_sql_query(query,con=conn)
    return df

# 데이터 날짜 추출
with init_connection() as conn:
    dt = run_query('select "basDt" from stockprice_info.stockprice_stat limit 1').iat[0,0]
md=dt.strftime("%m.%d")
ymd=dt.strftime("%Y.%m.%d")

# 하위 제목
st.subheader(f"주요 증시 현황 ({md})",divider='grey')

# 크롤링 URL 정의
kospi_url = 'https://finance.naver.com/sise/sise_index_day.naver?code=KOSPI&page='
kospi200_url = 'https://finance.naver.com/sise/sise_index_day.naver?code=KPI200&page='
kosdaq_url ='https://finance.naver.com/sise/sise_index_day.naver?code=KOSDAQ&page='

@st.cache_data
def display_metric2(url,ymd,w):
    url = url+'1'
    df = pd.read_html(url,encoding='cp949')[0]
    df = df[df['날짜']==ymd]
    title = w
    value = f"{df['체결가'].iat[0]:,}"
    delta = f"{df['등락률'].iat[0]}({df['전일비'].iat[0]})"
    return title, value, delta






@st.cache_data
def fetch_data(url, days=90):
    odt = dt - datetime.timedelta(days=days) 
    oymd = odt.strftime("%Y.%m.%d")

    new_df = pd.DataFrame()
    for i in range(1, int(days/3)):
        new_url = url + str(i)
        df = pd.read_html(new_url, encoding='cp949')[0]
        new_df = pd.concat([new_df, df], ignore_index=True)

    new_df = new_df.dropna()
    graph_df = new_df[(new_df['날짜'] >= oymd) & (new_df['날짜'] <= ymd)].sort_values(by='날짜', ascending=True)
    return graph_df

def display_chart(url, _col, days=90):
    graph_df = fetch_data(url, days)

    if graph_df[graph_df['날짜'] == ymd]['등락률'].iloc[0][0] == '-':
        color = '#007aff'
    else: 
        color = '#e52300'
    
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(graph_df['날짜'], graph_df['체결가'], color=color, linewidth=3.5, alpha=0.7)
    poly = ax.fill_between(graph_df['날짜'], graph_df['체결가'], graph_df['체결가'].min(), alpha=0.05, color=color)
    ylim = ax.get_ylim()
    ax.spines['top'].set_alpha(0)
    ax.spines['right'].set_alpha(0)
    ax.spines['bottom'].set_alpha(0.1)
    ax.spines['left'].set_alpha(0.1)

    plt.xticks([])
    plt.yticks([])
    
    _col.pyplot(fig)

### 지스 메트릭 
col1,colgap1,col2,colgap2,col3=st.columns([1,0.2,1,0.2,1])
title,value,delta=display_metric2(kospi_url,ymd,"코스피")
col1.metric(title,value,delta,delta_color="inverse")
title,value,delta=display_metric2(kosdaq_url,ymd,"코스닥")
col2.metric(title,value,delta,delta_color="inverse")
title,value,delta=display_metric2(kospi200_url,ymd,"코스피200")
col3.metric(title,value,delta,delta_color="inverse")

### 그래프
display_chart(kospi_url,col1)
display_chart(kosdaq_url,col2)
display_chart(kospi200_url,col3)

st.write("")
st.write("")

def display_metrics(column, df,idx):
    title = f"{df['mrktCtg'].iloc[idx]} $\\newline$ {df['itmsNm'].iloc[idx]}"
    value = f"{df['clpr'].iloc[idx]:,}"
    delta = f"{df['fltRt'].iloc[idx]}%({df['vs'].iloc[idx]})"
    column.metric(title, value, delta, delta_color="inverse")



st.subheader("TOP10 종목")
tab1, tab2, tab3, tab4 = st.tabs(["📈 상승","📉 하락" , "💸 거래상위", "💰 시가총액 상위"])

with tab1:
    with init_connection() as conn:
        df = run_query('select "itmsNm","mrktCtg", "clpr", "vs", "fltRt" from stockprice_info.stockprice_stat order by "fltRt" desc limit 10')
    columns = st.columns(5)
    for i in range(10):
        col = columns[i%5]
        display_metrics(col,df,i)
with tab2:
    with init_connection() as conn:
        df = run_query('select "itmsNm","mrktCtg", "clpr", "vs", "fltRt" from stockprice_info.stockprice_stat order by "fltRt" asc limit 10')
    columns = st.columns(5)
    for i in range(10):
        col = columns[i%5]
        display_metrics(col,df,i)
with tab3:
    with init_connection() as conn:
        df = run_query('select "itmsNm","mrktCtg", "clpr", "vs", "fltRt" from stockprice_info.stockprice_stat order by "trqu" desc limit 10')
    columns = st.columns(5)
    for i in range(10):
        col = columns[i%5]
        display_metrics(col,df,i)
with tab4:
    with init_connection() as conn:
        df = run_query('select "itmsNm","mrktCtg", "clpr", "vs", "fltRt" from stockprice_info.stockprice_stat order by "mrktTotAmt" desc limit 10')
    columns = st.columns(5)
    for i in range(10):
        col = columns[i%5]
        display_metrics(col,df,i)
