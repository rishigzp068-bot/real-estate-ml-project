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
st.markdown("Analysis of Real Estate Dataset using Machine Learning")

# -------------------------------
# LOAD DATA (NO UPLOAD BUTTON)
# -------------------------------
df = pd.read_excel("Final_Analyzed_RealEstate_Data.xlsx")

# -------------------------------
# CLEAN COLUMN NAMES (IMPORTANT)
# -------------------------------
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

# -------------------------------
# SHOW DATA
# -------------------------------
st.subheader("📊 Dataset Preview")
st.dataframe(df.head())

st.write("Columns in dataset:", df.columns)

# -------------------------------
# BASIC KPIs
# -------------------------------
st.subheader("📈 Key Metrics")

col1, col2, col3 = st.columns(3)

if "price" in df.columns:
    col1.metric("Average Price", f"{df['price'].mean():,.0f}")
    col2.metric("Max Price", f"{df['price'].max():,.0f}")
    col3.metric("Min Price", f"{df['price'].min():,.0f}")
else:
    st.warning("Column 'price' not found in dataset")

# -------------------------------
# CORRELATION HEATMAP
# -------------------------------
st.subheader("🔥 Correlation Heatmap")

numeric_df = df.select_dtypes(include=['number'])

if not numeric_df.empty:
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(numeric_df.corr(), annot=True, cmap='coolwarm', ax=ax)
    st.pyplot(fig)
else:
    st.warning("No numeric columns found for heatmap")

# -------------------------------
# AREA vs PRICE (PLOTLY SAFE)
# -------------------------------
st.subheader("📍 Area vs Price Scatter Plot")

# Convert safely
if "area" in df.columns:
    df["area"] = pd.to_numeric(df["area"], errors="coerce")

if "price" in df.columns:
    df["price"] = pd.to_numeric(df["price"], errors="coerce")

# Drop missing
plot_df = df.dropna(subset=["area", "price"]) if all(col in df.columns for col in ["area", "price"]) else pd.DataFrame()

if not plot_df.empty:
    fig = px.scatter(
        plot_df,
        x="area",
        y="price",
        color="location" if "location" in plot_df.columns else None,
        title="Area vs Price"
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("Required columns ('area', 'price') not found or empty")

# -------------------------------
# PRICE DISTRIBUTION
# -------------------------------
st.subheader("📊 Price Distribution")

if "price" in df.columns:
    fig, ax = plt.subplots()
    sns.histplot(df["price"], kde=True, ax=ax)
    st.pyplot(fig)
else:
    st.warning("Column 'price' not found")

# -------------------------------
# LOCATION COUNT
# -------------------------------
st.subheader("📍 Properties by Location")

if "location" in df.columns:
    fig = px.bar(
        df["location"].value_counts().reset_index(),
        x="location",
        y="count",
        labels={"location": "Location", "count": "Number of Properties"},
        title="Properties per Location"
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("Column 'location' not found")

# -------------------------------
# FOOTER
# -------------------------------
st.markdown("---")
st.markdown("✅ Developed using Streamlit | Machine Learning Project")
