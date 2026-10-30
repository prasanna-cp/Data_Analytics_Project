"""
visualizations.py
-------------------
Generates 8 charts from the cleaned cricket datasets and saves them to outputs/.
Run eda.py first to produce the cleaned CSVs.

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
    matches = pd.read_csv("data/matches_cleaned.csv", parse_dates=["date"])
    perf = pd.read_csv("data/player_performances_cleaned.csv", parse_dates=["date"])
    return matches, perf


def chart_top_run_scorers(perf):
    top = perf.groupby("player_name")["runs_scored"].sum().sort_values(ascending=False).head(10).reset_index()
    plt.figure(figsize=(9, 6))
    sns.barplot(data=top, x="runs_scored", y="player_name", hue="player_name", legend=False, palette="viridis")
    plt.title("Top 10 Run Scorers (All Seasons)", fontsize=14, weight="bold")
    plt.xlabel("Total Runs")
    plt.ylabel("")
    plt.tight_layout()
    plt.savefig(f"{OUT_DIR}/01_top_run_scorers.png")
    plt.close()


def chart_top_wicket_takers(perf):
    top = perf.groupby("player_name")["wickets_taken"].sum().sort_values(ascending=False).head(10).reset_index()
    plt.figure(figsize=(9, 6))
    sns.barplot(data=top, x="wickets_taken", y="player_name", hue="player_name", legend=False, palette="mako")
    plt.title("Top 10 Wicket Takers (All Seasons)", fontsize=14, weight="bold")
    plt.xlabel("Total Wickets")
    plt.ylabel("")
    plt.tight_layout()
    plt.savefig(f"{OUT_DIR}/02_top_wicket_takers.png")
    plt.close()


def chart_team_wins(matches):
    wins = matches["winner"].value_counts().reset_index()
    wins.columns = ["team", "wins"]
    plt.figure(figsize=(9, 6))
    sns.barplot(data=wins, x="wins", y="team", hue="team", legend=False, palette="crest")
    plt.title("Total Match Wins by Team", fontsize=14, weight="bold")
    plt.xlabel("Wins")
    plt.ylabel("")
    plt.tight_layout()
    plt.savefig(f"{OUT_DIR}/03_team_wins.png")
    plt.close()


def chart_toss_impact(matches):
    matches = matches.copy()
    matches["toss_winner_won"] = matches["toss_winner"] == matches["winner"]
    impact = matches.groupby("toss_decision")["toss_winner_won"].mean().mul(100).reset_index()
    plt.figure(figsize=(6, 5))
    sns.barplot(data=impact, x="toss_decision", y="toss_winner_won", hue="toss_decision", legend=False, palette="flare")
    plt.title("Win % When Toss Winner Chooses to Bat/Field", fontsize=13, weight="bold")
    plt.xlabel("")
    plt.ylabel("Toss Winner Win Rate (%)")
    plt.ylim(0, 100)
    plt.tight_layout()
    plt.savefig(f"{OUT_DIR}/04_toss_impact.png")
    plt.close()


def chart_strike_rate_vs_runs(perf):
    agg = perf.groupby("player_name").agg(
        total_runs=("runs_scored", "sum"), avg_sr=("strike_rate", "mean"), role=("role", "first")
    ).reset_index()
    agg = agg[agg["total_runs"] > 100]
    plt.figure(figsize=(9, 6))
    sns.scatterplot(data=agg, x="avg_sr", y="total_runs", hue="role", s=60, palette="deep")
    plt.title("Strike Rate vs Total Runs (Career, min 100 runs)", fontsize=14, weight="bold")
    plt.xlabel("Average Strike Rate")
    plt.ylabel("Total Runs")
    plt.tight_layout()
    plt.savefig(f"{OUT_DIR}/05_strike_rate_vs_runs.png")
    plt.close()


def chart_runs_by_season(perf):
    season_runs = perf.groupby("season")["runs_scored"].sum().reset_index()
    plt.figure(figsize=(8, 5))
    sns.lineplot(data=season_runs, x="season", y="runs_scored", marker="o", linewidth=2)
    plt.title("Total League Runs by Season", fontsize=14, weight="bold")
    plt.xlabel("Season")
    plt.ylabel("Total Runs")
    plt.xticks(season_runs["season"])
    plt.tight_layout()
    plt.savefig(f"{OUT_DIR}/06_runs_by_season.png")
    plt.close()


def chart_venue_avg_score(matches):
    venue_scores = matches.groupby("venue")["team1_score"].mean().sort_values(ascending=False).reset_index()
    plt.figure(figsize=(9, 6))
    sns.barplot(data=venue_scores, x="team1_score", y="venue", hue="venue", legend=False, palette="magma")
    plt.title("Average First-Innings Score by Venue", fontsize=14, weight="bold")
    plt.xlabel("Avg Score")
    plt.ylabel("")
    plt.tight_layout()
    plt.savefig(f"{OUT_DIR}/07_venue_avg_score.png")
    plt.close()


def chart_economy_by_role(perf):
    bowlers = perf[perf["overs_bowled"] > 0]
    plt.figure(figsize=(8, 5))
    sns.boxplot(data=bowlers, x="role", y="economy", hue="role", legend=False, palette="rocket")
    plt.title("Economy Rate Distribution by Role", fontsize=14, weight="bold")
    plt.xlabel("")
    plt.ylabel("Economy (runs/over)")
    plt.tight_layout()
    plt.savefig(f"{OUT_DIR}/08_economy_by_role.png")
    plt.close()


if __name__ == "__main__":
    matches, perf = load()
    chart_top_run_scorers(perf)
    chart_top_wicket_takers(perf)
    chart_team_wins(matches)
    chart_toss_impact(matches)
    chart_strike_rate_vs_runs(perf)
    chart_runs_by_season(perf)
    chart_venue_avg_score(matches)
    chart_economy_by_role(perf)
    print("8 charts saved to outputs/")
