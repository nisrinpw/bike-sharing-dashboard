
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Page Config
st.set_page_config(
    page_title="Bike Sharing Dashboard",
    page_icon="🚲",
    layout="wide"
)

sns.set(style="darkgrid")

# Load Data
@st.cache_data
def load_data():
    df = pd.read_csv("dashboard/main_data.csv")
    return df

day_df = load_data()

# Mapping Label
weather_labels = {
    1: "Clear Weather",
    2: "Misty",
    3: "Light Rain/Snow",
    4: "Heavy Rain"
}

season_labels = {
    1: "Spring",
    2: "Summer",
    3: "Fall",
    4: "Winter"
}

day_df["weather_label"] = day_df["weathersit"].map(weather_labels)
day_df["season_label"] = day_df["season"].map(season_labels)

# Sidebar Filter
st.sidebar.header("Filter Data")

selected_season = st.sidebar.multiselect(
    "Pilih Musim",
    options=day_df["season_label"].unique(),
    default=day_df["season_label"].unique()
)

selected_weather = st.sidebar.multiselect(
    "Pilih Kondisi Cuaca",
    options=day_df["weather_label"].unique(),
    default=day_df["weather_label"].unique()
)

# Filtering Data
main_df = day_df[
    (day_df["season_label"].isin(selected_season)) &
    (day_df["weather_label"].isin(selected_weather))
]

# Header
st.title("🚲 Bike Sharing Dashboard")
st.markdown("Analisis penyewaan sepeda berdasarkan kondisi cuaca, musim, dan tingkat permintaan.")

# Metrics
col1, col2, col3 = st.columns(3)

with col1:
    total_rentals = int(main_df["cnt"].sum())
    st.metric("Total Rentals", value=f"{total_rentals:,}")

with col2:
    avg_rentals = int(main_df["cnt"].mean())
    st.metric("Average Daily Rentals", value=f"{avg_rentals:,}")

with col3:
    max_rentals = int(main_df["cnt"].max())
    st.metric("Maximum Daily Rentals", value=f"{max_rentals:,}")

st.divider()

# Visualization 1
st.subheader("Average Bike Rentals by Weather Condition")

fig, ax = plt.subplots(figsize=(8,5))
sns.barplot(
    data=main_df,
    x="weather_label",
    y="cnt",
    ax=ax
)

ax.set_xlabel("Weather Condition")
ax.set_ylabel("Average Total Rentals")
ax.set_title("Bike Rentals by Weather")

st.pyplot(fig)

# Visualization 2
st.subheader("Average Bike Rentals by Season")

fig, ax = plt.subplots(figsize=(8,5))
sns.barplot(
    data=main_df,
    x="season_label",
    y="cnt",
    ax=ax
)

ax.set_xlabel("Season")
ax.set_ylabel("Average Total Rentals")
ax.set_title("Bike Rentals by Season")

st.pyplot(fig)

# Clustering (Demand Category)
st.subheader("Demand Category Distribution")

main_df = main_df.copy()

main_df["demand_category"] = pd.cut(
    main_df["cnt"],
    bins=3,
    labels=["Low Demand", "Medium Demand", "High Demand"]
)

fig, ax = plt.subplots(figsize=(8,5))
sns.countplot(
    data=main_df,
    x="demand_category",
    ax=ax
)

ax.set_xlabel("Demand Category")
ax.set_ylabel("Total Days")
ax.set_title("Bike Rental Demand Category")

st.pyplot(fig)

st.divider()

# Insight
st.subheader("Key Insights")

st.markdown("""
- Cuaca cerah memiliki rata-rata penyewaan sepeda tertinggi.
- Musim gugur menunjukkan jumlah penyewaan tertinggi dibanding musim lainnya.
- Sebagian besar hari berada pada kategori *Medium Demand*.
- Hari kerja memiliki jumlah penyewaan sedikit lebih tinggi dibanding hari libur.
""")

st.caption("Copyright © Dicoding Submission - Bike Sharing Analysis")
