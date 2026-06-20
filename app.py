# app.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(page_title="Real Estate ML Dashboard", layout="wide")

st.title("🏡 Real Estate Buyer Segmentation Dashboard")

# -------------------------------
# LOAD DATA
# -------------------------------
@st.cache_data
def load_data():
    df = pd.read_excel("Final_Analyzed_RealEstate_Data.xlsx")
    return df

df = load_data()

# -------------------------------
# SHOW DATA
# -------------------------------
st.subheader("📊 Dataset Preview")
st.dataframe(df.head())

st.write("Dataset Shape:", df.shape)

# Show columns (IMPORTANT for debugging)
st.write("Columns:", df.columns)

# -------------------------------
# AGE DISTRIBUTION
# -------------------------------
if 'Age' in df.columns:
    st.subheader("📌 Age Distribution")
    fig, ax = plt.subplots()
    sns.histplot(df['Age'], bins=20, kde=True, ax=ax)
    st.pyplot(fig)

# -------------------------------
# INCOME DISTRIBUTION
# -------------------------------
if 'Income' in df.columns:
    st.subheader("💰 Income Distribution")
    fig, ax = plt.subplots()
    sns.histplot(df['Income'], bins=20, kde=True, ax=ax)
    st.pyplot(fig)

# -------------------------------
# PROPERTY TYPE
# -------------------------------
if 'Property_Type' in df.columns:
    st.subheader("🏢 Property Type")
    fig, ax = plt.subplots()
    sns.countplot(x='Property_Type', data=df, ax=ax)
    plt.xticks(rotation=30)
    st.pyplot(fig)

# -------------------------------
# LOCATION
# -------------------------------
if 'Location' in df.columns:
    st.subheader("📍 Location Distribution")
    fig, ax = plt.subplots()
    sns.countplot(x='Location', data=df, ax=ax)
    plt.xticks(rotation=45)
    st.pyplot(fig)

# -------------------------------
# CLUSTER (VERY IMPORTANT)
# -------------------------------
if 'Cluster' in df.columns:
    st.subheader("🧠 Buyer Segments")
    fig, ax = plt.subplots()
    sns.countplot(x='Cluster', data=df, ax=ax)
    st.pyplot(fig)

# -------------------------------
# SCATTER (INCOME VS PRICE)
# -------------------------------
if 'Income' in df.columns and 'Property_Price' in df.columns:
    st.subheader("📈 Income vs Property Price")
    fig, ax = plt.subplots()
    sns.scatterplot(x='Income', y='Property_Price', data=df, ax=ax)
    st.pyplot(fig)

# -------------------------------
# HEATMAP
# -------------------------------
numeric_df = df.select_dtypes(include=['int64','float64'])

if not numeric_df.empty:
    st.subheader("🔥 Correlation Heatmap")
    fig, ax = plt.subplots(figsize=(10,6))
    sns.heatmap(numeric_df.corr(), annot=True, cmap='coolwarm', ax=ax)
    st.pyplot(fig)

# -------------------------------
# SUCCESS
# -------------------------------
st.success("✅ App Running Successfully!")
st.set_page_config(page_title="Real Estate ML Dashboard", layout="wide")

st.markdown("Machine Learning based analysis of real estate data")
pd.read_excel("Final_Analyzed_RealEstate_Data.xlsx")
location = st.selectbox("Select Location", df['location'].unique())
filtered_df = df[df['location'] == location]
