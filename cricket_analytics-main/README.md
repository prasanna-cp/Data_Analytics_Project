# Cricket Analytics Dashboard

An end-to-end data analytics project: synthetic T20 league dataset → data
cleaning + merging → exploratory analysis → visualization → a Django web
dashboard that serves the results. Built to be resume-ready and
GitHub-presentable.

**Stack:** Python, NumPy, Pandas, Matplotlib, Seaborn, Django, Jupyter

> All team names, player names, and venues in this dataset are fictional.

---

## What this project shows

- Working with **two linked tables** (matches + player performances) and
  merging them with pandas — a step up from single-table analysis
- Cleaning realistic messy data (duplicates, role-aware missing value handling
  — a bowler with 0 balls faced legitimately has no strike rate, so it isn't
  blindly imputed)
- Career-level aggregation with qualification thresholds (e.g. best strike
  rate among players with 300+ career balls faced — mirrors how real cricket
  stats are reported)
- 8 chart types with Matplotlib/Seaborn (bar, scatter, boxplot, line)
- A Jupyter notebook version with outputs already baked in
- A Django web app reading the cleaned CSVs and rendering a live stats
  dashboard

---

## Folder structure

```
cricket_analytics/
├── data/
│   ├── generate_data.py                    # creates the synthetic dataset
│   ├── matches.csv                         # raw match results
│   ├── player_performances.csv             # raw per-player, per-match stats
│   ├── matches_cleaned.csv                 # created after step 2
│   └── player_performances_cleaned.csv     # created after step 2
├── analysis/
│   ├── eda.py                              # cleaning + merge + full EDA
│   └── visualizations.py                   # generates 8 charts into outputs/
├── notebook/
│   └── Cricket_Analytics.ipynb             # same analysis, notebook form
├── outputs/                                # generated PNG charts land here
├── dashboard/                              # Django project (optional web integration)
│   ├── manage.py
│   ├── dashboard_project/                  # settings, urls
│   ├── analytics_app/                      # view + template reading the cleaned CSVs
│   └── static/charts/                      # copies of the chart PNGs Django serves
└── requirements.txt
```

---

## How to run it (step by step)

### 1. Set up the environment

```bash
cd cricket_analytics
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Generate the dataset

```bash
python data/generate_data.py
```
Creates `data/matches.csv` (240 matches, 4 seasons, 8 teams) and
`data/player_performances.csv` (~7,200 individual batting/bowling
performances).

### 3. Run the cleaning + EDA script

```bash
python analysis/eda.py
```
Cleans both tables, merges match context onto performances, engineers
strike rate / economy, and prints a full stats summary — top scorers, top
wicket takers, toss impact on wins, venue scoring trends, and more. Saves
`data/matches_cleaned.csv` and `data/player_performances_cleaned.csv`, which
the notebook and Django dashboard both read from.

### 4. Generate the charts

```bash
python analysis/visualizations.py
```
Saves 8 PNG charts into `outputs/`.

### 5. (Optional) Open the Jupyter notebook

```bash
jupyter notebook notebook/Cricket_Analytics.ipynb
```
Same analysis in notebook form with outputs already baked in.

### 6. (Optional) Run the Django dashboard

```bash
cd dashboard
python manage.py migrate
python manage.py runserver
```
Open **http://127.0.0.1:8000/** — the dashboard reads the two cleaned CSVs
(from step 3) and renders KPI cards, leaderboards, and the 8 charts as a
single page.

> If you regenerate the charts (step 4), re-copy them into
> `dashboard/static/charts/`:
> `cp outputs/*.png dashboard/static/charts/`

---

## Sample insights the analysis surfaces

- A small core of top-order batters accounts for a disproportionate share of
  total runs — consistent with real T20 leagues
- Winning the toss and choosing to bat first correlates with a slightly
  higher win rate than choosing to field
- Wicketkeepers and all-rounders post the highest average strike rates,
  likely from batting in the aggressive middle-order slog overs
- Economy rate spreads wider among specialist bowlers than all-rounders

*(These come from the synthetic dataset. Point the same scripts at a real
ball-by-ball dataset with matching column names for live insights.)*

---

## Using your own data instead

Skip `generate_data.py` and drop your own CSVs at `data/matches.csv` and
`data/player_performances.csv` with these columns, then run steps 3–6:

**matches.csv:** `match_id, season, date, venue, team1, team2, toss_winner,
toss_decision, team1_score, team2_score, winner, margin, margin_type`

**player_performances.csv:** `match_id, season, date, team, opponent,
player_name, role, runs_scored, balls_faced, fours, sixes, strike_rate,
overs_bowled, runs_conceded, wickets_taken, economy, is_winner`

---

## Resume bullet points (edit to taste)

- Built an end-to-end cricket analytics pipeline in Python (Pandas, NumPy)
  covering data cleaning, table merging, and exploratory analysis across
  240 matches and 7,000+ player performances
- Designed 8 Matplotlib/Seaborn visualizations (leaderboards, distributions,
  correlation, trend) to surface batting, bowling, and team performance
  insights
- Integrated the analysis into a Django web application serving a live
  stats dashboard from the processed dataset
- Documented and packaged the project with a reproducible setup (README,
  requirements.txt, notebook) for portfolio/GitHub presentation

---

## Next step (Part 2, later)

A Power BI version of the same dataset — same KPIs and leaderboards, with
interactive filtering by season/team/venue — as a companion piece.
