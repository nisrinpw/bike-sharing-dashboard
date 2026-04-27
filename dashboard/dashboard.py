
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# PAGE CONFIG
st.set_page_config(
    page_title="Bike Sharing Dashboard",
    page_icon="🚲",
    layout="wide"
)

sns.set(style="darkgrid")

# LOAD DATA
@st.cache_data
def load_data():
    df = pd.read_csv("dashboard/main_data.csv")
    df["dteday"] = pd.to_datetime(df["dteday"])
    return df

day_df = load_data()

# LABEL MAPPING
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

# SIDEBAR
with st.sidebar:
    st.title("🚲 Bike Sharing")
    st.markdown("Interactive dashboard for bike rental analysis")

    selected_season = st.multiselect(
        "Pilih Musim",
        options=day_df["season_label"].unique(),
        default=day_df["season_label"].unique()
    )

    selected_weather = st.multiselect(
        "Pilih Kondisi Cuaca",
        options=day_df["weather_label"].unique(),
        default=day_df["weather_label"].unique()
    )

# HEADER
st.title("🚲 Bike Sharing Dashboard")
st.caption(
    "Analysis of bike rentals based on weather conditions, seasons, and demand levels."
)

# FILTER
st.subheader("Filter by Date")

min_date = day_df["dteday"].min().date()
max_date = day_df["dteday"].max().date()

col1, col2 = st.columns(2)

with col1:
    start_date = st.date_input(
        "Start Date",
        value=min_date,
        min_value=min_date,
        max_value=max_date
    )

with col2:
    end_date = st.date_input(
        "End Date",
        value=max_date,
        min_value=min_date,
        max_value=max_date
    )

if start_date > end_date:
    st.error("Start Date tidak boleh lebih besar dari End Date")
    st.stop()

# FILTER DATA
main_df = day_df[
    (day_df["dteday"] >= pd.to_datetime(start_date)) &
    (day_df["dteday"] <= pd.to_datetime(end_date)) &
    (day_df["season_label"].isin(selected_season)) &
    (day_df["weather_label"].isin(selected_weather))
].copy()


main_df["demand_category"] = pd.cut(
    main_df["cnt"],
    bins=3,
    labels=["Low Demand", "Medium Demand", "High Demand"]
)

# METRICS
st.subheader("Summary Metrics")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Total Rentals",
        f"{int(main_df['cnt'].sum()):,}"
    )

with col2:
    st.metric(
        "Average Daily Rentals",
        f"{int(main_df['cnt'].mean()):,}"
    )

with col3:
    st.metric(
        "Maximum Daily Rentals",
        f"{int(main_df['cnt'].max()):,}"
    )

st.divider()

# DAILY RENTAL TREND
st.subheader("Daily Rental Trend")

fig, ax = plt.subplots(figsize=(12, 5))

sns.lineplot(
    data=main_df,
    x="dteday",
    y="cnt",
    ax=ax
)

ax.set_title("Daily Bike Rental Trend")
ax.set_xlabel("Date")
ax.set_ylabel("Total Rentals")

st.pyplot(fig)

# WEATHER + SEASON + WORKING DAY
col1, col2, col3 = st.columns(3)

# WEATHER
with col1:
    st.subheader("Bike Rentals by Weather")

    fig, ax = plt.subplots(figsize=(6, 4))

    sns.barplot(
        data=main_df,
        x="weather_label",
        y="cnt",
        palette="Blues",
        ax=ax
    )

    ax.set_xlabel("Weather")
    ax.set_ylabel("Avg Rentals")

    st.pyplot(fig)


# SEASON
with col2:
    st.subheader("Bike Rentals by Season")

    fig, ax = plt.subplots(figsize=(6, 4))

    sns.barplot(
        data=main_df,
        x="season_label",
        y="cnt",
        palette="Greens",
        ax=ax
    )

    ax.set_xlabel("Season")
    ax.set_ylabel("Avg Rentals")

    st.pyplot(fig)


# WORKING DAY
with col3:
    workingday_labels = {
        0: "Holiday",
        1: "Working Day"
    }

    main_df["workingday_label"] = main_df["workingday"].map(workingday_labels)

    st.subheader("Bike Rentals by Day Type")

    fig, ax = plt.subplots(figsize=(6, 4))

    sns.barplot(
        data=main_df,
        x="workingday_label",
        y="cnt",
        palette="Purples",
        ax=ax
    )

    ax.set_xlabel("Day Type")
    ax.set_ylabel("Avg Rentals")

    st.pyplot(fig)

# MONTHLY RENTAL TREND
month_labels = {
    1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr",
    5: "May", 6: "Jun", 7: "Jul", 8: "Aug",
    9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"
}

main_df["month_label"] = main_df["mnth"].map(month_labels)

st.subheader("Monthly Rental Trend")

fig, ax = plt.subplots(figsize=(10, 5))

sns.barplot(
    data=main_df,
    x="month_label",
    y="cnt",
    palette="crest",
    ax=ax
)

ax.set_xlabel("Month")
ax.set_ylabel("Average Rentals")
ax.set_title("Average Bike Rentals by Month")

st.pyplot(fig)

# DEMAND CATEGORY
st.subheader("Demand Category Distribution")

fig, ax = plt.subplots(figsize=(8, 5))

sns.countplot(
    data=main_df,
    x="demand_category",
    palette="Oranges",
    ax=ax
)

ax.set_xlabel("Demand Category")
ax.set_ylabel("Total Days")
ax.set_title("Bike Rental Demand Category")

st.pyplot(fig)

# CORRELATION HEATMAP
st.subheader("Correlation Heatmap")

corr_columns = [
    "temp",
    "atemp",
    "hum",
    "windspeed",
    "cnt"
]

corr_matrix = main_df[corr_columns].corr()

fig, ax = plt.subplots(figsize=(8, 6))

sns.heatmap(
    corr_matrix,
    annot=True,
    cmap="Blues",
    fmt=".2f",
    linewidths=0.5,
    ax=ax
)

ax.set_title("Correlation Between Variables")

st.pyplot(fig)

# INSIGHT
st.subheader("Key Insights")

st.info("""
• Clear weather results in the highest bike rentals

• Fall season shows the highest average rentals

• Most days fall into the Medium Demand category

• Working days tend to have slightly higher rentals
""")


st.caption("Created using Python, Streamlit, and Bike Sharing Dataset")
