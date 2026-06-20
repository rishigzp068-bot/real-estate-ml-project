# =========================================
# IMPORT LIBRARIES
# =========================================
import streamlit as st
import pandas as pd
import plotly.express as px
import joblib
import os

# =========================================
# PAGE CONFIG
# =========================================
st.set_page_config(page_title="Real Estate Dashboard", layout="wide")

st.title("🏠 Real Estate Market Intelligence Dashboard")

# =========================================
# FILE UPLOAD
# =========================================
uploaded_file = st.file_uploader("📂 Upload Final Excel Dataset", type=["xlsx"])

if uploaded_file is not None:

    try:
        df = pd.read_excel(uploaded_file)

        st.success("✅ File loaded successfully!")

        # =========================================
        # SHOW DATA
        # =========================================
        st.subheader("📊 Dataset Preview")
        st.dataframe(df.head())

        st.write("Columns:", df.columns.tolist())

        # =========================================
        # SIDEBAR FILTER
        # =========================================
        st.sidebar.header("🔍 Filters")

        if 'Cluster' in df.columns:
            selected_cluster = st.sidebar.multiselect(
                "Select Cluster",
                options=df['Cluster'].unique(),
                default=df['Cluster'].unique()
            )
            df = df[df['Cluster'].isin(selected_cluster)]

        # =========================================
        # KPI METRICS
        # =========================================
        st.markdown("### 📌 Key Metrics")

        col1, col2, col3 = st.columns(3)

        col1.metric("Total Records", len(df))

        if 'Income' in df.columns:
            col2.metric("Avg Income", round(df['Income'].mean(), 2))

        if 'Price' in df.columns:
            col3.metric("Avg Price", round(df['Price'].mean(), 2))

        st.markdown("---")

        # =========================================
        # CHARTS
        # =========================================
        col1, col2 = st.columns(2)

        # Cluster Chart
        with col1:
            if 'Cluster' in df.columns:
                fig = px.histogram(df, x='Cluster', title="Cluster Distribution")
                st.plotly_chart(fig, use_container_width=True)

        # Buyer Type Chart
        with col2:
            if 'Buyer_Type' in df.columns:
                fig = px.pie(df, names='Buyer_Type', title="Buyer Type Distribution")
                st.plotly_chart(fig, use_container_width=True)

        # Scatter Plot
        if 'Income' in df.columns and 'Price' in df.columns:
            st.subheader("💰 Income vs Price")
            fig = px.scatter(df, x='Income', y='Price', color='Cluster' if 'Cluster' in df.columns else None)
            st.plotly_chart(fig, use_container_width=True)

        # Box Plot
        if 'Cluster' in df.columns and 'Income' in df.columns:
            st.subheader("📦 Income Distribution by Cluster")
            fig = px.box(df, x='Cluster', y='Income')
            st.plotly_chart(fig, use_container_width=True)

        # =========================================
        # PRICE PREDICTION
        # =========================================
        st.sidebar.header("💰 Price Prediction")

        model_path = "price_model.pkl"

        if os.path.exists(model_path):

            model = joblib.load(model_path)

            income = st.sidebar.number_input("Enter Income", value=50000)
            age = st.sidebar.number_input("Enter Age", value=30)

            if st.sidebar.button("Predict Price"):
                prediction = model.predict([[income, age]])
                st.sidebar.success(f"Estimated Price: {round(prediction[0], 2)}")

        else:
            st.sidebar.warning("⚠️ Model file not found (price_model.pkl)")

    except Exception as e:
        st.error(f"❌ Error: {e}")

else:
    st.info("📂 Please upload your final Excel file to continue.")
