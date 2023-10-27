import streamlit as st
import pandas as pd
import numpy as np
import psycopg2
import plotly.graph_objects as go



# 페이지 설정
st.set_page_config(page_title="📊주가 현황", layout="wide")

# 메인 페이지 타이틀
st.title("📊주가 현황")


@st.cache_resource
def init_connection():
    return psycopg2.connect(**st.secrets["postgres"])


def run_query(query):
    df = pd.read_sql_query(query,con=conn)
    return df


def display_metrics(column, df,idx):
    title = f"{df['mrktCtg'].iloc[idx]} $\\newline$ {df['itmsNm'].iloc[idx]}"
    value = f"{df['clpr'].iloc[idx]}"
    delta = f"{df['fltRt'].iloc[idx]}%({df['vs'].iloc[idx]})"
    column.metric(title, value, delta, delta_color="inverse")

st.subheader("주요 증시 현황")
kospi_url = 'https://finance.naver.com/sise/sise_index_day.naver?code=KOSPI&page=1'
#kosdaq_url

st.dataframe(pd.read_html(kospi_url,encoding='cp949')[0])


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
