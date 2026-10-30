"""
visualizations.py
-------------------
Generates 8 charts (matplotlib + seaborn) from the cleaned dataset and
saves them into outputs/. Run eda.py first to produce the cleaned CSV.

Usage:
    python analysis/visualizations.py
"""

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

sns.set_theme(style="whitegrid", palette="viridis")
plt.rcParams["figure.dpi"] = 110

OUT_DIR = "outputs"


def load():
    df = pd.read_csv("data/retail_sales_cleaned.csv", parse_dates=["order_date"])
    return df


def chart_monthly_revenue(df):
    monthly = df.groupby("month")["revenue"].sum().reset_index()
    plt.figure(figsize=(11, 5))
    sns.lineplot(data=monthly, x="month", y="revenue", marker="o", linewidth=2)
    plt.title("Monthly Revenue Trend (2023–2024)", fontsize=14, weight="bold")
    plt.xlabel("Month")
    plt.ylabel("Revenue (₹)")
    plt.xticks(rotation=60)
    plt.tight_layout()
    plt.savefig(f"{OUT_DIR}/01_monthly_revenue_trend.png")
    plt.close()


def chart_category_revenue(df):
    cat = df.groupby("category")["revenue"].sum().sort_values(ascending=False).reset_index()
    plt.figure(figsize=(9, 5))
    sns.barplot(data=cat, x="revenue", y="category", hue="category", legend=False)
    plt.title("Total Revenue by Category", fontsize=14, weight="bold")
    plt.xlabel("Revenue (₹)")
    plt.ylabel("")
    plt.tight_layout()
    plt.savefig(f"{OUT_DIR}/02_revenue_by_category.png")
    plt.close()


def chart_region_distribution(df):
    plt.figure(figsize=(7, 7))
    region_rev = df.groupby("region")["revenue"].sum()
    colors = sns.color_palette("viridis", len(region_rev))
    plt.pie(region_rev, labels=region_rev.index, autopct="%1.1f%%", startangle=90, colors=colors)
    plt.title("Revenue Share by Region", fontsize=14, weight="bold")
    plt.tight_layout()
    plt.savefig(f"{OUT_DIR}/03_revenue_share_by_region.png")
    plt.close()


def chart_top_products(df):
    top = df.groupby("product")["revenue"].sum().sort_values(ascending=False).head(10).reset_index()
    plt.figure(figsize=(9, 6))
    sns.barplot(data=top, x="revenue", y="product", hue="product", legend=False, palette="mako")
    plt.title("Top 10 Products by Revenue", fontsize=14, weight="bold")
    plt.xlabel("Revenue (₹)")
    plt.ylabel("")
    plt.tight_layout()
    plt.savefig(f"{OUT_DIR}/04_top_10_products.png")
    plt.close()


def chart_payment_mode(df):
    plt.figure(figsize=(8, 5))
    order = df["payment_mode"].value_counts().index
    sns.countplot(data=df, y="payment_mode", order=order, hue="payment_mode", legend=False, palette="crest")
    plt.title("Order Volume by Payment Mode", fontsize=14, weight="bold")
    plt.xlabel("Number of Orders")
    plt.ylabel("")
    plt.tight_layout()
    plt.savefig(f"{OUT_DIR}/05_payment_mode_distribution.png")
    plt.close()


def chart_rating_by_category(df):
    plt.figure(figsize=(9, 5))
    sns.boxplot(data=df, x="category", y="customer_rating", hue="category", legend=False, palette="flare")
    plt.title("Customer Rating Distribution by Category", fontsize=14, weight="bold")
    plt.xlabel("")
    plt.ylabel("Rating (1-5)")
    plt.xticks(rotation=20)
    plt.tight_layout()
    plt.savefig(f"{OUT_DIR}/06_rating_by_category.png")
    plt.close()


def chart_segment_vs_revenue(df):
    plt.figure(figsize=(8, 5))
    seg = df.groupby("customer_segment")["revenue"].sum().reset_index()
    sns.barplot(data=seg, x="customer_segment", y="revenue", hue="customer_segment", legend=False, palette="magma")
    plt.title("Revenue by Customer Segment", fontsize=14, weight="bold")
    plt.xlabel("")
    plt.ylabel("Revenue (₹)")
    plt.tight_layout()
    plt.savefig(f"{OUT_DIR}/07_revenue_by_segment.png")
    plt.close()


def chart_correlation_heatmap(df):
    plt.figure(figsize=(7, 6))
    numeric_cols = ["quantity", "unit_price", "discount_pct", "revenue", "customer_rating"]
    corr = df[numeric_cols].corr()
    sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5)
    plt.title("Correlation Heatmap (Numeric Features)", fontsize=14, weight="bold")
    plt.tight_layout()
    plt.savefig(f"{OUT_DIR}/08_correlation_heatmap.png")
    plt.close()


if __name__ == "__main__":
    df = load()
    chart_monthly_revenue(df)
    chart_category_revenue(df)
    chart_region_distribution(df)
    chart_top_products(df)
    chart_payment_mode(df)
    chart_rating_by_category(df)
    chart_segment_vs_revenue(df)
    chart_correlation_heatmap(df)
    print("8 charts saved to outputs/")
