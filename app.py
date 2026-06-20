# app.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Page config
st.set_page_config(page_title="Employee Attrition Analysis", layout="wide")

st.title("📊 Employee Attrition Analysis Dashboard")

# Load your FINAL analyzed Excel file
# Make sure file is in same folder as app.py
df = pd.read_excel("Final_Analyzed_Data.xlsx")

# Show dataset
st.subheader("Dataset Preview")
st.dataframe(df.head())

# -------------------------------
# ATTRITION COUNT
# -------------------------------
st.subheader("Attrition Count")

fig1, ax1 = plt.subplots()
sns.countplot(x='Attrition', data=df, ax=ax1)
st.pyplot(fig1)

# -------------------------------
# ATTRITION BY DEPARTMENT
# -------------------------------
st.subheader("Attrition by Department")

fig2, ax2 = plt.subplots()
sns.countplot(x='Department', hue='Attrition', data=df, ax=ax2)
plt.xticks(rotation=30)
st.pyplot(fig2)

# -------------------------------
# AGE DISTRIBUTION
# -------------------------------
st.subheader("Age Distribution")

fig3, ax3 = plt.subplots()
sns.histplot(df['Age'], bins=20, kde=True, ax=ax3)
st.pyplot(fig3)

# -------------------------------
# SALARY VS ATTRITION
# -------------------------------
st.subheader("Monthly Income vs Attrition")

fig4, ax4 = plt.subplots()
sns.boxplot(x='Attrition', y='MonthlyIncome', data=df, ax=ax4)
st.pyplot(fig4)

# -------------------------------
# JOB SATISFACTION
# -------------------------------
st.subheader("Job Satisfaction Distribution")

fig5, ax5 = plt.subplots()
sns.countplot(x='JobSatisfaction', data=df, ax=ax5)
st.pyplot(fig5)

# -------------------------------
# CORRELATION HEATMAP
# -------------------------------
st.subheader("Correlation Heatmap")

fig6, ax6 = plt.subplots(figsize=(10,6))
sns.heatmap(df.corr(numeric_only=True), annot=True, cmap='coolwarm', ax=ax6)
st.pyplot(fig6)

st.success("✅ Dashboard Loaded Successfully!")
