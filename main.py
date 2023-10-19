import streamlit as st
import pandas as pd
import numpy as np
import psycopg2
import plotly.graph_objects as go

@st.cache_resource
def init_connection():
    return psycopg2.connect(**st.secrets["postgres"])

conn = init_connection()








st.text("hello streamlit")