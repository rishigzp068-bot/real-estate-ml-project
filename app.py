# =========================================================
# ✅ FINAL FIX SECTION (CLEAN + PROFESSIONAL + ERROR FREE)
# =========================================================

st.subheader("📊 Data Columns Check")
st.write(df.columns)

# ---------------------------------------------------------
# 🔴 STEP 1: SET YOUR REAL COLUMN NAMES HERE (EDIT ONLY THIS)
# ---------------------------------------------------------
AREA_COL = "area"        # 👉 change if needed (example: "property_area")
PRICE_COL = "price"      # 👉 change if needed (example: "sale_price")
LOCATION_COL = "location"  # 👉 change if needed (example: "city")

# ---------------------------------------------------------
# 🔍 STEP 2: VALIDATE COLUMNS
# ---------------------------------------------------------
missing_cols = [col for col in [AREA_COL, PRICE_COL, LOCATION_COL] if col not in df.columns]

if missing_cols:
    st.error(f"❌ Missing columns in dataset: {missing_cols}")
    st.warning("👉 Please update AREA_COL, PRICE_COL, LOCATION_COL in code")
    st.stop()

# ---------------------------------------------------------
# 🧹 STEP 3: CLEAN DATA
# ---------------------------------------------------------
df[AREA_COL] = pd.to_numeric(df[AREA_COL], errors='coerce')
df[PRICE_COL] = pd.to_numeric(df[PRICE_COL], errors='coerce')

df = df.dropna(subset=[AREA_COL, PRICE_COL])

# ---------------------------------------------------------
# 📍 STEP 4: AREA vs PRICE SCATTER
# ---------------------------------------------------------
st.subheader("📍 Area vs Price Scatter Plot")

fig1 = px.scatter(
    df,
    x=AREA_COL,
    y=PRICE_COL,
    color=LOCATION_COL,
    title="Area vs Price"
)

st.plotly_chart(fig1, use_container_width=True)

# ---------------------------------------------------------
# 📊 STEP 5: PRICE DISTRIBUTION
# ---------------------------------------------------------
st.subheader("📊 Price Distribution")

fig2, ax = plt.subplots()
sns.histplot(df[PRICE_COL], kde=True, ax=ax)
st.pyplot(fig2)

# ---------------------------------------------------------
# 📍 STEP 6: LOCATION COUNT
# ---------------------------------------------------------
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

# =========================================================
# ✅ END OF FINAL SECTION
# =========================================================
