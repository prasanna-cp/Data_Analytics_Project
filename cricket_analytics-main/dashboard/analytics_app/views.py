import pandas as pd
from django.conf import settings
from django.shortcuts import render


def dashboard(request):
    """
    Loads the two cleaned CSVs (matches, player performances) and computes
    the KPIs / tables shown on the dashboard. Same pattern as the analysis
    scripts: this view is just another consumer of the cleaned data contract.
    """
    matches_path = settings.MATCHES_CSV_PATH
    perf_path = settings.PERFORMANCES_CSV_PATH

    if not matches_path.exists() or not perf_path.exists():
        return render(request, "analytics_app/missing_data.html",
                       {"matches_path": str(matches_path), "perf_path": str(perf_path)})

    matches = pd.read_csv(matches_path, parse_dates=["date"])
    perf = pd.read_csv(perf_path, parse_dates=["date"])

    total_runs = int(perf["runs_scored"].sum())
    total_wickets = int(perf["wickets_taken"].sum())
    top_scorer = perf.groupby("player_name")["runs_scored"].sum().idxmax()
    top_scorer_runs = int(perf.groupby("player_name")["runs_scored"].sum().max())
    top_bowler = perf.groupby("player_name")["wickets_taken"].sum().idxmax()
    top_bowler_wkts = int(perf.groupby("player_name")["wickets_taken"].sum().max())

    kpis = {
        "total_matches": f"{len(matches):,}",
        "total_runs": f"{total_runs:,}",
        "total_wickets": f"{total_wickets:,}",
        "top_scorer": f"{top_scorer} ({top_scorer_runs} runs)",
        "top_bowler": f"{top_bowler} ({top_bowler_wkts} wkts)",
    }

    top_run_scorers = (
        perf.groupby("player_name")["runs_scored"].sum().sort_values(ascending=False).head(5)
    )
    top_wicket_takers = (
        perf.groupby("player_name")["wickets_taken"].sum().sort_values(ascending=False).head(5)
    )
    team_wins = matches["winner"].value_counts()

    context = {
        "kpis": kpis,
        "top_run_scorers": top_run_scorers.items(),
        "top_wicket_takers": top_wicket_takers.items(),
        "team_wins": team_wins.items(),
        "chart_files": [
            "01_top_run_scorers.png",
            "02_top_wicket_takers.png",
            "03_team_wins.png",
            "04_toss_impact.png",
            "05_strike_rate_vs_runs.png",
            "06_runs_by_season.png",
            "07_venue_avg_score.png",
            "08_economy_by_role.png",
        ],
    }
    return render(request, "analytics_app/dashboard.html", context)
