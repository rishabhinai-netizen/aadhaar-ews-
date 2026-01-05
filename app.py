import streamlit as st
import pandas as pd
import plotly.express as px
import json

# --------------------------------------------------
# Page Config
# --------------------------------------------------
st.set_page_config(
    page_title="Aadhaar EWS – National Monitoring",
    layout="wide"
)

# --------------------------------------------------
# Load Data
# --------------------------------------------------
@st.cache_data
def load_ews_data():
    return pd.read_csv("data/ews_weekly_district.csv", parse_dates=["week"])

@st.cache_data
def load_geo_cleaning():
    return pd.read_csv("data/geo_cleaning_summary.csv")

ews_df = load_ews_data()
geo_df = load_geo_cleaning()

# --------------------------------------------------
# Title
# --------------------------------------------------
st.title("Aadhaar Early Warning System (EWS)")
st.caption(
    "A PIN-validated, district-level monitoring system for proactive "
    "Aadhaar enrolment and update risk detection."
)

# --------------------------------------------------
# Sidebar Filters
# --------------------------------------------------
st.sidebar.header("Filters")

weeks = sorted(ews_df["week"].dt.strftime("%Y-%m-%d").unique(), reverse=True)
states = ["All"] + sorted(ews_df["state"].unique())

selected_week = st.sidebar.selectbox("Select Week", weeks)
selected_state = st.sidebar.selectbox("Select State", states)

filtered_df = ews_df[ews_df["week"].dt.strftime("%Y-%m-%d") == selected_week]

if selected_state != "All":
    filtered_df = filtered_df[filtered_df["state"] == selected_state]

# --------------------------------------------------
# Navigation
# --------------------------------------------------
page = st.sidebar.radio(
    "Navigate",
    [
        "National Overview",
        "Early Warning Signals",
        "Geospatial Risk Map",
        "District Deep Dive",
        "Data Quality & Geo Cleaning",
        "Methodology & Ethics"
    ]
)

# --------------------------------------------------
# Page 1: National Overview
# --------------------------------------------------
if page == "National Overview":
    st.subheader("National Health Snapshot")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Districts Monitored", filtered_df["district"].nunique())
    col2.metric("Stable", (filtered_df["risk_category"] == "Stable").sum())
    col3.metric("Watchlist", (filtered_df["risk_category"] == "Watchlist").sum())
    col4.metric("Emerging Risk", (filtered_df["risk_category"] == "Emerging Risk").sum())

    st.info(
        "No critical national anomalies detected for the selected week. "
        "However, several districts show rising biometric volatility "
        "and are under early warning."
    )

# --------------------------------------------------
# Page 2: Early Warning Signals
# --------------------------------------------------
elif page == "Early Warning Signals":
    st.subheader("Trending Risk Districts")

    table = (
        filtered_df
        .sort_values("severity_trend", ascending=False)
        [["state", "district", "risk_category", "severity_trend", "dominant_signal"]]
        .head(15)
    )

    st.dataframe(table, use_container_width=True)

# --------------------------------------------------
# Page 3: Geospatial Risk Map
# --------------------------------------------------
elif page == "Geospatial Risk Map":
    st.subheader("District-Level Risk Map")

    with open("assets/india_districts.geojson", "r") as f:
        geojson = json.load(f)

    fig = px.choropleth(
        filtered_df,
        geojson=geojson,
        featureidkey="properties.district",
        locations="district",
        color="risk_category",
        hover_data={
            "state": True,
            "severity_score": ":.2f",
            "dominant_signal": True
        },
        category_orders={
            "risk_category": ["Stable", "Watchlist", "Emerging Risk", "Critical"]
        },
        color_discrete_map={
            "Stable": "#2ecc71",
            "Watchlist": "#f1c40f",
            "Emerging Risk": "#e67e22",
            "Critical": "#e74c3c"
        }
    )

    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(height=650, margin={"r":0,"t":0,"l":0,"b":0})

    st.plotly_chart(fig, use_container_width=True)

# --------------------------------------------------
# Page 4: District Deep Dive
# --------------------------------------------------
elif page == "District Deep Dive":
    st.subheader("District Deep Dive")

    districts = sorted(filtered_df["district"].unique())
    district = st.selectbox("Select District", districts)

    df_d = ews_df[
        (ews_df["district"] == district) &
        (ews_df["state"] == filtered_df["state"].iloc[0])
    ].sort_values("week")

    st.line_chart(df_d.set_index("week")[["severity_score"]])

    st.write("**Dominant Signal:**", df_d["dominant_signal"].iloc[-1])

# --------------------------------------------------
# Page 5: Geo Cleaning
# --------------------------------------------------
elif page == "Data Quality & Geo Cleaning":
    st.subheader("Geospatial Standardisation Impact")
    st.dataframe(geo_df, use_container_width=True)

# --------------------------------------------------
# Page 6: Methodology & Ethics
# --------------------------------------------------
elif page == "Methodology & Ethics":
    st.markdown(
        """
        **Methodology**
        - Weekly district-level aggregation
        - PIN-based geo canonicalisation
        - Trend-based severity scoring
        - Explainable early warning logic

        **Ethics & Privacy**
        - Aggregated and anonymised data
        - No personal identifiers
        - Designed for preventive governance
        """
    )
