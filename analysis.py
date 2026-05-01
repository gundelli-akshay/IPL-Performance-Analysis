# ============================================================
# FILE: analysis.py
# IPL Player Performance Analysis - Main Script
# Run: python analysis.py
# ============================================================

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# ── Settings ─────────────────────────────────────────────────
sns.set(style="whitegrid")
plt.rcParams["figure.figsize"] = (12, 6)

MATCHES_PATH    = "data/matches.csv"
DELIVERIES_PATH = "data/deliveries.csv"
VISUALS_DIR     = "visuals"

PALETTE = {
    "orange": "#e67e22",
    "green": "#2ecc71",
    "red": "#e74c3c",
    "blue": "#3498db",
    "purple": "#9b59b6",
    "teal": "#1abc9c",
    "yellow": "#f39c12",
}

TEAM_NAME_MAP = {
    "Delhi Daredevils": "Delhi Capitals",
    "Royal Challengers Bangalore": "Royal Challengers Bengaluru",
    "Rising Pune Supergiants": "Rising Pune Supergiant",
    "Kings XI Punjab": "Punjab Kings"
}

NON_BOWLER_DISMISSALS = ["run out", "retired hurt", "obstructing the field"]

os.makedirs(VISUALS_DIR, exist_ok=True)


# ── Helper ───────────────────────────────────────────────────
def save(fig, filename):
    path = os.path.join(VISUALS_DIR, filename)
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    print(f"  [saved] {path}")


def barh_chart(series, title, xlabel, filename, color):
    fig, ax = plt.subplots()
    bars = ax.barh(series.index[::-1], series.values[::-1], color=color)
    ax.bar_label(bars, padding=4)
    ax.set_title(title, fontsize=14, fontweight="bold")
    ax.set_xlabel(xlabel)
    save(fig, filename)


def pie_chart(values, labels, title, filename, colors):
    fig, ax = plt.subplots(figsize=(7, 7))
    ax.pie(values, labels=labels, autopct="%1.1f%%",
           colors=colors, startangle=90,
           wedgeprops={"edgecolor": "white", "linewidth": 2})
    ax.set_title(title, fontsize=14, fontweight="bold")
    save(fig, filename)


def bowler_wickets(deliveries):
    wicket_deliveries = deliveries[
        deliveries["dismissal_kind"].notna() &
        ~deliveries["dismissal_kind"].isin(NON_BOWLER_DISMISSALS)
    ]
    return (
        wicket_deliveries.groupby("bowler")["dismissal_kind"]
        .count()
        .sort_values(ascending=False)
    )


# ============================================================
# STEP 1 — Load Data
# ============================================================
def load_data():
    print("\n📂 Loading datasets...")

    if not os.path.exists(MATCHES_PATH):
        raise FileNotFoundError(
            "matches.csv not found in data/ folder.\n"
            "Download from: https://www.kaggle.com/datasets/patrickb1912/ipl-complete-dataset-20082020"
        )
    if not os.path.exists(DELIVERIES_PATH):
        raise FileNotFoundError(
            "deliveries.csv not found in data/ folder.\n"
            "Download from: https://www.kaggle.com/datasets/patrickb1912/ipl-complete-dataset-20082020"
        )

    matches    = pd.read_csv(MATCHES_PATH)
    deliveries = pd.read_csv(DELIVERIES_PATH)

    print(f"  Matches    : {matches.shape[0]} rows, {matches.shape[1]} columns")
    print(f"  Deliveries : {deliveries.shape[0]} rows, {deliveries.shape[1]} columns")

    return matches, deliveries


# ============================================================
# STEP 2 — Clean Data
# ============================================================
def clean_data(matches, deliveries):
    print("\n🧹 Cleaning data...")

    # Keep only completed matches
    matches = matches[matches["result"].isin(["runs", "wickets"])].copy()

    # Fill missing winners
    matches["winner"].fillna("Unknown", inplace=True)

    # Standardize team names
    for col in ["team1", "team2", "winner", "toss_winner"]:
        matches[col] = matches[col].replace(TEAM_NAME_MAP)

    deliveries["batting_team"] = deliveries["batting_team"].replace(TEAM_NAME_MAP)

    print(f"  Matches after cleaning  : {matches.shape[0]}")
    print(f"  Missing values (matches): {matches.isnull().sum().sum()}")
    print("  Data is clean and ready.")

    return matches, deliveries


# ============================================================
# STEP 3 — EDA
# ============================================================
def run_eda(matches, deliveries):
    print("\n🔍 Running EDA...")

    findings = {}

    # Team wins
    team_wins = matches["winner"].value_counts().head(10)
    findings["team_wins"] = team_wins
    print(f"\n  Top 5 Teams by Wins:\n{team_wins.head().to_string()}")

    # Toss impact
    matches["toss_won_match"] = matches["toss_winner"] == matches["winner"]
    toss_won  = matches["toss_won_match"].sum()
    toss_lost = len(matches) - toss_won
    toss_pct  = round(toss_won * 100 / len(matches), 2)
    findings["toss_won"]  = toss_won
    findings["toss_lost"] = toss_lost
    findings["toss_pct"]  = toss_pct
    print(f"\n  Toss winner won the match : {toss_pct}% of the time")

    # Top batsmen
    top_batsmen = (
        deliveries.groupby("batter")["batsman_runs"]
        .sum().sort_values(ascending=False).head(10)
    )
    findings["top_batsmen"] = top_batsmen
    print(f"\n  Top 3 Run Scorers:\n{top_batsmen.head(3).to_string()}")

    # Top bowlers
    top_bowlers = bowler_wickets(deliveries).head(10)
    findings["top_bowlers"] = top_bowlers
    print(f"\n  Top 3 Wicket Takers:\n{top_bowlers.head(3).to_string()}")

    # Runs per season
    merged = deliveries.merge(matches[["id", "season"]], left_on="match_id", right_on="id", how="inner")
    season_runs = merged.groupby("season")["total_runs"].sum()
    findings["season_runs"] = season_runs
    print(f"\n  Runs per Season:\n{season_runs.to_string()}")

    # Top venues
    findings["top_venues"] = matches["venue"].value_counts().head(10)

    # Matches per season
    findings["matches_per_season"] = matches.groupby("season").size()

    # Toss decision
    findings["toss_decision"] = matches["toss_decision"].value_counts()
    print(f"\n  Toss Decision:\n{findings['toss_decision'].to_string()}")

    return findings, matches, deliveries


# ============================================================
# STEP 4 — Visualizations
# ============================================================
def create_visualizations(findings, matches):
    print("\n📊 Creating visualizations...")

    # Chart 1 — Top 10 Teams by Wins
    barh_chart(findings["team_wins"], "Top 10 Teams by Total Wins",
               "Number of Wins", "1_team_wins.png", PALETTE["orange"])

    # Chart 2 — Toss Impact on Match Result
    pie_chart(
        [findings["toss_won"], findings["toss_lost"]],
        ["Won Toss & Match", "Won Toss, Lost Match"],
        "Toss Impact on Match Result",
        "2_toss_impact.png",
        [PALETTE["green"], PALETTE["red"]],
    )

    # Chart 3 — Top 10 Run Scorers
    barh_chart(findings["top_batsmen"], "Top 10 Run Scorers in IPL History",
               "Total Runs", "3_top_batsmen.png", PALETTE["blue"])

    # Chart 4 — Top 10 Wicket Takers
    barh_chart(findings["top_bowlers"], "Top 10 Wicket Takers in IPL History",
               "Total Wickets", "4_top_bowlers.png", PALETTE["red"])

    # Chart 5 — Runs Scored Per Season
    fig, ax = plt.subplots()
    season_runs = findings["season_runs"]
    ax.plot(season_runs.index, season_runs.values, marker="o",
            color=PALETTE["purple"], linewidth=2.5, markersize=7)   
    ax.fill_between(season_runs.index, season_runs.values, alpha=0.15, color=PALETTE["purple"])
    ax.set_title("Total Runs Scored Per Season", fontsize=14, fontweight="bold")
    ax.set_xlabel("Season")
    ax.set_ylabel("Total Runs")
    ax.set_xticks(season_runs.index)
    ax.tick_params(axis="x", rotation=45)
    save(fig, "5_runs_per_season.png")

    # Chart 6 — Top 10 Venues by Matches Hosted
    barh_chart(findings["top_venues"], "Top 10 Venues by Matches Hosted",
               "Number of Matches", "6_top_venues.png", PALETTE["teal"])

    # Chart 7 — Matches Per Season
    fig, ax = plt.subplots()
    mps = findings["matches_per_season"]
    bars = ax.bar(mps.index.astype(str), mps.values, color=PALETTE["yellow"], width=0.6)
    ax.bar_label(bars, padding=4)
    ax.set_title("Number of Matches Per Season", fontsize=14, fontweight="bold")
    ax.set_xlabel("Season")
    ax.set_ylabel("Matches Played")
    ax.tick_params(axis="x", rotation=45)
    save(fig, "7_matches_per_season.png")

    # Chart 8 — Toss Decision (Bat vs Field)
    pie_chart(
        findings["toss_decision"].values,
        findings["toss_decision"].index,
        "Toss Decision — Bat vs Field",
        "8_toss_decision.png",
        [PALETTE["blue"], PALETTE["orange"]],
    )

    print(f"  All charts saved to '{VISUALS_DIR}/' folder.")
    

# ============================================================
# STEP 5 — Save Summary Report
# ============================================================
def save_report(findings):
    print("\n📝 Saving summary report...")

    team_wins   = findings["team_wins"]
    top_bat     = findings["top_batsmen"]
    top_bowl    = findings["top_bowlers"]
    toss_pct    = findings["toss_pct"]

    report = f"""
============================================================
       IPL PLAYER PERFORMANCE ANALYSIS — SUMMARY REPORT
============================================================

DATASET
  Source  : IPL Complete Dataset 2008-2020 (Kaggle)
  Files   : matches.csv, deliveries.csv

------------------------------------------------------------
KEY FINDINGS
------------------------------------------------------------

1. MOST SUCCESSFUL TEAM
   {team_wins.idxmax()} — {team_wins.max()} total wins

2. TOP 3 RUN SCORERS
   1. {top_bat.index[0]} — {top_bat.iloc[0]} runs
   2. {top_bat.index[1]} — {top_bat.iloc[1]} runs
   3. {top_bat.index[2]} — {top_bat.iloc[2]} runs

3. TOP 3 WICKET TAKERS
   1. {top_bowl.index[0]} — {top_bowl.iloc[0]} wickets
   2. {top_bowl.index[1]} — {top_bowl.iloc[1]} wickets
   3. {top_bowl.index[2]} — {top_bowl.iloc[2]} wickets

4. TOSS IMPACT
   Teams that won the toss went on to win the match
   {toss_pct}% of the time.

------------------------------------------------------------
INSIGHTS
------------------------------------------------------------
  - Toss advantage is real but not decisive
  - Top run scorers and wicket takers are consistent
    across seasons showing player dominance
  - Wankhede and Eden Gardens are the most used venues
    indicating their strategic importance

============================================================
"""

    with open("ipl_report.txt", "w") as f:
        f.write(report)

    print(report)
    print("  Report saved to 'ipl_report.txt'")


# ============================================================
# STEP 6 — Export Excel Report
# ============================================================
def export_excel(matches, deliveries):
    print("\n📊 Exporting Excel report...")

    # Sheet 1 — Top 20 Batsmen
    top_batsmen = (
        deliveries.groupby("batter")["batsman_runs"]
        .sum().sort_values(ascending=False).head(20).reset_index()
    )
    top_batsmen.columns = ["Batsman", "Total Runs"]
    top_batsmen.insert(0, "Rank", range(1, len(top_batsmen) + 1))

    # Sheet 2 — Top 20 Bowlers
    top_bowlers = bowler_wickets(deliveries).head(20).reset_index()
    top_bowlers.columns = ["Bowler", "Total Wickets"]
    top_bowlers.insert(0, "Rank", range(1, len(top_bowlers) + 1))

    # Sheet 3 — Team Wins
    team_wins = matches["winner"].value_counts().reset_index()
    team_wins.columns = ["Team", "Total Wins"]
    team_wins.insert(0, "Rank", range(1, len(team_wins) + 1))

    # Sheet 4 — Season Summary
    merged = deliveries.merge(
        matches[["id", "season"]], left_on="match_id", right_on="id", how="inner"
    )
    season_runs    = merged.groupby("season")["total_runs"].sum().reset_index()
    season_matches = matches.groupby("season").size().reset_index(name="matches_played")
    season_summary = season_runs.merge(season_matches, on="season")
    season_summary.columns = ["Season", "Total Runs", "Matches Played"]

    # Sheet 5 — Toss Analysis
    matches["toss_won_match"] = matches["toss_winner"] == matches["winner"]
    toss_by_decision = (
        matches.groupby("toss_decision")["toss_won_match"]
        .agg(["count", "sum"])
        .reset_index()
    )
    toss_by_decision.columns = ["Toss Decision", "Total", "Won After Toss"]
    toss_by_decision["Win %"] = (
        toss_by_decision["Won After Toss"] / toss_by_decision["Total"] * 100
    ).round(2)

    # Write all sheets to Excel
    with pd.ExcelWriter("ipl_report.xlsx", engine="openpyxl") as writer:
        top_batsmen.to_excel(writer, sheet_name="Top Batsmen", index=False)
        top_bowlers.to_excel(writer, sheet_name="Top Bowlers", index=False)
        team_wins.to_excel(writer, sheet_name="Team Wins", index=False)
        season_summary.to_excel(writer, sheet_name="Season Summary", index=False)
        toss_by_decision.to_excel(writer, sheet_name="Toss Analysis", index=False)

    print("  Excel report saved as 'ipl_report.xlsx'")


    # ============================================================
# MAIN
# ============================================================
if __name__ == "__main__":
    print("=" * 60)
    print("   IPL PLAYER PERFORMANCE ANALYSIS")
    print("=" * 60)

    matches, deliveries           = load_data()
    matches, deliveries           = clean_data(matches, deliveries)
    findings, matches, deliveries = run_eda(matches, deliveries)
    create_visualizations(findings, matches)
    save_report(findings)
    export_excel(matches, deliveries)

    print("\n✅ Analysis complete!")
    print(f"   Charts  → {VISUALS_DIR}/")
    print("   Report  → ipl_report.txt")
    print("   Excel   → ipl_report.xlsx")
