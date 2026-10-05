# MASELCO Energy Data Analysis Dashboard

An interactive data-analysis dashboard for the **Masbate Electric Cooperative (MASELCO)** using publicly available data published by the Philippine Department of Energy (DOE).

## Live Dashboard

**[Open the MASELCO Energy Data Analysis Dashboard](https://maselco-energy-dashboard.streamlit.app/)**

The dashboard presents utility-level analysis of MASELCO's customer distribution, electricity sales, and peak-demand planning data.

## Overview

The dashboard analyzes:

- 2022 captive customers by sector
- 2022 energy sales by sector
- Customer share and energy sales share
- Energy sales per customer
- 2022 actual peak demand
- 2023–2032 forecast peak demand
- Actual-versus-forecast demand trends
- Interactive year-range and data-status filtering
- Source-traceable data and derived metrics

## Key Findings

Based on the current dataset:

- Residential customers account for **95.5%** of MASELCO's 2022 captive customers.
- Residential customers account for **70.5%** of 2022 energy sales.
- Industrial customers average **28.00 MWh per customer**, compared with **1.26 MWh per residential customer**.
- Peak demand increases from **28.1 MW in 2022** to a projected **52.4 MW in 2032**, an increase of approximately **86.5%**.

## Data Source

Primary source: **Department of Energy (DOE) — 2023–2032 Distribution Development Plan**.

The MASELCO section contains 2022 actual customer counts and energy sales by sector. A DOE-published MASELCO supply-demand series is used for the peak-demand planning trend.

[DOE — 2023–2032 Distribution Development Plan](https://prod-cms.doe.gov.ph/documents/d/epimb/2023-2032-distribution-development-plan)

### Data Policy

- Source data are not fabricated.
- Actual and forecast values are clearly distinguished.
- Calculated metrics are derived from source values.
- Forecast values are never presented as measured actual data.
- Additional datasets are added only after source verification.

## Technology

- **Python**
- **Pandas**
- **Plotly**
- **Streamlit**
- **GitHub**
- **Streamlit Community Cloud**

## Project Structure

```text
maselco-energy-dashboard/
├── app.py
├── data/
│   └── maselco_energy_data.csv
├── analysis/
│   └── analysis.py
├── requirements.txt
├── README.md
├── .gitignore
├── .streamlit/
│   └── config.toml
└── screenshots/
```

## Run Locally

Clone the repository, install the dependencies, and start the Streamlit application:

```bash
git clone https://github.com/valeriovlad13-del/maselco-energy-dashboard.git
cd maselco-energy-dashboard
pip install -r requirements.txt
streamlit run app.py
```

## Main Derived Metrics

**Customer Share (%)**

`Sector Customers / Total Customers × 100`

**Energy Sales Share (%)**

`Sector Energy Sales / Total Energy Sales × 100`

**MWh per Customer**

`Sector Energy Sales / Sector Customers`

**Peak-Demand Increase (%)**

`(Forecast Peak Demand − Actual Peak Demand) / Actual Peak Demand × 100`

## Future Improvements

- Energy purchase and system-loss analysis
- Longer historical time series
- Supply-demand margin analysis
- Forecast-versus-actual analysis when comparable actual data are available
- Additional MASELCO planning indicators
- Downloadable filtered datasets

## Author

**Blademir P. Rubia**

Electrical Engineer | Computer Science Student | Data Analyst

[GitHub](https://github.com/valeriovlad13-del)
