# app.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# -------------------------------
# PAGE SETTINGS
# -------------------------------
st.set_page_config(page_title="Real Estate ML Analysis", layout="wide")

st.title("🏡 Real Estate Buyer Segmentation & Investment Analysis")

# -------------------------------
# LOAD DATA (NO UPLOAD)
# -------------------------------
@st.cache_data
def load_data():
    df = pd.read_excel("Final_Analyzed_RealEstate_Data.xlsx")
    return df

df = load_data()

# -------------------------------
# DATA PREVIEW
# -------------------------------
st.subheader("📊 Dataset Preview")
st.dataframe(df.head())

st.write("Shape of dataset:", df.shape)

# -------------------------------
# CHECK NUMERIC COLUMNS
# -------------------------------
numeric_df = df.select_dtypes(include=['int64','float64'])

# -------------------------------
# 1. AGE DISTRIBUTION
# -------------------------------
if 'Age' in df.columns:
    st.subheader("📌 Age Distribution")
    fig, ax = plt.subplots()
    sns.histplot(df['Age'], bins=20, kde=True, ax=ax)
    st.pyplot(fig)

# -------------------------------
# 2. INCOME DISTRIBUTION
# -------------------------------
if 'Income' in df.columns:
    st.subheader("💰 Income Distribution")
    fig, ax = plt.subplots()
    sns.histplot(df['Income'], bins=20, kde=True, ax=ax)
    st.pyplot(fig)

# -------------------------------
# 3. PROPERTY TYPE COUNT
# -------------------------------
for col in ['Property_Type', 'PropertyType']:
    if col in df.columns:
        st.subheader("🏢 Property Type Distribution")
        fig, ax = plt.subplots()
        sns.countplot(x=col, data=df, ax=ax)
        plt.xticks(rotation=30)
        st.pyplot(fig)
        break

# -------------------------------
# 4. LOCATION ANALYSIS
# -------------------------------
for col in ['Location', 'Preferred_Location']:
    if col in df.columns:
        st.subheader("📍 Location Distribution")
        fig, ax = plt.subplots()
        sns.countplot(x=col, data=df, ax=ax)
        plt.xticks(rotation=45)
        st.pyplot(fig)
        break

# -------------------------------
# 5. INCOME vs PROPERTY PRICE
# -------------------------------
if 'Income' in df.columns and 'Property_Price' in df.columns:
    st.subheader("📈 Income vs Property Price")
    fig, ax = plt.subplots()
    sns.scatterplot(x='Income', y='Property_Price', data=df, ax=ax)
    st.pyplot(fig)

# -------------------------------
# 6. CLUSTER DISTRIBUTION (IMPORTANT)
# -------------------------------
for col in ['Cluster', 'cluster', 'Segment']:
    if col in df.columns:
        st.subheader("🧠 Buyer Segmentation (Clusters)")
        fig, ax = plt.subplots()
        sns.countplot(x=col, data=df, ax=ax)
        st.pyplot(fig)
        break

# -------------------------------
# 7. CORRELATION HEATMAP
# -------------------------------
if not numeric_df.empty:
    st.subheader("🔥 Correlation Heatmap")
    fig, ax = plt.subplots(figsize=(10,6))
    sns.heatmap(numeric_df.corr(), annot=True, cmap='coolwarm', ax=ax)
    st.pyplot(fig)

# -------------------------------
# 8. BOXPLOT (INCOME VS CLUSTER)
# -------------------------------
if 'Income' in df.columns:
    for col in ['Cluster', 'cluster', 'Segment']:
        if col in df.columns:
            st.subheader("📊 Income vs Cluster")
            fig, ax = plt.subplots()
            sns.boxplot(x=col, y='Income', data=df, ax=ax)
            st.pyplot(fig)
            break

# -------------------------------
# SUCCESS MESSAGE
# -------------------------------
st.success("✅ Dashboard Loaded Successfully Without Errors!")
