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

conn = init_connection()

def run_query(query):
    df = pd.read_sql_query(query,con=conn)
    return df


tab1, tab2, tab3, tab4 = st.tabs(["📈 상승","📉 하락" , "💸 거래상위", "💰 시가총액 상위"])

with tab1:
    df = run_query('select "itmsNm","mrktCtg", "clpr", "vs", "fltRt" from stockprice_info.stockprice_stat order by "fltRt" desc limit 10')
    st.dataframe(df)
    tab1.metric(f"{df['mrktCtg'].iloc[0]} $\\newline $ {df['itmsNm'].iloc[0]}",f"{df['clpr'].iloc[0]}",f"{df['fltRt'].iloc[0]}%({df['vs'].iloc[0]})",delta_color="inverse")
with tab2:
    df = run_query('select "itmsNm","mrktCtg", "clpr", "vs", "fltRt" from stockprice_info.stockprice_stat order by "fltRt" asc limit 10')
    st.dataframe(df)
    tab2.metric(f"{df['mrktCtg'].iloc[0]} $\\newline $ {df['itmsNm'].iloc[0]}",f"{df['clpr'].iloc[0]}",f"{df['fltRt'].iloc[0]}%({df['vs'].iloc[0]})",delta_color="inverse")
with tab3:
    df = run_query('select "itmsNm","mrktCtg", "clpr", "vs", "fltRt" from stockprice_info.stockprice_stat order by "trqu" desc limit 10')
    st.dataframe(df)
with tab4:
    df = run_query('select "itmsNm","mrktCtg", "clpr", "vs", "fltRt" from stockprice_info.stockprice_stat order by "mrktTotAmt" desc limit 10')
    st.dataframe(df)
