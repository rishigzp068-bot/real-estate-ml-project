import streamlit as st
import pandas as pd
import numpy as np

# Safe Plotly import
try:
    import plotly.express as px
    plotly_available = True
except:
    plotly_available = False

# Page config
st.set_page_config(page_title="Real Estate Dashboard", layout="wide")
st.title("🏡 Real Estate Analysis Dashboard")

# ==============================
# LOAD DATA (SAFE)
# ==============================
@st.cache_data
def load_data():
    try:
        df = pd.read_excel("Final_Analyzed_RealEstate_Data.xlsx", engine="openpyxl")
        return df
    except Exception as e:
        st.error(f"Error loading file: {e}")
        return None

df = load_data()

if df is None:
    st.stop()

# ==============================
# DATA PREVIEW
# ==============================
st.subheader("Dataset Preview")
st.write(df.head())

# ==============================
# CLEANING
# ==============================
df = df.drop_duplicates()

# ==============================
# KPI
# ==============================
st.subheader("Key Metrics")

col1, col2 = st.columns(2)
col1.metric("Total Rows", df.shape[0])
col2.metric("Total Columns", df.shape[1])

# ==============================
# VISUALIZATION (SAFE)
# ==============================
st.subheader("Visuals")

if plotly_available:
    numeric_cols = df.select_dtypes(include=np.number).columns

    if len(numeric_cols) > 0:
        fig = px.histogram(df, x=numeric_cols[0], title="Numeric Distribution")
        st.plotly_chart(fig, use_container_width=True)

else:
    st.warning("Plotly not installed")

# ==============================
# DOWNLOAD
# ==============================
csv = df.to_csv(index=False).encode('utf-8')

st.download_button(
    label="Download Data",
    data=csv,
    file_name="data.csv",
    mime="text/csv"
)
