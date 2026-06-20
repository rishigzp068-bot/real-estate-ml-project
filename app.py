import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Real Estate Dashboard", layout="wide")

st.title("🏠 Real Estate Dashboard")

# =========================
# FILE UPLOAD
# =========================
file = st.file_uploader("Upload Excel File", type=["xlsx"])

if file is not None:
    try:
        df = pd.read_excel(file)

        st.success("✅ File Loaded")

        # Show data
        st.write("### Preview")
        st.dataframe(df.head())

        # =========================
        # BASIC INFO
        # =========================
        st.write("### Columns")
        st.write(df.columns.tolist())

        # =========================
        # SAFE COLUMN DETECTION
        # =========================
        income_col = None
        price_col = None
        cluster_col = None
        buyer_col = None
        age_col = None

        for col in df.columns:
            if "income" in col.lower():
                income_col = col
            if "price" in col.lower():
                price_col = col
            if "cluster" in col.lower():
                cluster_col = col
            if "buyer" in col.lower():
                buyer_col = col
            if "age" in col.lower():
                age_col = col

        # =========================
        # METRICS
        # =========================
        st.write("### 📊 Metrics")
        col1, col2, col3 = st.columns(3)

        col1.metric("Total Rows", len(df))

        if income_col:
            col2.metric("Avg Income", round(df[income_col].mean(), 2))

        if price_col:
            col3.metric("Avg Price", round(df[price_col].mean(), 2))

        # =========================
        # CHARTS
        # =========================
        st.write("### 📈 Charts")

        # Cluster Chart
        if cluster_col:
            fig = px.histogram(df, x=cluster_col, title="Cluster Distribution")
            st.plotly_chart(fig)

        # Buyer Type
        if buyer_col:
            fig = px.pie(df, names=buyer_col, title="Buyer Type")
            st.plotly_chart(fig)

        # Scatter
        if income_col and price_col:
            fig = px.scatter(df, x=income_col, y=price_col, title="Income vs Price")
            st.plotly_chart(fig)

        # Box
        if cluster_col and income_col:
            fig = px.box(df, x=cluster_col, y=income_col, title="Income by Cluster")
            st.plotly_chart(fig)

    except Exception as e:
        st.error(f"Error: {e}")

else:
    st.info("Please upload your Excel file")
