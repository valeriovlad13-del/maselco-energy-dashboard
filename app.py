import pandas as pd
import plotly.express as px
import streamlit as st
from pathlib import Path

st.set_page_config(
    page_title="MASELCO Energy Data Analysis Dashboard",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# MASELCO-inspired palette: green + yellow, with neutral backgrounds.
GREEN = "#0B6B3A"
GREEN_LIGHT = "#2E8B57"
YELLOW = "#F2C94C"
DARK = "#17352A"
MUTED = "#667085"
GRID = "#E6EAE8"
FORECAST = "#2E8B57"
ACTUAL = "#F2C94C"

DATA_PATH = Path(__file__).parent / "data" / "maselco_energy_data.csv"


@st.cache_data
def load_data():
    return pd.read_csv(DATA_PATH)


df = load_data()

# Minimal, clean styling using the main MASELCO-inspired colors.
st.markdown(
    f"""
    <style>
        .stApp {{
            background: #FAFBFA;
        }}

        [data-testid="stSidebar"] {{
            background: #F3F7F4;
            border-right: 1px solid #DCE6DF;
        }}

        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3 {{
            color: {GREEN};
        }}

        h1, h2, h3 {{
            color: {DARK};
            letter-spacing: -0.02em;
        }}

        .dashboard-subtitle {{
            color: {MUTED};
            font-size: 0.92rem;
            margin-top: -0.55rem;
            margin-bottom: 1.3rem;
        }}

        .section-note {{
            color: {MUTED};
            font-size: 0.86rem;
            margin-top: -0.45rem;
            margin-bottom: 0.8rem;
        }}

        div[data-testid="stMetric"] {{
            background: white;
            border: 1px solid #E1E8E3;
            border-radius: 12px;
            padding: 16px 18px;
            box-shadow: 0 1px 2px rgba(23, 53, 42, 0.04);
        }}

        div[data-testid="stMetricLabel"] {{
            color: {MUTED};
        }}

        div[data-testid="stMetricValue"] {{
            color: {DARK};
        }}

        .finding-card {{
            background: white;
            border: 1px solid #E1E8E3;
            border-left: 4px solid {GREEN};
            border-radius: 10px;
            padding: 14px 16px;
            margin-bottom: 10px;
            line-height: 1.45;
        }}

        .finding-card strong {{
            color: {GREEN};
        }}

        .source-note {{
            color: {MUTED};
            font-size: 0.78rem;
        }}
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("⚡ MASELCO Energy Data Analysis Dashboard")
st.markdown(
    '<div class="dashboard-subtitle">'
    "DOE-published data for the Masbate Electric Cooperative (MASELCO). "
    "Actual and forecast values are explicitly separated."
    "</div>",
    unsafe_allow_html=True,
)

# -----------------------------
# Sidebar filters
# -----------------------------
st.sidebar.header("Dashboard Filters")

years = sorted(df["year"].unique())
year_range = st.sidebar.slider(
    "Year range",
    min_value=int(min(years)),
    max_value=int(max(years)),
    value=(int(min(years)), int(max(years))),
)

statuses = sorted(df["data_status"].unique())
selected_status = st.sidebar.multiselect(
    "Data status",
    statuses,
    default=statuses,
)

filtered = df[
    df["year"].between(year_range[0], year_range[1])
    & df["data_status"].isin(selected_status)
].copy()

st.sidebar.caption("Tip: use the status filter to compare actual and forecast records.")

# -----------------------------
# Fixed 2022 overview
# -----------------------------
st.subheader("MASELCO Overview")
st.markdown(
    '<div class="section-note">2022 actual sector profile with the long-term peak-demand outlook.</div>',
    unsafe_allow_html=True,
)

actual_2022 = df[(df["year"] == 2022) & (df["data_status"] == "Actual")]

customer_rows = actual_2022[
    (actual_2022["dataset"] == "sector_profile")
    & (actual_2022["metric"] == "Captive Customers")
]
sales_rows = actual_2022[
    (actual_2022["dataset"] == "sector_profile")
    & (actual_2022["metric"] == "Energy Sales")
]
peak_rows = actual_2022[
    (actual_2022["dataset"] == "demand_profile")
    & (actual_2022["metric"] == "Peak Demand")
]

total_customers = customer_rows["value"].sum()
total_sales = sales_rows["value"].sum()
peak_demand = peak_rows["value"].iloc[0] if not peak_rows.empty else None

forecast_rows = df[
    (df["dataset"] == "demand_profile")
    & (df["metric"] == "Peak Demand")
    & (df["data_status"] == "Forecast")
].sort_values("year")

forecast_2032 = forecast_rows.iloc[-1]["value"] if not forecast_rows.empty else None

growth_pct = (
    (forecast_2032 - peak_demand) / peak_demand * 100
    if peak_demand is not None and forecast_2032 is not None
    else None
)

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("2022 Captive Customers", f"{total_customers:,.0f}")
c2.metric("2022 Energy Sales", f"{total_sales:,.0f} MWh")
c3.metric("2022 Peak Demand", f"{peak_demand:.1f} MW")
c4.metric("2032 Forecast Peak", f"{forecast_2032:.1f} MW")
c5.metric("Projected Demand Growth", f"+{growth_pct:.1f}%")

# -----------------------------
# 2022 Sector Profile
# -----------------------------
st.subheader("2022 Sector Profile")

sector = actual_2022[actual_2022["dataset"] == "sector_profile"].copy()

customers = (
    sector[sector["metric"] == "Captive Customers"][["sector", "value"]]
    .rename(columns={"value": "customers"})
)
sales = (
    sector[sector["metric"] == "Energy Sales"][["sector", "value"]]
    .rename(columns={"value": "sales_mwh"})
)

sector_summary = customers.merge(sales, on="sector")
sector_summary["customer_share_pct"] = (
    sector_summary["customers"] / sector_summary["customers"].sum() * 100
)
sector_summary["sales_share_pct"] = (
    sector_summary["sales_mwh"] / sector_summary["sales_mwh"].sum() * 100
)
sector_summary["mwh_per_customer"] = (
    sector_summary["sales_mwh"] / sector_summary["customers"]
)

left, right = st.columns(2)

with left:
    fig = px.bar(
        sector_summary,
        x="sector",
        y="customers",
        title="Captive Customers by Sector",
        labels={"sector": "Sector", "customers": "Customers"},
        text_auto=".0f",
        color_discrete_sequence=[GREEN],
    )
    fig.update_layout(
        showlegend=False,
        plot_bgcolor="white",
        paper_bgcolor="white",
        font_color=DARK,
        margin=dict(l=10, r=10, t=55, b=10),
        yaxis=dict(gridcolor=GRID),
    )
    st.plotly_chart(fig, use_container_width=True)

with right:
    fig = px.bar(
        sector_summary,
        x="sector",
        y="sales_mwh",
        title="Energy Sales by Sector",
        labels={"sector": "Sector", "sales_mwh": "Energy Sales (MWh)"},
        text_auto=".0f",
        color_discrete_sequence=[YELLOW],
    )
    fig.update_layout(
        showlegend=False,
        plot_bgcolor="white",
        paper_bgcolor="white",
        font_color=DARK,
        margin=dict(l=10, r=10, t=55, b=10),
        yaxis=dict(gridcolor=GRID),
    )
    st.plotly_chart(fig, use_container_width=True)

st.dataframe(
    sector_summary.style.format(
        {
            "customers": "{:,.0f}",
            "sales_mwh": "{:,.0f}",
            "customer_share_pct": "{:.1f}%",
            "sales_share_pct": "{:.1f}%",
            "mwh_per_customer": "{:.2f}",
        }
    ),
    use_container_width=True,
    hide_index=True,
)

# -----------------------------
# Key Findings
# -----------------------------
st.subheader("Key Findings")

residential = sector_summary[sector_summary["sector"] == "Residential"].iloc[0]
industrial = sector_summary[sector_summary["sector"] == "Industrial"].iloc[0]

findings = [
    f"<strong>Customer concentration:</strong> Residential customers represent {residential['customer_share_pct']:.1f}% of MASELCO's 2022 captive customers.",
    f"<strong>Energy-sales concentration:</strong> Residential customers account for {residential['sales_share_pct']:.1f}% of 2022 energy sales.",
    f"<strong>Customer intensity:</strong> Industrial customers average {industrial['mwh_per_customer']:.2f} MWh per customer, compared with {residential['mwh_per_customer']:.2f} MWh for residential customers.",
]

for finding in findings:
    st.markdown(f'<div class="finding-card">{finding}</div>', unsafe_allow_html=True)

# -----------------------------
# Peak Demand
# -----------------------------
st.subheader("Peak Demand: 2022 Actual and 2023–2032 Forecast")
st.markdown(
    '<div class="section-note">The 2022 value is actual; 2023–2032 values are forecasts.</div>',
    unsafe_allow_html=True,
)

demand = filtered[
    (filtered["dataset"] == "demand_profile")
    & (filtered["metric"] == "Peak Demand")
].sort_values("year")

if not demand.empty:
    fig = px.line(
        demand,
        x="year",
        y="value",
        markers=True,
        color="data_status",
        title="MASELCO Peak Demand",
        labels={
            "year": "Year",
            "value": "Peak Demand (MW)",
            "data_status": "Status",
        },
        color_discrete_map={"Actual": ACTUAL, "Forecast": FORECAST},
    )
    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        font_color=DARK,
        margin=dict(l=10, r=10, t=55, b=10),
        xaxis=dict(gridcolor=GRID),
        yaxis=dict(gridcolor=GRID),
        legend=dict(orientation="h", y=1.08, x=0),
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("No peak-demand records match the selected filters.")

if peak_demand is not None and forecast_2032 is not None:
    st.info(
        f"Peak demand is projected to increase from {peak_demand:.1f} MW in 2022 "
        f"to {forecast_2032:.1f} MW in 2032, an increase of approximately {growth_pct:.1f}%."
    )

# -----------------------------
# Source Data
# -----------------------------
st.subheader("Source Data")
st.markdown(
    '<div class="section-note">Use the filters in the sidebar to inspect the records used by the dashboard.</div>',
    unsafe_allow_html=True,
)

st.dataframe(filtered, use_container_width=True, hide_index=True)

st.markdown(
    '<div class="source-note">'
    "Source: Department of Energy (DOE), 2023–2032 Distribution Development Plan "
    "and DOE-published MASELCO supply-demand data. Derived calculations are "
    "analysis results rather than source measurements."
    "</div>",
    unsafe_allow_html=True,
)
