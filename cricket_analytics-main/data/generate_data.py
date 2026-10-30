"""
generate_data.py
-----------------
Generates a synthetic T20 league dataset: match results + per-player
batting/bowling performances across 4 seasons. Two linked tables
(matches.csv + player_performances.csv) so the analysis can demonstrate
merges/joins as well as aggregation.

All team, player, and venue names are fictional.

Usage:
    python data/generate_data.py
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta

np.random.seed(7)

# ---------------------------------------------------------
# Config
# ---------------------------------------------------------
SEASONS = [2021, 2022, 2023, 2024]
MATCHES_PER_SEASON = 60

TEAMS = [
    "Mumbai Monarchs", "Chennai Chargers", "Bengaluru Blasters", "Kolkata Cobras",
    "Delhi Dragons", "Punjab Panthers", "Jaipur Jaguars", "Hyderabad Hurricanes",
]

VENUES = {
    "Mumbai Monarchs": "Coastal Arena, Mumbai",
    "Chennai Chargers": "Riverside Ground, Chennai",
    "Bengaluru Blasters": "Skyline Stadium, Bengaluru",
    "Kolkata Cobras": "Lake View Ground, Kolkata",
    "Delhi Dragons": "Capital Arena, Delhi",
    "Punjab Panthers": "Panthers Park, Mohali",
    "Jaipur Jaguars": "Desert Stadium, Jaipur",
    "Hyderabad Hurricanes": "Deccan Arena, Hyderabad",
}

FIRST_NAMES = [
    "Arjun", "Rohan", "Vikram", "Karan", "Aditya", "Rahul", "Suresh", "Manoj",
    "Deepak", "Ajay", "Naveen", "Sanjay", "Vivek", "Rajesh", "Anil", "Prakash",
    "Harish", "Gaurav", "Nikhil", "Siddharth", "Yash", "Rohit", "Varun", "Amit",
]
LAST_NAMES = [
    "Sharma", "Verma", "Iyer", "Reddy", "Nair", "Gupta", "Menon", "Rao",
    "Chauhan", "Malhotra", "Kulkarni", "Joshi", "Pillai", "Bhat", "Desai", "Singh",
]

ROLES = ["Batter", "Bowler", "All-rounder", "Wicketkeeper"]


def build_squads():
    """Give every team a fixed 18-player squad with assigned roles."""
    squads = {}
    used_names = set()
    for team in TEAMS:
        squad = []
        while len(squad) < 18:
            name = f"{np.random.choice(FIRST_NAMES)} {np.random.choice(LAST_NAMES)}"
            if name in used_names:
                continue
            used_names.add(name)
            role = np.random.choice(ROLES, p=[0.4, 0.3, 0.2, 0.1])
            # skill ratings drive performance distributions per player
            batting_skill = np.clip(np.random.normal(60, 15), 20, 95)
            bowling_skill = np.clip(np.random.normal(60, 15), 20, 95)
            if role == "Batter":
                bowling_skill *= 0.3
            elif role == "Bowler":
                batting_skill *= 0.4
            elif role == "Wicketkeeper":
                bowling_skill *= 0.1
            squad.append({
                "name": name, "team": team, "role": role,
                "batting_skill": batting_skill, "bowling_skill": bowling_skill,
            })
        squads[team] = squad
    return squads


def simulate_innings_batting(squad, target_runs):
    """Distribute a team's total runs across ~7-8 batters based on skill."""
    batters = sorted(squad, key=lambda p: -p["batting_skill"])[:9]
    weights = np.array([p["batting_skill"] for p in batters]) ** 1.5
    weights = weights / weights.sum()
    raw_runs = np.random.dirichlet(weights * 10) * target_runs

    perf = []
    for player, runs in zip(batters, raw_runs):
        runs = max(0, int(round(runs)))
        if runs == 0 and np.random.rand() < 0.5:
            balls = np.random.randint(1, 5)
        else:
            sr_base = 100 + (player["batting_skill"] - 50) * 1.3
            balls = max(1, int(round(runs / (sr_base / 100))))
        fours = min(runs // 4, np.random.poisson(max(runs, 1) / 12))
        sixes = min((runs - fours * 4) // 6, np.random.poisson(max(runs, 1) / 20))
        perf.append({
            "name": player["name"], "role": player["role"],
            "runs_scored": runs, "balls_faced": balls, "fours": int(fours), "sixes": int(sixes),
        })
    return perf


def simulate_innings_bowling(squad, wickets_fallen, overs=20):
    """Distribute wickets and overs among ~5-6 bowlers based on skill."""
    bowlers = sorted(squad, key=lambda p: -p["bowling_skill"])[:6]
    weights = np.array([p["bowling_skill"] for p in bowlers]) ** 1.3
    weights = weights / weights.sum()
    wicket_dist = np.random.multinomial(wickets_fallen, weights)

    overs_left = overs
    perf = []
    for i, (player, wkts) in enumerate(zip(bowlers, wicket_dist)):
        max_overs = 4
        ov = min(max_overs, max(1, overs_left // max(1, (len(bowlers) - i))))
        overs_left -= ov
        economy_base = 9.5 - (player["bowling_skill"] - 50) * 0.05
        economy = max(3.5, np.random.normal(economy_base, 1.3))
        runs_conceded = int(round(economy * ov))
        perf.append({
            "name": player["name"], "role": player["role"],
            "overs_bowled": ov, "runs_conceded": runs_conceded, "wickets_taken": int(wkts),
        })
    return perf


def generate():
    squads = build_squads()
    matches = []
    performances = []
    match_id_counter = 1

    for season in SEASONS:
        season_start = datetime(season, 3, 25)
        used_pairs = set()
        for i in range(MATCHES_PER_SEASON):
            team1, team2 = np.random.choice(TEAMS, size=2, replace=False)
            match_id = f"M{match_id_counter:04d}"
            match_id_counter += 1
            match_date = season_start + timedelta(days=int(i * 3.5))
            venue = VENUES[team1]

            toss_winner = np.random.choice([team1, team2])
            toss_decision = np.random.choice(["Bat", "Field"], p=[0.55, 0.45])

            team1_score = int(np.clip(np.random.normal(165, 22), 90, 240))
            team2_score = int(np.clip(np.random.normal(165, 22), 90, 240))
            team1_wkts_lost = np.random.randint(3, 11)
            team2_wkts_lost = np.random.randint(3, 11)

            if team1_score == team2_score:
                team1_score += 1  # avoid ties for simplicity

            winner = team1 if team1_score > team2_score else team2
            if winner == team1:
                margin_type = "runs"
                margin = team1_score - team2_score
            else:
                margin_type = "wickets"
                margin = 10 - team2_wkts_lost

            matches.append({
                "match_id": match_id, "season": season, "date": match_date.strftime("%Y-%m-%d"),
                "venue": venue, "team1": team1, "team2": team2,
                "toss_winner": toss_winner, "toss_decision": toss_decision,
                "team1_score": team1_score, "team2_score": team2_score,
                "winner": winner, "margin": margin, "margin_type": margin_type,
            })

            # Batting performances
            bat1 = simulate_innings_batting(squads[team1], team1_score)
            bat2 = simulate_innings_batting(squads[team2], team2_score)
            # Bowling performances (team2 bowls at team1's innings and vice versa)
            bowl_vs1 = simulate_innings_bowling(squads[team2], team1_wkts_lost)
            bowl_vs2 = simulate_innings_bowling(squads[team1], team2_wkts_lost)

            def merge_perf(batting, bowling, team):
                combined = {}
                for b in batting:
                    combined[b["name"]] = {**b, "team": team, "overs_bowled": 0,
                                            "runs_conceded": 0, "wickets_taken": 0}
                for b in bowling:
                    if b["name"] in combined:
                        combined[b["name"]]["overs_bowled"] = b["overs_bowled"]
                        combined[b["name"]]["runs_conceded"] = b["runs_conceded"]
                        combined[b["name"]]["wickets_taken"] = b["wickets_taken"]
                    else:
                        combined[b["name"]] = {
                            "name": b["name"], "role": b["role"], "team": team,
                            "runs_scored": 0, "balls_faced": 0, "fours": 0, "sixes": 0,
                            "overs_bowled": b["overs_bowled"], "runs_conceded": b["runs_conceded"],
                            "wickets_taken": b["wickets_taken"],
                        }
                return list(combined.values())

            for row in merge_perf(bat1, bowl_vs1, team1):
                row.update({"match_id": match_id, "season": season, "date": match_date.strftime("%Y-%m-%d"),
                            "opponent": team2, "is_winner": (winner == team1)})
                performances.append(row)
            for row in merge_perf(bat2, bowl_vs2, team2):
                row.update({"match_id": match_id, "season": season, "date": match_date.strftime("%Y-%m-%d"),
                            "opponent": team1, "is_winner": (winner == team2)})
                performances.append(row)

    matches_df = pd.DataFrame(matches)
    perf_df = pd.DataFrame(performances)

    # derived batting/bowling metrics
    perf_df["strike_rate"] = np.where(
        perf_df["balls_faced"] > 0, round(perf_df["runs_scored"] / perf_df["balls_faced"] * 100, 2), np.nan
    )
    perf_df["economy"] = np.where(
        perf_df["overs_bowled"] > 0, round(perf_df["runs_conceded"] / perf_df["overs_bowled"], 2), np.nan
    )

    # inject a bit of realistic messiness
    missing_idx = np.random.choice(perf_df.index, size=int(0.015 * len(perf_df)), replace=False)
    perf_df.loc[missing_idx, "strike_rate"] = np.nan

    dup_idx = np.random.choice(perf_df.index, size=20, replace=False)
    perf_df = pd.concat([perf_df, perf_df.loc[dup_idx]], ignore_index=True)
    perf_df = perf_df.sample(frac=1, random_state=3).reset_index(drop=True)

    cols = ["match_id", "season", "date", "team", "opponent", "name", "role",
            "runs_scored", "balls_faced", "fours", "sixes", "strike_rate",
            "overs_bowled", "runs_conceded", "wickets_taken", "economy", "is_winner"]
    perf_df = perf_df[cols].rename(columns={"name": "player_name"})

    return matches_df, perf_df


if __name__ == "__main__":
    matches_df, perf_df = generate()
    matches_df.to_csv("data/matches.csv", index=False)
    perf_df.to_csv("data/player_performances.csv", index=False)
    print(f"Generated {len(matches_df)} matches -> data/matches.csv")
    print(f"Generated {len(perf_df)} player performances -> data/player_performances.csv")
    print(matches_df.head())
    print(perf_df.head())
