from pathlib import Path
import pandas as pd

DATA_PATH = Path(__file__).parents[1] / "data" / "maselco_energy_data.csv"

def load_data():
    return pd.read_csv(DATA_PATH)

def build_sector_summary(df):
    actual = df[(df["year"] == 2022) & (df["data_status"] == "Actual") & (df["dataset"] == "sector_profile")]
    customers = actual[actual["metric"] == "Captive Customers"][["sector", "value"]].rename(columns={"value": "customers"})
    sales = actual[actual["metric"] == "Energy Sales"][["sector", "value"]].rename(columns={"value": "sales_mwh"})
    result = customers.merge(sales, on="sector")
    result["customer_share_pct"] = result["customers"] / result["customers"].sum() * 100
    result["sales_share_pct"] = result["sales_mwh"] / result["sales_mwh"].sum() * 100
    result["mwh_per_customer"] = result["sales_mwh"] / result["customers"]
    return result

if __name__ == "__main__":
    print(build_sector_summary(load_data()).to_string(index=False))
