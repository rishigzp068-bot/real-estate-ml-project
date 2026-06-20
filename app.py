# ==============================
# IMPORT LIBRARIES
# ==============================
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.linear_model import LinearRegression

# ==============================
# PAGE CONFIG
# ==============================
st.set_page_config(page_title="Employee Attrition Analysis", layout="wide")

st.title("📊 Employee Attrition Analysis Dashboard")

# ==============================
# FILE UPLOAD
# ==============================
uploaded_file = st.file_uploader("Upload your dataset (CSV file)", type=["csv"])

if uploaded_file is not None:

    # ==============================
    # LOAD DATA
    # ==============================
    df = pd.read_csv(uploaded_file)

    st.subheader("Raw Dataset")
    st.write(df.head())

    # ==============================
    # DATA CLEANING
    # ==============================
    df.drop_duplicates(inplace=True)

    # Fill missing values
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

    if 'MonthlyIncome' in df.columns:
        df['IncomeLevel'] = pd.qcut(
            df['MonthlyIncome'],
            q=4,
            labels=['Low', 'Medium', 'High', 'Very High']
        )

    # ==============================
    # KPI METRICS
    # ==============================
    st.subheader("📌 Key Metrics")

    col1, col2, col3 = st.columns(3)

    if 'Attrition' in df.columns:
        attrition_rate = (df['Attrition'].value_counts(normalize=True).get('Yes', 0)) * 100
    else:
        attrition_rate = 0

    col1.metric("Total Employees", len(df))
    col2.metric("Attrition Rate", f"{attrition_rate:.2f}%")
    col3.metric("Avg Salary", int(df['MonthlyIncome'].mean()) if 'MonthlyIncome' in df.columns else 0)

    # ==============================
    # CHARTS (PLOTLY)
    # ==============================
    st.subheader("📊 Visual Analysis")

    if 'Department' in df.columns:
        fig1 = px.bar(df, x='Department', title="Employees by Department")
        st.plotly_chart(fig1, use_container_width=True)

    if 'Attrition' in df.columns:
        fig2 = px.pie(df, names='Attrition', title="Attrition Distribution")
        st.plotly_chart(fig2, use_container_width=True)

    if 'AgeGroup' in df.columns:
        fig3 = px.histogram(df, x='AgeGroup', title="Age Group Distribution")
        st.plotly_chart(fig3, use_container_width=True)

    if 'MonthlyIncome' in df.columns:
        fig4 = px.box(df, x='Attrition', y='MonthlyIncome', title="Salary vs Attrition")
        st.plotly_chart(fig4, use_container_width=True)

    # ==============================
    # PREDICTION MODEL
    # ==============================
    st.subheader("🤖 Salary Prediction Model")

    if 'Age' in df.columns and 'MonthlyIncome' in df.columns:

        X = df[['Age']]
        y = df['MonthlyIncome']

        model = LinearRegression()
        model.fit(X, y)

        age_input = st.slider("Select Age", 18, 60, 30)

        prediction = model.predict([[age_input]])

        st.success(f"Predicted Salary: ₹ {int(prediction[0])}")

    # ==============================
    # DOWNLOAD ANALYZED DATA
    # ==============================
    st.subheader("📥 Download Final Analyzed Dataset")

    csv = df.to_csv(index=False).encode('utf-8')

    st.download_button(
        label="Download CSV",
        data=csv,
        file_name="final_analyzed_dataset.csv",
        mime='text/csv',
    )

else:
    st.warning("Please upload a dataset to continue.")
