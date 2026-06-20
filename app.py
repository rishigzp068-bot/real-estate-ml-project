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
st.set_page_config(page_title="Employee Attrition Analysis", layout="wide")

st.title("📊 Employee Attrition Analysis Dashboard")
st.markdown("### 📌 Final Year Project | Data Analysis + ML Model")

# ==============================
# LOAD FINAL DATA (AUTO LOAD)
# ==============================
@st.cache_data
def load_data():
    return pd.read_csv("final_data.csv")   # 👈 your final file name

df = load_data()

# ==============================
# SHOW DATA
# ==============================
st.subheader("📄 Final Analyzed Dataset")
st.dataframe(df.head())

# ==============================
# KPI METRICS
# ==============================
st.subheader("📌 Key Insights")

col1, col2, col3 = st.columns(3)

col1.metric("Total Employees", len(df))

if 'Attrition' in df.columns:
    attrition_rate = (df['Attrition'].value_counts(normalize=True).get('Yes', 0)) * 100
    col2.metric("Attrition Rate", f"{attrition_rate:.2f}%")
else:
    col2.metric("Attrition Rate", "N/A")

if 'MonthlyIncome' in df.columns:
    col3.metric("Avg Salary", int(df['MonthlyIncome'].mean()))
else:
    col3.metric("Avg Salary", "N/A")

# ==============================
# CHARTS
# ==============================
st.subheader("📊 Visual Dashboard")

if plotly_available:

    if 'Department' in df.columns:
        fig1 = px.bar(df, x='Department', title="Employees by Department")
        st.plotly_chart(fig1, use_container_width=True)

    if 'Attrition' in df.columns:
        fig2 = px.pie(df, names='Attrition', title="Attrition Distribution")
        st.plotly_chart(fig2, use_container_width=True)

    if 'Age' in df.columns:
        fig3 = px.histogram(df, x='Age', title="Age Distribution")
        st.plotly_chart(fig3, use_container_width=True)

    if 'MonthlyIncome' in df.columns and 'Attrition' in df.columns:
        fig4 = px.box(df, x='Attrition', y='MonthlyIncome', title="Salary vs Attrition")
        st.plotly_chart(fig4, use_container_width=True)

else:
    st.warning("Plotly not installed. Please check requirements.txt")

# ==============================
# MACHINE LEARNING MODEL
# ==============================
st.subheader("🤖 Salary Prediction Model")

if 'Age' in df.columns and 'MonthlyIncome' in df.columns:

    X = df[['Age']]
    y = df['MonthlyIncome']

    model = LinearRegression()
    model.fit(X, y)

    age = st.slider("Select Employee Age", 18, 60, 30)

    prediction = model.predict([[age]])

    st.success(f"Predicted Salary: ₹ {int(prediction[0])}")

else:
    st.warning("Required columns not found for prediction")

# ==============================
# DOWNLOAD BUTTON
# ==============================
st.subheader("📥 Download Final Dataset")

csv = df.to_csv(index=False).encode('utf-8')

st.download_button(
    label="Download Dataset",
    data=csv,
    file_name="final_analyzed_data.csv",
    mime="text/csv"
)
