import streamlit as st
import pandas as pd

st.set_page_config(page_title="Real Estate ML Dashboard", layout="wide")

st.title("🏠 Real Estate Buyer Segmentation Dashboard")

# Upload file
uploaded_file = st.file_uploader("Upload Final Excel File", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    st.subheader("📊 Dataset Preview")
    st.dataframe(df)

    # Show columns
    st.write("Columns:", df.columns.tolist())

    # Cluster Distribution
    if 'Cluster' in df.columns:
        st.subheader("📌 Cluster Distribution")
        st.bar_chart(df['Cluster'].value_counts())

    # Income vs Age
    if 'Income' in df.columns and 'Age' in df.columns:
        st.subheader("💰 Income vs Age")
        st.scatter_chart(df[['Income', 'Age']])

    # Buyer Type
    if 'Buyer_Type' in df.columns:
        st.subheader("🧑‍💼 Buyer Type Distribution")
        st.bar_chart(df['Buyer_Type'].value_counts())

    st.success("✅ Dashboard Loaded Successfully!")
