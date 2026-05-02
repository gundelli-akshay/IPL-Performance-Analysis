# IPL Player Performance Analysis

A data analysis project to identify top performers, team win patterns, and toss impact across IPL seasons using Python, SQL, Excel, and Power BI.

---

## What This Project Does

- Loads and cleans ball-by-ball IPL match data
- Analyzes team wins, player performance, toss impact, and venue trends
- Creates 8 charts to visualize key findings
- Runs SQL queries for in-depth statistical analysis
- Exports a structured Excel report with 5 sheets
- Presents an interactive Power BI dashboard

---

## Dataset

- Source: IPL Complete Dataset from Kaggle
- Link: https://www.kaggle.com/datasets/patrickb1912/ipl-complete-dataset-20082020
- matches.csv: 1,076 completed matches
- deliveries.csv: 260,920 ball-by-ball records
- Seasons covered: 2008 to 2024

---

## Tools Used

- Python 3.8+
- Pandas
- Matplotlib
- Seaborn
- MySQL 8.0
- Microsoft Excel
- Power BI Desktop

---

## Project Structure

```
IPL Performance Analysis/
├── data/
│   ├── matches.csv
│   └── deliveries.csv
├── visuals/
│   ├── 1_team_wins.png
│   ├── 2_toss_impact.png
│   ├── 3_top_batsmen.png
│   ├── 4_top_bowlers.png
│   ├── 5_runs_per_season.png
│   ├── 6_top_venues.png
│   ├── 7_matches_per_season.png
│   └── 8_toss_decision.png
├── analysis.py
├── queries.sql
├── ipl_report.txt
├── ipl_report.xlsx
├── ipl_dashboard.pbix
└── README.md
```

---

## How to Run

Step 1 - Clone the repository
```bash
git clone https://github.com/your-username/ipl-performance-analysis.git
cd ipl-performance-analysis
```

Step 2 - Install required libraries
```bash
pip install pandas numpy matplotlib seaborn openpyxl
```

Step 3 - Download the dataset from Kaggle and place both CSV files inside the data/ folder

Step 4 - Run the main script
```bash
python analysis.py
```

This generates all 8 charts, ipl_report.txt, and ipl_report.xlsx automatically.

---

## Key Findings

- Mumbai Indians are the most successful team with 142 total wins
- V Kohli is the all-time top run scorer with 8,014 runs
- YS Chahal is the leading wicket taker with 205 wickets
- Toss winner goes on to win the match only 50.93% of the time showing toss has minimal impact
- Teams prefer fielding first after winning the toss in recent seasons

---

## Visualizations

| Chart | Insight |
|---|---|
| Team Wins | Top 10 teams by total wins across all seasons |
| Toss Impact | Whether winning the toss leads to winning the match |
| Top Batsmen | Top 10 run scorers in IPL history |
| Top Bowlers | Top 10 wicket takers in IPL history |
| Runs Per Season | Season wise total runs trend |
| Top Venues | Most frequently used venues |
| Matches Per Season | Number of matches played each season |
| Toss Decision | Bat vs field preference after winning toss |

---

## SQL Analysis

The queries.sql file contains 11 sections covering:
- Team win percentage using joins and subqueries
- Toss decision win rate analysis
- Batter strike rate with HAVING clause
- Season wise top scorer using RANK window function
- Bowler economy rate and dot ball percentage
- All-rounder identification using JOIN on aggregated subqueries

---

## Power BI Dashboard

The ipl_dashboard.pbix file contains an interactive dashboard with:
- Team wins bar chart
- Toss impact pie chart
- Top run scorers bar chart
- Runs per season line chart
- Season and team slicers for dynamic filtering

---

## Skills Demonstrated

- Data cleaning and preparation
- Exploratory data analysis
- Data visualization using Matplotlib and Seaborn
- SQL querying with joins, aggregations, subqueries, and window functions
- Excel reporting with multiple structured sheets
- Power BI dashboard creation with interactive slicers
- End-to-end project documentation

---

## Author

Name: Akshay Gundelli

Email: gundelliakshay@gmail.com

LinkedIn: https://linkedin.com/in/gundelli-akshay

GitHub: https://github.com/gundelli-akshay

---

## License

This project is open source under the MIT License.

