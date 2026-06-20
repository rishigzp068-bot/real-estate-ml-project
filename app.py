import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Attrition Analysis Dashboard", layout="wide")

st.title("📊 Employee Attrition Analysis Dashboard")

# Upload file
uploaded_file = st.file_uploader("Upload your dataset (CSV)", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.subheader("📌 Dataset Preview")
    st.write(df.head())

    st.subheader("📌 Column Names in Dataset")
    st.write(list(df.columns))

    # -------------------------------
    # 🔧 AUTO FIX COLUMN NAMES
    # -------------------------------
    df.columns = df.columns.str.strip().str.lower()

    # Try to map correct columns automatically
    AREA_COL = None
    PRICE_COL = None
    LOCATION_COL = None

    for col in df.columns:
        if "area" in col:
            AREA_COL = col
        elif "price" in col or "salary" in col:
            PRICE_COL = col
        elif "location" in col or "city" in col:
            LOCATION_COL = col

    # -------------------------------
    # ❗ ERROR HANDLING
    # -------------------------------
    if AREA_COL is None or PRICE_COL is None or LOCATION_COL is None:
        st.error(f"❌ Missing required columns.\n\nDetected:\nArea: {AREA_COL}\nPrice: {PRICE_COL}\nLocation: {LOCATION_COL}")
        st.info("👉 Please make sure your dataset has columns like: area, price, location OR similar names.")
        st.stop()

    # -------------------------------
    # 📊 CLEANING
    # -------------------------------
    df = df.dropna()

    # -------------------------------
    # 📈 GRAPH 1: Price Distribution
    # -------------------------------
    st.subheader("📈 Price Distribution")

    fig1, ax1 = plt.subplots()
    sns.histplot(df[PRICE_COL], kde=True, ax=ax1)
    st.pyplot(fig1)

    # -------------------------------
    # 📊 GRAPH 2: Area vs Price
    # -------------------------------
    st.subheader("📊 Area vs Price")

    fig2, ax2 = plt.subplots()
    sns.scatterplot(x=df[AREA_COL], y=df[PRICE_COL], ax=ax2)
    st.pyplot(fig2)

    # -------------------------------
    # 📍 GRAPH 3: Location Count
    # -------------------------------
    st.subheader("📍 Properties by Location")

    fig3, ax3 = plt.subplots()
    df[LOCATION_COL].value_counts().head(10).plot(kind='bar', ax=ax3)
    st.pyplot(fig3)

    # -------------------------------
    # 📊 CORRELATION HEATMAP
    # -------------------------------
    st.subheader("🔥 Correlation Heatmap")

    fig4, ax4 = plt.subplots()
    sns.heatmap(df.select_dtypes(include=['number']).corr(), annot=True, cmap="coolwarm", ax=ax4)
    st.pyplot(fig4)

    # -------------------------------
    # 📥 DOWNLOAD CLEANED DATA
    # -------------------------------
    st.subheader("📥 Download Cleaned Data")

    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("Download CSV", csv, "cleaned_data.csv", "text/csv")

else:
    st.warning("⚠️ Please upload a dataset to proceed.")
