# -------------------------------
# AUTO DETECT COLUMNS
# -------------------------------
st.subheader("🔍 Detecting Columns")

st.write("Available columns:", df.columns)

# Try to guess columns
area_col = None
price_col = None
location_col = None

for col in df.columns:
    if "area" in col:
        area_col = col
    if "price" in col:
        price_col = col
    if "location" in col or "city" in col:
        location_col = col

st.write("Detected Area Column:", area_col)
st.write("Detected Price Column:", price_col)
st.write("Detected Location Column:", location_col)

# -------------------------------
# AREA vs PRICE
# -------------------------------
st.subheader("📍 Area vs Price Scatter Plot")

if area_col and price_col:
    df[area_col] = pd.to_numeric(df[area_col], errors="coerce")
    df[price_col] = pd.to_numeric(df[price_col], errors="coerce")

    plot_df = df.dropna(subset=[area_col, price_col])

    if not plot_df.empty:
        fig = px.scatter(
            plot_df,
            x=area_col,
            y=price_col,
            color=location_col if location_col else None,
            title="Area vs Price"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No valid data for plotting")
else:
    st.error("Could not detect area/price columns")

# -------------------------------
# PRICE DISTRIBUTION
# -------------------------------
st.subheader("📊 Price Distribution")

if price_col:
    fig, ax = plt.subplots()
    sns.histplot(df[price_col], kde=True, ax=ax)
    st.pyplot(fig)
else:
    st.error("Price column not found")

# -------------------------------
# LOCATION GRAPH
# -------------------------------
st.subheader("📍 Properties by Location")

if location_col:
    loc_df = df[location_col].value_counts().reset_index()
    loc_df.columns = ["Location", "Count"]

    fig = px.bar(loc_df, x="Location", y="Count", title="Properties per Location")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.error("Location column not found")
