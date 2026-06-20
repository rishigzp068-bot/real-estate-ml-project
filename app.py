# ==============================
# IMPORT LIBRARIES
# ==============================
import streamlit as st
import pandas as pd
import numpy as np

# Safe Plotly import
try:
    import plotly.express as px
    plotly_available = True
except:
    plotly_available = False

from sklearn.linear_model import LinearRegression

# ==============================
# PAGE CONFIG
# ==============================
st.set_page_config(page_title="Real Estate Analysis", layout="wide")

st.title("🏡 Real Estate Data Analysis Dashboard")
st.markdown("### 📊 Final Year Project | Data Analysis + Machine Learning")

# ==============================
# LOAD DATA (EXCEL FILE)
# ==============================
@st.cache_data
def load_data():
    df = pd.read_excel("Final_Analyzed_RealEstate_Data.xlsx")
    return df

df = load_data()

# ==============================
# DATA PREVIEW
# ==============================
st.subheader("📄 Dataset Preview")
st.dataframe(df.head())

# ==============================
# BASIC CLEANING (SAFE)
# ==============================
df = df.drop_duplicates()

# ==============================
# KPI SECTION
# ==============================
st.subheader("📌 Key Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("Total Properties", len(df))

# Try common column names safely
price_col = None
for col in df.columns:
    if "price" in col.lower():
        price_col = col
        break

if price_col:
    col2.metric("Average Price", f"{int(df[price_col].mean())}")
else:
    col2.metric("Average Price", "N/A")

col3.metric("Total Columns", len(df.columns))

# ==============================
# VISUALIZATION
# ==============================
st.subheader("📊 Visual Analysis")

if plotly_available:

    # Price Distribution
    if price_col:
        fig1 = px.histogram(df, x=price_col, title="Price Distribution")
        st.plotly_chart(fig1, use_container_width=True)

    # First categorical column chart
    cat_col = None
    for col in df.columns:
        if df[col].dtype == "object":
            cat_col = col
            break

    if cat_col:
        fig2 = px.bar(df, x=cat_col, title=f"{cat_col} Distribution")
        st.plotly_chart(fig2, use_container_width=True)

else:
    st.warning("Plotly not installed. Please check requirements.txt")

# ==============================
# MACHINE LEARNING MODEL
# ==============================
st.subheader("🤖 Price Prediction")

# Try to find numeric columns for ML
numeric_cols = df.select_dtypes(include=np.number).columns.tolist()

if len(numeric_cols) >= 2:
    X = df[[numeric_cols[0]]]
    y = df[numeric_cols[1]]

    model = LinearRegression()
    model.fit(X, y)

    val = st.slider(f"Select {numeric_cols[0]}", int(X.min()), int(X.max()))

    prediction = model.predict([[val]])

    st.success(f"Predicted {numeric_cols[1]}: {int(prediction[0])}")

else:
    st.warning("Not enough numeric columns for prediction")

# ==============================
# DOWNLOAD DATA
# ==============================
st.subheader("📥 Download Data")

csv = df.to_csv(index=False).encode('utf-8')

st.download_button(
    label="Download CSV",
    data=csv,
    file_name="processed_data.csv",
    mime="text/csv"
)
