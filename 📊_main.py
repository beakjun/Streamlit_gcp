import streamlit as st
import pandas as pd
import numpy as np
import psycopg2
import plotly.graph_objects as go
import matplotlib.pyplot as plt


# 페이지 설정
st.set_page_config(page_title="📊주가 현황", layout="wide")

# 메인 페이지 타이틀
st.title("📊주가 현황")


@st.cache_resource
def init_connection():
    return psycopg2.connect(**st.secrets["postgres"])

@st.cache_data
def run_query(query):
    df = pd.read_sql_query(query,con=conn)
    return df
with init_connection() as conn:
    dt = run_query('select "basDt" from stockprice_info.stockprice_stat limit 1').iat[0,0]

md=dt.strftime("%m.%d")
ymd=dt.strftime("%Y.%m.%d")


st.subheader(f"주요 증시 현황 ({md})")

kospi_url = 'https://finance.naver.com/sise/sise_index_day.naver?code=KOSPI&page=1'
kospi200_url = 'https://finance.naver.com/sise/sise_index_day.naver?code=KPI200&page=1'
kosdaq_url ='https://finance.naver.com/sise/sise_index_day.naver?code=KOSDAQ&page=1'

def display_metric2(url,ymd,col,w):
    df = pd.read_html(url,encoding='cp949')[0]
    df = df[df['날짜']==ymd]
    title = w
    value = df['체결가']
    delta = f"{df['등락률'].iat[0]}({df['전일비'].iat[0]})"
    col.metric(title, value, delta, delta_color="inverse")
    

col1,col2,col3,col4,col5,col6,col7,col8=st.columns(8)
display_metric2(kospi_url,ymd,col2,"코스피")
display_metric2(kosdaq_url,ymd,col5,"코스닥")


cols1,cols2,gap1,cols3,cols4=st.columns([0.1,1,0.2,1,1])
np.random.seed(123)
x = np.linspace(0, 10, 200)
y = np.random.normal(0.01, 1, 200).cumsum()
fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(x, y,color='white')

ylim = ax.get_ylim()

grad1 = ax.imshow(np.linspace(0, 1, 256).reshape(-1, 1), cmap='Reds', vmin=-0.05, aspect='auto',
                  extent=[x.min(), x.max(), 0, y.max()], origin='lower')
poly_pos = ax.fill_between(x, y.min(), y, alpha=0.05)
grad1.set_clip_path(poly_pos.get_paths()[0], transform=ax.transData)
poly_pos.remove()
plt.axis('off')
grad2 = ax.imshow(np.linspace(0, 1, 256).reshape(-1, 1), cmap='Blues', vmin=-0.5, aspect='auto',
                  extent=[x.min(), x.max(), y.min(), 0], origin='upper')
poly_neg = ax.fill_between(x, y, y.max(), alpha=0.1)
grad2.set_clip_path(poly_neg.get_paths()[0], transform=ax.transData)
poly_neg.remove()

cols2.pyplot(fig)
cols3.pyplot(fig)

st.write("")
st.write("")

def display_metrics(column, df,idx):
    title = f"{df['mrktCtg'].iloc[idx]} $\\newline$ {df['itmsNm'].iloc[idx]}"
    value = f"{df['clpr'].iloc[idx]}"
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
