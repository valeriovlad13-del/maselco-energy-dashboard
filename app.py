import pandas as pd
import plotly.express as px
import streamlit as st
from pathlib import Path

st.set_page_config(
    page_title="MASELCO Energy Data Analysis Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
)

# MASELCO-inspired palette: green + yellow with clean neutral surfaces.
GREEN = "#0B6B3A"
GREEN_LIGHT = "#2E8B57"
YELLOW = "#F2C94C"
DARK = "#17352A"
MUTED = "#667085"
GRID = "#E6EAE8"
ACTUAL = "#0B6B3A"
FORECAST = "#F2B705"

DATA_PATH = Path(__file__).parent / "data" / "maselco_energy_data.csv"


@st.cache_data
def load_data():
    return pd.read_csv(DATA_PATH)


df = load_data()

def icon_svg(kind, color=GREEN, size=24):
    icons = {
        "bolt": '<path d="M13 2 3 14h7l-1 8 12-14h-7l-1-6Z"/>',
        "users": '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75"/>',
        "chart": '<path d="M4 19V9m6 10V5m6 14v-7m6 7V3"/>',
        "trend": '<path d="m3 17 6-6 4 4 8-9"/><path d="M17 6h4v4"/>',
        "table": '<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M3 10h18M9 4v16M15 10v10"/>',
        "info": '<circle cx="12" cy="12" r="9"/><path d="M12 11v5M12 8h.01"/>',
    }
    path = icons.get(kind, icons["info"])
    return (
        f'<svg class="svg-icon" width="{size}" height="{size}" viewBox="0 0 24 24" '
        f'fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" '
        f'aria-hidden="true">{path}</svg>'
    )


# -----------------------------
# Responsive, minimal styling
# -----------------------------
st.markdown(
    f"""
    <style>
        .stApp {{
            background: #FAFBFA;
            color: {DARK};
        }}

        [data-testid="stAppViewContainer"] {{
            background: #FAFBFA;
        }}

        /* Pull the dashboard content to the top of the viewport while preserving Streamlit's native header behavior. */
        [data-testid="stAppViewContainer"] .main .block-container {{
            padding-top: 0 !important;
            padding-bottom: 0.75rem !important;
            margin-top: 0 !important;
        }}



        @media (max-width: 480px) {{
            .dashboard-title {{
                font-size: 1.05rem;
            }}

            .header-map {{
                display: none;
            }}
        }}

        @media (max-width: 640px) {{
            [data-testid="stHorizontalBlock"] {{
                flex-direction: column !important;
                gap: 0.75rem !important;
            }}

            [data-testid="stHorizontalBlock"] > [data-testid="column"] {{
                width: 100% !important;
                flex: 1 1 100% !important;
            }}

            .modebar {{
                display: none !important;
            }}
            [data-testid="stAppViewContainer"] .main .block-container {{
                padding-top: 0 !important;
                padding-bottom: 0.5rem !important;
                margin-top: 0 !important;
            }}
        }}

        /* Keep Streamlit's native header controls functional without creating a large visual strip. */
        [data-testid="stHeader"] {{
            background: transparent !important;
            border: 0 !important;
            box-shadow: none !important;
            height: 0 !important;
            min-height: 0 !important;
        }}

        [data-testid="stDecoration"] {{
            display: none !important;
        }}

        /* Native Streamlit navigation controls are replaced by in-page controls. */
        [data-testid="collapsedControl"],
        [data-testid="stToolbar"] {{
            display: none !important;
        }}

        h1, h2, h3 {{
            color: {DARK};
            letter-spacing: -0.02em;
        }}

        .dashboard-header {{
            position: sticky;
            top: 0;
            z-index: 1000;
            display: flex;
            align-items: center;
            gap: 12px;
            min-height: 64px;
            margin: -1rem -1rem 0;
            padding: 10px 1rem;
            background: rgba(250, 251, 250, 0.96);
            border-bottom: 1px solid #E1E8E3;
            box-shadow: 0 2px 10px rgba(23, 53, 42, 0.05);
            backdrop-filter: blur(8px);
        }}

        .header-icon {{
            display: flex;
            align-items: center;
            justify-content: center;
            width: 42px;
            height: 42px;
            flex: 0 0 42px;
            border-radius: 10px;
            background: #EAF5EE;
        }}

        .header-icon svg {{
            width: 25px;
            height: 25px;
        }}

        .dashboard-title {{
            color: {DARK};
            font-size: clamp(1.3rem, 2.8vw, 2rem);
            font-weight: 700;
            line-height: 1.15;
        }}

        .header-map {{
            margin-left: auto;
            display: flex;
            align-items: center;
            gap: 8px;
            flex: 0 0 auto;
        }}

        .header-map img {{
            width: 38px;
            height: 48px;
            object-fit: contain;
            opacity: 0.88;
        }}

        .header-map-label {{
            color: {MUTED};
            font-size: 0.72rem;
            line-height: 1.2;
            text-align: left;
        }}

        .dashboard-subtitle {{
            color: {MUTED};
            font-size: 0.9rem;
            line-height: 1.45;
            margin: 3px 0 1.25rem 54px;
        }}

        .section-note {{
            color: {MUTED};
            font-size: 0.86rem;
            margin-top: -0.45rem;
            margin-bottom: 0.8rem;
        }}

        @media print {{
            [data-testid="stSidebar"],
            [data-testid="stHeader"] {{
                display: none !important;
            }}
        }}

        div[data-testid="stMetric"] {{
            background: white;
            border: 1px solid #E1E8E3;
            border-radius: 12px;
            padding: 14px 15px;
            min-height: 104px;
            box-shadow: 0 1px 2px rgba(23, 53, 42, 0.04);
        }}

        div[data-testid="stMetricLabel"] {{
            color: {MUTED};
            font-size: 0.78rem;
        }}

        div[data-testid="stMetricValue"] {{
            color: {DARK};
            font-size: clamp(1.25rem, 2.3vw, 1.75rem);
        }}

        .finding-card {{
            display: flex;
            gap: 10px;
            align-items: flex-start;
            background: white;
            border: 1px solid #E1E8E3;
            border-left: 4px solid {GREEN};
            border-radius: 10px;
            padding: 12px 14px;
            margin-bottom: 9px;
            line-height: 1.45;
            font-size: 0.9rem;
        }}

        .finding-icon {{
            flex: 0 0 24px;
            margin-top: 1px;
        }}

        .finding-card strong {{
            color: {GREEN};
        }}

        .source-note {{
            color: {MUTED};
            font-size: 0.78rem;
            line-height: 1.45;
        }}

        .dashboard-footer {{
            border-top: 1px solid #DCE6DF;
            margin-top: 2rem;
            padding: 16px 0 8px;
            color: {MUTED};
            font-size: 0.76rem;
        }}

        .footer-name {{
            color: {DARK};
            font-weight: 700;
            font-size: 0.9rem;
        }}

        .footer-role {{
            margin-top: 3px;
        }}

        .footer-dot {{
            color: {YELLOW};
            padding: 0 5px;
        }}

        .svg-icon {{
            vertical-align: middle;
        }}

        @media (max-width: 900px) {{
            .dashboard-subtitle {{
                margin-left: 0;
            }}

            .header-icon {{
                width: 36px;
                height: 36px;
                flex-basis: 36px;
            }}

            .dashboard-header {{
                gap: 9px;
                min-height: 58px;
                margin-left: -0.5rem;
                margin-right: -0.5rem;
                padding-left: 0.5rem;
                padding-right: 0.5rem;
            }}

            .header-map-label {{
                display: none;
            }}

            .header-map img {{
                width: 30px;
                height: 38px;
            }}

            [data-testid="stSidebar"] {{
                min-width: 280px;
            }}
        }}

        @media (max-width: 640px) {{
            .dashboard-title {{
                font-size: 1.15rem;
            }}

            .dashboard-header {{
                min-height: 54px;
                padding-top: 7px;
                padding-bottom: 7px;
            }}

            .dashboard-subtitle {{
                font-size: 0.82rem;
                margin-top: 5px;
                margin-bottom: 1rem;
            }}

            div[data-testid="stMetric"] {{
                min-height: auto;
                padding: 12px 13px;
            }}

            .finding-card {{
                font-size: 0.82rem;
                padding: 10px 11px;
            }}

            .dashboard-footer {{
                font-size: 0.72rem;
            }}
        }}
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------
# Header
# -----------------------------
st.markdown(
    f"""
    <div class="dashboard-header">
        <div class="header-icon">{icon_svg("bolt", YELLOW, 26)}</div>
        <div class="dashboard-title">MASELCO Energy Data Analysis Dashboard</div>
        <div class="header-map" title="Masbate, Philippines">
            <img src="https://commons.wikimedia.org/wiki/Special:Redirect/file/Masbate_in_Philippines.svg" alt="Map of Masbate, Philippines">
            <div class="header-map-label">MASBATE<br>PHILIPPINES</div>
        </div>
    </div>
    <div class="dashboard-subtitle">
        Analysis of MASELCO's customer distribution, energy sales, and peak demand
        using DOE-published data.
    </div>
    """,
    unsafe_allow_html=True,
)

# -----------------------------
# Dashboard filters
# -----------------------------
years = sorted(df["year"].unique())
statuses = sorted(df["data_status"].unique())

filtered = df.copy()

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

# Streamlit automatically stacks these columns on narrower screens.
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
        yaxis=dict(gridcolor=GRID, rangemode="tozero"),
    )
    st.plotly_chart(fig, use_container_width=True)

sector_table = sector_summary.rename(
    columns={
        "sector": "Sector",
        "customers": "Customers",
        "sales_mwh": "Energy Sales (MWh)",
        "customer_share_pct": "Customer Share",
        "sales_share_pct": "Sales Share",
        "mwh_per_customer": "MWh per Customer",
    }
)

st.dataframe(
    sector_table.style.format(
        {
            "Customers": "{:,.0f}",
            "Energy Sales (MWh)": "{:,.0f}",
            "Customer Share": "{:.1f}%",
            "Sales Share": "{:.1f}%",
            "MWh per Customer": "{:.2f}",
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
    ("users", GREEN, f"<strong>Customer concentration:</strong> Residential customers represent {residential['customer_share_pct']:.1f}% of MASELCO's 2022 captive customers."),
    ("chart", GREEN, f"<strong>Energy-sales concentration:</strong> Residential customers account for {residential['sales_share_pct']:.1f}% of 2022 energy sales."),
    ("bolt", YELLOW, f"<strong>Customer intensity:</strong> Industrial customers average {industrial['mwh_per_customer']:.2f} MWh per customer, compared with {residential['mwh_per_customer']:.2f} MWh for residential customers."),
]

for kind, color, finding in findings:
    st.markdown(
        f'<div class="finding-card"><div class="finding-icon">{icon_svg(kind, color, 22)}</div><div>{finding}</div></div>',
        unsafe_allow_html=True,
    )

st.markdown("### Dashboard Filters")
filter_col1, filter_col2 = st.columns(2)

with filter_col1:
    year_range = st.slider(
        "Year range",
        min_value=int(min(years)),
        max_value=int(max(years)),
        value=(int(min(years)), int(max(years))),
    )

with filter_col2:
    selected_status = st.multiselect(
        "Data status",
        statuses,
        default=statuses,
    )

filtered = df[
    df["year"].between(year_range[0], year_range[1])
    & df["data_status"].isin(selected_status)
].copy()

st.markdown(
    '<div class="section-note">Use these filters to control the peak-demand chart and source-data table.</div>',
    unsafe_allow_html=True,
)

# -----------------------------
# Peak Demand
# -----------------------------
st.subheader("Peak Demand: Actual and Forecast")
st.markdown(
    '<div class="section-note">The chart and summary below respond to the selected year range and data-status filters.</div>',
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
    if (not demand.empty) and ("Forecast" in demand["data_status"].values) and ("Actual" in demand["data_status"].values):
        forecast_start = int(demand.loc[demand["data_status"] == "Forecast", "year"].min())
        fig.add_vline(
            x=forecast_start - 0.5,
            line_dash="dot",
            line_color="#AAB7B0",
            annotation_text="Forecast begins",
            annotation_position="top right",
            annotation_font_color=MUTED,
        )
    st.plotly_chart(fig, use_container_width=True)

    # Dynamic summary: always use the first and last visible demand records.
    first_point = demand.iloc[0]
    last_point = demand.iloc[-1]
    first_year = int(first_point["year"])
    last_year = int(last_point["year"])
    first_value = float(first_point["value"])
    last_value = float(last_point["value"])

    if first_year == last_year:
        st.info(
            f"Peak demand for {first_year} is {first_value:.1f} MW "
            f"({first_point['data_status'].lower()})."
        )
    else:
        change_pct = (last_value - first_value) / first_value * 100
        direction = "increase" if change_pct >= 0 else "decrease"
        st.info(
            f"Peak demand changes from {first_value:.1f} MW in {first_year} "
            f"to {last_value:.1f} MW in {last_year}, a {direction} of "
            f"approximately {abs(change_pct):.1f}% over the selected period."
        )
else:
    st.warning("No peak-demand records match the selected filters.")

# -----------------------------
# About the Dashboard
# -----------------------------
st.subheader("About This Dashboard")
st.markdown(
    f"""
    <div class="finding-card">
        <div class="finding-icon">{icon_svg("info", GREEN, 22)}</div>
        <div>
            This dashboard analyzes DOE-published MASELCO data to examine
            <strong>customer distribution, electricity sales, and peak-demand projections</strong>.
            It combines Electrical Engineering knowledge with Python-based data analysis
            and interactive visualization.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# -----------------------------
# Source Data
# -----------------------------
st.subheader("Source Data")
st.markdown(
    '<div class="section-note">Use the filters above to inspect the records used by the dashboard. Source URLs are retained in the dataset but omitted here for readability.</div>',
    unsafe_allow_html=True,
)

source_display = filtered[
    ["dataset", "year", "sector", "metric", "value", "unit", "data_status", "source"]
].rename(
    columns={
        "dataset": "Dataset",
        "year": "Year",
        "sector": "Sector",
        "metric": "Metric",
        "value": "Value",
        "unit": "Unit",
        "data_status": "Status",
        "source": "Source Document",
    }
)

st.dataframe(
    source_display,
    use_container_width=True,
    hide_index=True,
)

# -----------------------------
# Footer
# -----------------------------
st.markdown(
    f"""
    <div class="dashboard-footer">
        <div class="footer-name">MASELCO Energy Data Analysis Dashboard</div>
        <div class="footer-role">
            Developed by <strong style="color:{DARK};">Engr. Blademir P. Rubia</strong>
            <span class="footer-dot">|</span>
            Electrical Engineer
            <span class="footer-dot">|</span>
            Computer Science
            <span class="footer-dot">|</span>
            Data Analyst
        </div>
        <div class="source-note" style="margin-top:7px;">
            Source: Department of Energy (DOE), 2023–2032 Distribution Development Plan
            and DOE-published MASELCO supply-demand data. Derived calculations are
            analysis results rather than source measurements.<br>
            Map: Milenioscuro, <a href="https://commons.wikimedia.org/wiki/File:Masbate_in_Philippines.svg" target="_blank" rel="noopener noreferrer">Wikimedia Commons, CC BY-SA 4.0</a>.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


