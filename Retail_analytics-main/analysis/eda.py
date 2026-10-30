"""
eda.py
-------
Loads the raw dataset, cleans it, and prints a full exploratory
data analysis summary to the console. This is the "show your pandas/numpy
skills" script.

Usage:
    python analysis/eda.py
"""

import numpy as np
import pandas as pd

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 120)


def load_and_clean(path="data/retail_sales.csv"):
    df = pd.read_csv(path, parse_dates=["order_date"])

    print("=" * 60)
    print("RAW SHAPE:", df.shape)
    print("DUPLICATE ROWS:", df.duplicated().sum())
    print("MISSING VALUES:\n", df.isnull().sum())
    print("=" * 60)

    # Drop exact duplicates
    df = df.drop_duplicates()

    # Fill missing ratings with the category-level median (more meaningful than a global fill)
    df["customer_rating"] = df.groupby("category")["customer_rating"].transform(
        lambda x: x.fillna(x.median())
    )

    # Feature engineering
    df["month"] = df["order_date"].dt.to_period("M").astype(str)
    df["weekday"] = df["order_date"].dt.day_name()
    df["quarter"] = df["order_date"].dt.to_period("Q").astype(str)
    df["profit_margin_est"] = np.where(
        df["discount_pct"] > 15, "Low", np.where(df["discount_pct"] > 5, "Medium", "High")
    )

    return df.reset_index(drop=True)


def summary_stats(df):
    print("\n--- REVENUE SUMMARY (numpy + pandas) ---")
    revenue = df["revenue"].to_numpy()
    print(f"Total Revenue:   ₹{revenue.sum():,.2f}")
    print(f"Mean Order Value: ₹{revenue.mean():,.2f}")
    print(f"Median Order Value: ₹{np.median(revenue):,.2f}")
    print(f"Std Dev: ₹{revenue.std():,.2f}")
    print(f"95th percentile order value: ₹{np.percentile(revenue, 95):,.2f}")

    print("\n--- TOP 5 CATEGORIES BY REVENUE ---")
    print(df.groupby("category")["revenue"].sum().sort_values(ascending=False).head())

    print("\n--- TOP 5 PRODUCTS BY REVENUE ---")
    print(df.groupby("product")["revenue"].sum().sort_values(ascending=False).head())

    print("\n--- REVENUE BY REGION ---")
    print(df.groupby("region")["revenue"].agg(["sum", "mean", "count"]).sort_values("sum", ascending=False))

    print("\n--- MONTHLY REVENUE TREND ---")
    print(df.groupby("month")["revenue"].sum())

    print("\n--- CUSTOMER SEGMENT BREAKDOWN ---")
    print(df.groupby("customer_segment")["revenue"].agg(["sum", "mean", "count"]))

    print("\n--- PAYMENT MODE POPULARITY ---")
    print(df["payment_mode"].value_counts(normalize=True).mul(100).round(1))

    print("\n--- AVG RATING BY CATEGORY ---")
    print(df.groupby("category")["customer_rating"].mean().sort_values(ascending=False))

    return df


if __name__ == "__main__":
    df = load_and_clean()
    df = summary_stats(df)
    df.to_csv("data/retail_sales_cleaned.csv", index=False)
    print("\nCleaned dataset saved -> data/retail_sales_cleaned.csv")
