"""
eda.py
-------
Loads matches.csv + player_performances.csv, cleans the performance data,
merges in match context, and prints a full analysis summary.

Usage:
    python analysis/eda.py
"""

import numpy as np
import pandas as pd

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 130)


def load_and_clean():
    matches = pd.read_csv("data/matches.csv", parse_dates=["date"])
    perf = pd.read_csv("data/player_performances.csv", parse_dates=["date"])

    print("=" * 60)
    print("MATCHES SHAPE:", matches.shape)
    print("PERFORMANCES SHAPE:", perf.shape)
    print("DUPLICATE PERFORMANCE ROWS:", perf.duplicated().sum())
    print("MISSING VALUES (performances):\n", perf.isnull().sum())
    print("=" * 60)

    perf = perf.drop_duplicates()

    # Fill missing strike rate with role-level median (a bowler with 0 balls faced
    # legitimately has no strike rate, so only impute where balls_faced > 0)
    mask = (perf["balls_faced"] > 0) & (perf["strike_rate"].isnull())
    perf.loc[mask, "strike_rate"] = perf.groupby("role")["strike_rate"].transform(
        lambda x: x.fillna(x.median())
    )[mask]

    # Merge match context (venue, winner) onto performances for venue-level analysis
    merged = perf.merge(
        matches[["match_id", "venue", "winner", "toss_winner", "toss_decision"]],
        on="match_id", how="left"
    )

    return matches, perf, merged


def summary_stats(matches, perf, merged):
    print("\n--- TOP 10 RUN SCORERS (career) ---")
    print(perf.groupby("player_name")["runs_scored"].sum().sort_values(ascending=False).head(10))

    print("\n--- TOP 10 WICKET TAKERS (career) ---")
    print(perf.groupby("player_name")["wickets_taken"].sum().sort_values(ascending=False).head(10))

    print("\n--- BEST STRIKE RATES (min 300 career balls faced) ---")
    balls = perf.groupby("player_name")["balls_faced"].sum()
    runs = perf.groupby("player_name")["runs_scored"].sum()
    qualified = balls[balls >= 300].index
    sr = (runs[qualified] / balls[qualified] * 100).sort_values(ascending=False)
    print(sr.round(2).head(10))

    print("\n--- BEST ECONOMY (min 30 career overs bowled) ---")
    overs = perf.groupby("player_name")["overs_bowled"].sum()
    conceded = perf.groupby("player_name")["runs_conceded"].sum()
    qualified_b = overs[overs >= 30].index
    econ = (conceded[qualified_b] / overs[qualified_b]).sort_values()
    print(econ.round(2).head(10))

    print("\n--- TEAM WIN COUNTS ---")
    print(matches["winner"].value_counts())

    print("\n--- TOSS DECISION IMPACT ON WIN ---")
    matches["toss_winner_won"] = matches["toss_winner"] == matches["winner"]
    print(matches.groupby("toss_decision")["toss_winner_won"].mean().round(3))

    print("\n--- AVG TEAM SCORE BY VENUE ---")
    venue_scores = pd.concat([
        matches[["venue", "team1_score"]].rename(columns={"team1_score": "score"}),
    ])
    print(venue_scores.groupby("venue")["score"].mean().sort_values(ascending=False).round(1))

    print("\n--- RUNS PER SEASON (league total) ---")
    print(perf.groupby("season")["runs_scored"].sum())

    print("\n--- ROLE-WISE AVG STRIKE RATE ---")
    print(perf.groupby("role")["strike_rate"].mean().round(2))


if __name__ == "__main__":
    matches, perf, merged = load_and_clean()
    summary_stats(matches, perf, merged)
    perf.to_csv("data/player_performances_cleaned.csv", index=False)
    matches.to_csv("data/matches_cleaned.csv", index=False)
    print("\nCleaned datasets saved -> data/player_performances_cleaned.csv, data/matches_cleaned.csv")
