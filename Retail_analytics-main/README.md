# Retail Sales Analytics Dashboard

An end-to-end data analytics project: synthetic retail dataset → data cleaning →
exploratory analysis → visualization → a Django web dashboard that serves the
results. Built to be resume-ready and GitHub-presentable.

**Stack:** Python, NumPy, Pandas, Matplotlib, Seaborn, Django, Jupyter

---

## What this project shows

- Generating and cleaning a realistic, messy dataset (duplicates, missing values)
- Feature engineering with pandas (date parts, derived columns, pivot tables)
- Statistical summaries with NumPy (percentiles, std dev, aggregates)
- 8 different chart types with Matplotlib/Seaborn (line, bar, pie, box, heatmap)
- A Jupyter notebook version of the full analysis, with outputs baked in, for
  easy viewing on GitHub
- A Django web app that reads the cleaned CSV and renders a live KPI dashboard
  — this is the piece that turns "a notebook" into "a small full-stack project"

---

## Folder structure

```
retail_sales_analytics/
├── data/
│   ├── generate_data.py          # creates the synthetic dataset
│   ├── retail_sales.csv          # raw generated data (created after step 1)
│   └── retail_sales_cleaned.csv  # cleaned data (created after step 2)
├── analysis/
│   ├── eda.py                    # cleaning + full EDA, prints to console
│   └── visualizations.py         # generates 8 charts into outputs/
├── notebook/
│   └── Retail_Sales_Analysis.ipynb   # same analysis, notebook form, outputs included
├── outputs/                      # generated PNG charts land here
├── dashboard/                    # Django project (optional web integration)
│   ├── manage.py
│   ├── dashboard_project/        # settings, urls
│   ├── analytics_app/            # view + template that reads the cleaned CSV
│   └── static/charts/            # copies of the chart PNGs Django serves
└── requirements.txt
```

---

## How to run it (step by step)

### 1. Set up the environment

```bash
cd retail_sales_analytics
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Generate the dataset

```bash
python data/generate_data.py
```
Creates `data/retail_sales.csv` — ~8,000 rows of synthetic e-commerce orders
across 5 categories, 11 Indian cities, 4 regions, spanning 2023–2024.

### 3. Run the cleaning + EDA script

```bash
python analysis/eda.py
```
Cleans the data (drops duplicates, fills missing ratings by category median),
engineers new features, and prints a full analysis summary to the console.
Also saves `data/retail_sales_cleaned.csv`, which both the notebook and the
Django dashboard read from.

### 4. Generate the charts

```bash
python analysis/visualizations.py
```
Saves 8 PNG charts into `outputs/`.

### 5. (Optional) Open the Jupyter notebook

```bash
jupyter notebook notebook/Retail_Sales_Analysis.ipynb
```
Same analysis as steps 3–4, in notebook form with explanations and outputs
already baked in — good for a quick visual walkthrough or GitHub preview.

### 6. (Optional) Run the Django dashboard

```bash
cd dashboard
python manage.py migrate
python manage.py runserver
```
Open **http://127.0.0.1:8000/** in your browser. The dashboard reads
`data/retail_sales_cleaned.csv` (from step 3) and renders KPI cards, summary
tables, and the 8 charts as a single web page.

> If you regenerate the charts (step 4), re-copy them into
> `dashboard/static/charts/` so the Django app picks up the latest versions:
> `cp outputs/*.png dashboard/static/charts/`

---

## Sample insights the analysis surfaces

- Electronics drives the largest share of total revenue despite fewer orders,
  since unit prices are far higher than other categories
- North and West regions lead in total revenue; South has the highest order
  count, suggesting more frequent, lower-value purchases there
- Revenue rises in Oct–Dec, consistent with a festive/holiday shopping effect
- Loyal customers contribute disproportionately to revenue relative to their
  share of orders

*(These are illustrative — they come from the synthetic dataset. Swap in a
real dataset with the same column names and the same scripts will produce
real insights.)*

---

## Using your own data instead

Skip `generate_data.py` and drop your own CSV at `data/retail_sales.csv` with
these columns, then run steps 3–6 as normal:

```
order_id, order_date, category, product, city, region, quantity,
unit_price, discount_pct, revenue, payment_mode, customer_segment,
customer_rating
```

---

## Resume bullet points (edit to taste)

- Built an end-to-end retail sales analytics pipeline in Python (Pandas,
  NumPy) covering data cleaning, feature engineering, and exploratory
  analysis on an 8,000-row transactional dataset
- Designed 8 Matplotlib/Seaborn visualizations (trend, distribution,
  correlation, and comparison charts) to surface revenue, regional, and
  customer-segment insights
- Integrated the analysis into a Django web application that serves a live
  KPI dashboard from the processed dataset, connecting the data layer to a
  working full-stack interface
- Documented and packaged the project with a reproducible setup (README,
  requirements.txt, notebook) for portfolio/GitHub presentation

---

## Next step (Part 2, later)

A Power BI version of this same dataset — same KPIs, more interactive
filtering/drill-down — as a companion piece to show both a code-first and a
BI-tool-first approach to the same problem.
