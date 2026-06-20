import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(page_title="Real Estate Dashboard", layout="wide")

st.title("🏠 Real Estate Price Prediction Dashboard")
st.markdown("Real Estate Data Analysis using Machine Learning")

# -------------------------------
# LOAD DATA
# -------------------------------
df = pd.read_excel("Final_Analyzed_RealEstate_Data.xlsx")

# -------------------------------
# CLEAN COLUMN NAMES
# -------------------------------
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

# -------------------------------
# SHOW DATA
# -------------------------------
st.subheader("📊 Dataset Preview")
st.dataframe(df.head())

st.subheader("📋 Available Columns")
st.write(df.columns)

# =========================================================
# 🔴 SET YOUR ACTUAL COLUMN NAMES HERE (VERY IMPORTANT)
# =========================================================
AREA_COL = "area"        # 👉 CHANGE if needed
PRICE_COL = "price"      # 👉 CHANGE if needed
LOCATION_COL = "location"  # 👉 CHANGE if needed

# =========================================================
# VALIDATE COLUMNS
# =========================================================
missing_cols = [col for col in [AREA_COL, PRICE_COL, LOCATION_COL] if col not in df.columns]

if missing_cols:
    st.error(f"❌ Missing columns in dataset: {missing_cols}")
    st.warning("👉 Please update AREA_COL, PRICE_COL, LOCATION_COL in app.py")
    st.stop()

# =========================================================
# CLEAN DATA
# =========================================================
df[AREA_COL] = pd.to_numeric(df[AREA_COL], errors='coerce')
df[PRICE_COL] = pd.to_numeric(df[PRICE_COL], errors='coerce')

df = df.dropna(subset=[AREA_COL, PRICE_COL])

# -------------------------------
# 📈 KPIs
# -------------------------------
st.subheader("📈 Key Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("Average Price", f"{df[PRICE_COL].mean():,.0f}")
col2.metric("Max Price", f"{df[PRICE_COL].max():,.0f}")
col3.metric("Min Price", f"{df[PRICE_COL].min():,.0f}")

# -------------------------------
# 🔥 CORRELATION HEATMAP
# -------------------------------
st.subheader("🔥 Correlation Heatmap")

numeric_df = df.select_dtypes(include=['number'])

fig, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(numeric_df.corr(), annot=True, cmap='coolwarm', ax=ax)
st.pyplot(fig)

# -------------------------------
# 📍 AREA vs PRICE
# -------------------------------
st.subheader("📍 Area vs Price Scatter Plot")

fig1 = px.scatter(
    df,
    x=AREA_COL,
    y=PRICE_COL,
    color=LOCATION_COL,
    title="Area vs Price"
)

st.plotly_chart(fig1, use_container_width=True)

# -------------------------------
# 📊 PRICE DISTRIBUTION
# -------------------------------
st.subheader("📊 Price Distribution")

fig2, ax = plt.subplots()
sns.histplot(df[PRICE_COL], kde=True, ax=ax)
st.pyplot(fig2)

# -------------------------------
# 📍 LOCATION COUNT
# -------------------------------
st.subheader("📍 Properties by Location")

loc_df = df[LOCATION_COL].value_counts().reset_index()
loc_df.columns = ["Location", "Count"]

fig3 = px.bar(
    loc_df,
    x="Location",
    y="Count",
    title="Properties per Location"
)

st.plotly_chart(fig3, use_container_width=True)

# -------------------------------
# FOOTER
# -------------------------------
st.markdown("---")
st.markdown("✅ Developed using Streamlit | ML Project")
