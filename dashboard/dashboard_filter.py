import streamlit as st
import pandas as pd
from pathlib import Path

st.title("Sales Dashboard with Search and Filters")

BASE_DIR = Path(__file__).resolve().parent.parent
data_path = BASE_DIR / "data" / "sales.csv"

@st.cache_data
def load_data():
    return pd.read_csv(data_path, parse_dates=["date"])

df = load_data()

st.sidebar.header("Filter Options")

region = st.sidebar.selectbox(
    "Select Region",
    options=["All"] + sorted(df["region"].unique())
)

if region != "All":
    df = df[df["region"] == region]

product = st.sidebar.selectbox(
    "Select Product",
    options=["All"] + sorted(df["product"].unique())
)

if product != "All":
    df = df[df["product"] == product]

units_range = st.sidebar.slider(
    "Units Sold",
    int(df["units_sold"].min()),
    int(df["units_sold"].max()),
    value=(int(df["units_sold"].min()), int(df["units_sold"].max()))
)

df = df[
    (df["units_sold"] >= units_range[0]) &
    (df["units_sold"] <= units_range[1])
]

search_term = st.sidebar.text_input("Search Product Name")

if search_term:
    df = df[df["product"].str.contains(search_term, case=False, na=False)]

st.subheader("Filtered Results")
st.dataframe(df)

st.subheader("Revenue Over Time")

if not df.empty:
    revenue_by_date = df.groupby("date")["revenue"].sum().reset_index()
    st.line_chart(
        revenue_by_date
        .rename(columns={"date": "index"})
        .set_index("index")
    )
else:
    st.warning("No data available for the selected filters.")
