"""
generate_data.py
-----------------
Generates a realistic synthetic retail sales dataset for the analytics project.
Run this first — every other script depends on data/retail_sales.csv existing.

Usage:
    python data/generate_data.py
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta

np.random.seed(42)

# ---------------------------------------------------------
# Config
# ---------------------------------------------------------
N_ROWS = 8000
START_DATE = datetime(2023, 1, 1)
END_DATE = datetime(2024, 12, 31)

CATEGORIES = {
    "Electronics": ["Headphones", "Smartphone", "Laptop", "Smartwatch", "Tablet"],
    "Clothing": ["T-Shirt", "Jeans", "Jacket", "Sneakers", "Dress"],
    "Home & Kitchen": ["Blender", "Cookware Set", "Vacuum Cleaner", "Air Fryer", "Bedsheet"],
    "Beauty": ["Face Wash", "Perfume", "Lipstick", "Shampoo", "Sunscreen"],
    "Sports": ["Yoga Mat", "Dumbbells", "Football", "Running Shoes", "Cycling Helmet"],
}

CITIES = {
    "Bengaluru": "South", "Chennai": "South", "Hyderabad": "South",
    "Mumbai": "West", "Pune": "West", "Ahmedabad": "West",
    "Delhi": "North", "Jaipur": "North", "Lucknow": "North",
    "Kolkata": "East", "Bhubaneswar": "East",
}

PAYMENT_MODES = ["UPI", "Credit Card", "Debit Card", "Net Banking", "Cash on Delivery"]
CUSTOMER_SEGMENTS = ["New", "Returning", "Loyal"]

BASE_PRICES = {
    "Headphones": 1800, "Smartphone": 18000, "Laptop": 52000, "Smartwatch": 4500, "Tablet": 16000,
    "T-Shirt": 500, "Jeans": 1400, "Jacket": 2200, "Sneakers": 2800, "Dress": 1600,
    "Blender": 1900, "Cookware Set": 3200, "Vacuum Cleaner": 6500, "Air Fryer": 4200, "Bedsheet": 900,
    "Face Wash": 250, "Perfume": 1800, "Lipstick": 450, "Shampoo": 350, "Sunscreen": 400,
    "Yoga Mat": 700, "Dumbbells": 1500, "Football": 900, "Running Shoes": 3200, "Cycling Helmet": 1800,
}


def random_dates(start, end, n):
    delta_days = (end - start).days
    offsets = np.random.randint(0, delta_days, size=n)
    return [start + timedelta(days=int(d)) for d in offsets]


def generate():
    rows = []
    dates = random_dates(START_DATE, END_DATE, N_ROWS)
    cities = list(CITIES.keys())

    for i in range(N_ROWS):
        category = np.random.choice(list(CATEGORIES.keys()), p=[0.28, 0.24, 0.18, 0.16, 0.14])
        product = np.random.choice(CATEGORIES[category])
        city = np.random.choice(cities)
        region = CITIES[city]

        base_price = BASE_PRICES[product]
        # add some seasonal / random noise to price (discounts, price drift)
        price = base_price * np.random.uniform(0.85, 1.15)

        quantity = np.random.choice([1, 1, 1, 2, 2, 3], p=[0.45, 0.2, 0.15, 0.1, 0.06, 0.04])

        discount_pct = np.random.choice([0, 5, 10, 15, 20, 30], p=[0.35, 0.2, 0.2, 0.15, 0.07, 0.03])
        discount_amount = price * quantity * (discount_pct / 100)
        revenue = round(price * quantity - discount_amount, 2)

        rating = np.clip(np.random.normal(4.1, 0.7), 1, 5)

        date = dates[i]
        # slight holiday-season boost simulation for Oct-Dec
        if date.month in (10, 11, 12) and np.random.rand() < 0.3:
            revenue *= 1.2

        rows.append({
            "order_id": f"ORD{100000 + i}",
            "order_date": date.strftime("%Y-%m-%d"),
            "category": category,
            "product": product,
            "city": city,
            "region": region,
            "quantity": quantity,
            "unit_price": round(price, 2),
            "discount_pct": discount_pct,
            "revenue": round(revenue, 2),
            "payment_mode": np.random.choice(PAYMENT_MODES, p=[0.35, 0.25, 0.2, 0.1, 0.1]),
            "customer_segment": np.random.choice(CUSTOMER_SEGMENTS, p=[0.4, 0.35, 0.25]),
            "customer_rating": round(rating, 1),
        })

    df = pd.DataFrame(rows)

    # Inject a small amount of realistic messiness so the cleaning step has real work to do
    missing_idx = np.random.choice(df.index, size=int(0.02 * N_ROWS), replace=False)
    df.loc[missing_idx, "customer_rating"] = np.nan

    dup_idx = np.random.choice(df.index, size=15, replace=False)
    df = pd.concat([df, df.loc[dup_idx]], ignore_index=True)

    df = df.sample(frac=1, random_state=1).reset_index(drop=True)  # shuffle
    return df


if __name__ == "__main__":
    df = generate()
    out_path = "data/retail_sales.csv"
    df.to_csv(out_path, index=False)
    print(f"Generated {len(df)} rows -> {out_path}")
    print(df.head())
