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


st.text("hello streamlits1111231")