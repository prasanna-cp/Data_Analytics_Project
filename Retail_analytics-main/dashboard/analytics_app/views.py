import numpy as np
import pandas as pd
from django.conf import settings
from django.shortcuts import render


def dashboard(request):
    """
    Loads the cleaned retail sales CSV and computes the KPIs / tables
    shown on the dashboard. This is where pandas plugs into Django:
    the analysis layer (analysis/eda.py) and the web layer share the
    same cleaned CSV as their data contract.
    """
    csv_path = settings.DATA_CSV_PATH

    if not csv_path.exists():
        return render(request, "analytics_app/missing_data.html", {"csv_path": str(csv_path)})

    df = pd.read_csv(csv_path, parse_dates=["order_date"])

    revenue = df["revenue"].to_numpy()
    kpis = {
        "total_revenue": f"₹{revenue.sum():,.0f}",
        "total_orders": f"{len(df):,}",
        "avg_order_value": f"₹{revenue.mean():,.0f}",
        "avg_rating": f"{df['customer_rating'].mean():.2f} / 5",
    }

    top_categories = (
        df.groupby("category")["revenue"].sum().sort_values(ascending=False).round(0).astype(int)
    )
    top_products = (
        df.groupby("product")["revenue"].sum().sort_values(ascending=False).head(5).round(0).astype(int)
    )
    region_table = (
        df.groupby("region")["revenue"].agg(["sum", "mean", "count"]).sort_values("sum", ascending=False)
    )
    region_table["sum"] = region_table["sum"].round(0).astype(int)
    region_table["mean"] = region_table["mean"].round(0).astype(int)

    context = {
        "kpis": kpis,
        "top_categories": top_categories.items(),
        "top_products": top_products.items(),
        "region_table": region_table.itertuples(),
        "chart_files": [
            "01_monthly_revenue_trend.png",
            "02_revenue_by_category.png",
            "03_revenue_share_by_region.png",
            "04_top_10_products.png",
            "05_payment_mode_distribution.png",
            "06_rating_by_category.png",
            "07_revenue_by_segment.png",
            "08_correlation_heatmap.png",
        ],
    }
    return render(request, "analytics_app/dashboard.html", context)
