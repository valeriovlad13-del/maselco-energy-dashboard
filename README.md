# MASELCO Energy Data Analysis Dashboard

An interactive data-analysis dashboard for the **Masbate Electric Cooperative (MASELCO)** using publicly available data published by the Philippine Department of Energy (DOE).

## Project Goal

This project combines Electrical Engineering knowledge with Computer Science and data-analysis skills to analyze utility-level electricity data.

The first version focuses on customer distribution, energy sales, customer-vs-sales shares, energy sales per customer, peak-demand trends, actual-versus-forecast distinction, interactive filtering, and source traceability.

## Data Source

Primary source: **Department of Energy (DOE) — 2023–2032 Distribution Development Plan**.

The MASELCO section contains 2022 actual customer counts and energy sales by sector. A DOE-published MASELCO supply-demand series is used for the peak-demand planning trend.

### Data policy

- Source data are not fabricated.
- Actual and forecast values are kept separate.
- Calculated metrics are derived from source values.
- Forecast values are never presented as measured actual data.
- Additional datasets will only be added after source verification.

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
└── screenshots/
```

## Technology

- Python
- Pandas
- Plotly
- Streamlit
- GitHub
- Streamlit Community Cloud

## Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Main Derived Metrics

**Customer Share (%)** = Sector Customers / Total Customers × 100

**Energy Sales Share (%)** = Sector Energy Sales / Total Energy Sales × 100

**MWh per Customer** = Sector Energy Sales / Sector Customers

**Peak-Demand Increase (%)** = (Forecast Peak Demand − Actual Peak Demand) / Actual Peak Demand × 100

## Future Improvements

1. Energy purchase and system-loss analysis
2. Longer historical time series
3. Supply-demand margin analysis
4. Forecast-versus-actual analysis when comparable actual data are available
5. Additional MASELCO planning indicators
6. Downloadable filtered datasets
7. Streamlit Community Cloud deployment

## Author

**Blademir Rubia**

Electrical Engineer | Computer Science Student

Project C — Data Analysis Portfolio
