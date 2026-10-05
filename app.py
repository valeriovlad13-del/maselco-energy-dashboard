import pandas as pd
import plotly.express as px
import streamlit as st
from pathlib import Path

st.set_page_config(page_title="MASELCO Energy Data Analysis Dashboard", page_icon="⚡", layout="wide")

DATA_PATH = Path(__file__).parent / "data" / "maselco_energy_data.csv"

@st.cache_data
def load_data():
    return pd.read_csv(DATA_PATH)

df = load_data()

st.title("⚡ MASELCO Energy Data Analysis Dashboard")
st.caption("DOE-published data for the Masbate Electric Cooperative (MASELCO). Actual and forecast values are explicitly separated.")

st.sidebar.header("Filters")
years = sorted(df["year"].unique())
selected_years = st.sidebar.multiselect("Year", years, default=years)
selected_status = st.sidebar.multiselect("Data status", sorted(df["data_status"].unique()), default=sorted(df["data_status"].unique()))
filtered = df[df["year"].isin(selected_years) & df["data_status"].isin(selected_status)].copy()

st.subheader("MASELCO Overview")
actual_2022 = df[(df["year"] == 2022) & (df["data_status"] == "Actual")]
customer_rows = actual_2022[(actual_2022["dataset"] == "sector_profile") & (actual_2022["metric"] == "Captive Customers")]
sales_rows = actual_2022[(actual_2022["dataset"] == "sector_profile") & (actual_2022["metric"] == "Energy Sales")]
peak_rows = actual_2022[(actual_2022["dataset"] == "demand_profile") & (actual_2022["metric"] == "Peak Demand")]

total_customers = customer_rows["value"].sum()
total_sales = sales_rows["value"].sum()
peak_demand = peak_rows["value"].iloc[0] if not peak_rows.empty else None
forecast_rows = df[(df["dataset"] == "demand_profile") & (df["metric"] == "Peak Demand") & (df["data_status"] == "Forecast")].sort_values("year")
forecast_2032 = forecast_rows.iloc[-1]["value"] if not forecast_rows.empty else None

c1, c2, c3, c4 = st.columns(4)
c1.metric("2022 Captive Customers", f"{total_customers:,.0f}")
c2.metric("2022 Energy Sales", f"{total_sales:,.0f} MWh")
c3.metric("2022 Peak Demand", f"{peak_demand:.1f} MW")
c4.metric("2032 Forecast Peak Demand", f"{forecast_2032:.1f} MW")

st.subheader("2022 Sector Profile")
sector = actual_2022[actual_2022["dataset"] == "sector_profile"].copy()
customers = sector[sector["metric"] == "Captive Customers"][["sector", "value"]].rename(columns={"value": "customers"})
sales = sector[sector["metric"] == "Energy Sales"][["sector", "value"]].rename(columns={"value": "sales_mwh"})
sector_summary = customers.merge(sales, on="sector")
sector_summary["customer_share_pct"] = sector_summary["customers"] / sector_summary["customers"].sum() * 100
sector_summary["sales_share_pct"] = sector_summary["sales_mwh"] / sector_summary["sales_mwh"].sum() * 100
sector_summary["mwh_per_customer"] = sector_summary["sales_mwh"] / sector_summary["customers"]

left, right = st.columns(2)
with left:
    fig = px.bar(sector_summary, x="sector", y="customers", title="Captive Customers by Sector", labels={"sector": "Sector", "customers": "Customers"}, text_auto=".0f")
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
with right:
    fig = px.bar(sector_summary, x="sector", y="sales_mwh", title="Energy Sales by Sector", labels={"sector": "Sector", "sales_mwh": "Energy Sales (MWh)"}, text_auto=".0f")
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

st.dataframe(sector_summary.style.format({"customers": "{:,.0f}", "sales_mwh": "{:,.0f}", "customer_share_pct": "{:.1f}%", "sales_share_pct": "{:.1f}%", "mwh_per_customer": "{:.2f}"}), use_container_width=True)

st.subheader("Peak Demand: 2022 Actual and 2023–2032 Forecast")
demand = df[(df["dataset"] == "demand_profile") & (df["metric"] == "Peak Demand")].sort_values("year")
fig = px.line(demand, x="year", y="value", markers=True, color="data_status", title="MASELCO Peak Demand", labels={"year": "Year", "value": "Peak Demand (MW)", "data_status": "Status"})
st.plotly_chart(fig, use_container_width=True)

if peak_demand and forecast_2032:
    growth_pct = (forecast_2032 - peak_demand) / peak_demand * 100
    st.info(f"Peak demand is projected to increase from {peak_demand:.1f} MW in 2022 to {forecast_2032:.1f} MW in 2032, an increase of approximately {growth_pct:.1f}%.")

st.subheader("Source Data")
st.dataframe(filtered, use_container_width=True, hide_index=True)
st.caption("Source: Department of Energy (DOE), 2023–2032 Distribution Development Plan and DOE-published MASELCO supply-demand data. Derived calculations are analysis results rather than source measurements.")
