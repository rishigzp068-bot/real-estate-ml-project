# ==============================
# IMPORT LIBRARIES
# ==============================
import streamlit as st
import pandas as pd
import numpy as np

# Safe import for Plotly
try:
    import plotly.express as px
    plotly_available = True
except:
    plotly_available = False

from sklearn.linear_model import LinearRegression

# ==============================
# PAGE CONFIG
# ==============================
st.set_page_config(page_title="Employee Attrition Dashboard", layout="wide")

st.title("📊 Employee Attrition Analysis")

# ==============================
# DATA SOURCE OPTION
# ==============================
option = st.radio("Select Data Source", ["Use Default Data", "Upload Your Data"])

# ==============================
# LOAD DATA
# ==============================
if option == "Upload Your Data":
    file = st.file_uploader("Upload CSV File", type=["csv"])
    if file is not None:
        df = pd.read_csv(file)
    else:
        st.warning("Please upload a file")
        st.stop()
else:
    # 👉 Make sure data.csv exists in your GitHub repo
    df = pd.read_csv("data.csv")

# ==============================
# SHOW DATA
# ==============================
st.subheader("Dataset Preview")
st.write(df.head())

# ==============================
# DATA CLEANING
# ==============================
df.drop_duplicates(inplace=True)

for col in df.columns:
    if df[col].dtype == "object":
        df[col].fillna(df[col].mode()[0], inplace=True)
    else:
        df[col].fillna(df[col].median(), inplace=True)

# ==============================
# FEATURE ENGINEERING
# ==============================
if 'Age' in df.columns:
    df['AgeGroup'] = pd.cut(
        df['Age'],
        bins=[18, 25, 35, 50, 60],
        labels=['18-25', '26-35', '36-50', '50+'],
        include_lowest=True
    )

# ==============================
# KPI METRICS
# ==============================
st.subheader("📌 Key Metrics")

col1, col2 = st.columns(2)

col1.metric("Total Employees", len(df))

if 'Attrition' in df.columns:
    attrition_rate = (df['Attrition'].value_counts(normalize=True).get('Yes', 0)) * 100
    col2.metric("Attrition Rate", f"{attrition_rate:.2f}%")

# ==============================
# CHARTS
# ==============================
st.subheader("📊 Visual Analysis")

if plotly_available:

    if 'Department' in df.columns:
        fig = px.bar(df, x='Department', title="Department Distribution")
        st.plotly_chart(fig, use_container_width=True)

    if 'Attrition' in df.columns:
        fig = px.pie(df, names='Attrition', title="Attrition Distribution")
        st.plotly_chart(fig, use_container_width=True)

    if 'AgeGroup' in df.columns:
        fig = px.histogram(df, x='AgeGroup', title="Age Group Distribution")
        st.plotly_chart(fig, use_container_width=True)

else:
    st.warning("Plotly not installed. Charts not available.")

# ==============================
# PREDICTION MODEL
# ==============================
st.subheader("🤖 Salary Prediction")

if 'Age' in df.columns and 'MonthlyIncome' in df.columns:

    X = df[['Age']]
    y = df['MonthlyIncome']

    model = LinearRegression()
    model.fit(X, y)

    age = st.slider("Select Age", 18, 60, 30)
    pred = model.predict([[age]])

    st.success(f"Predicted Salary: ₹ {int(pred[0])}")

# ==============================
# DOWNLOAD DATA
# ==============================
st.subheader("📥 Download Processed Data")

csv = df.to_csv(index=False).encode('utf-8')

st.download_button(
    label="Download CSV",
    data=csv,
    file_name="analyzed_data.csv",
    mime="text/csv"
)
