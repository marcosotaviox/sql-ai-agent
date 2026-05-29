"""
data/seed_db.py
================
Seeds the SQLite database with ABS-style Australian Labour Force data.
Run once: python data/seed_db.py
"""

import sqlite3
import random
import pandas as pd
from pathlib import Path

DB_PATH = Path(__file__).parent / "abs_labour.db"


def seed():
    conn = sqlite3.connect(DB_PATH)

    states = ["NSW", "VIC", "QLD", "WA", "SA", "TAS", "ACT", "NT"]
    industries = [
        "Healthcare & Social Assistance",
        "Construction",
        "Retail Trade",
        "Professional Services",
        "Education & Training",
        "Mining",
        "Manufacturing",
        "Accommodation & Food Services",
    ]
    quarters = [
        "2022-Q1", "2022-Q2", "2022-Q3", "2022-Q4",
        "2023-Q1", "2023-Q2", "2023-Q3", "2023-Q4",
        "2024-Q1", "2024-Q2",
    ]

    random.seed(42)

    # --- Table 1: labour_force ---
    base_employment = {
        "NSW": 4200, "VIC": 3600, "QLD": 2800, "WA": 1800,
        "SA": 900, "TAS": 280, "ACT": 320, "NT": 140,
    }
    base_unemployment = {
        "NSW": 3.8, "VIC": 4.1, "QLD": 4.5, "WA": 3.9,
        "SA": 5.2, "TAS": 5.8, "ACT": 3.1, "NT": 4.9,
    }

    labour_data = []
    for quarter in quarters:
        for state in states:
            for industry in industries:
                q_idx = quarters.index(quarter)
                growth = 1 + (q_idx * 0.003)
                employed = int(
                    base_employment[state] * growth * random.uniform(0.08, 0.22)
                )
                unemp_rate = round(
                    base_unemployment[state] + random.uniform(-0.5, 0.5), 1
                )
                participation = round(random.uniform(64.0, 68.5), 1)
                labour_data.append({
                    "quarter": quarter,
                    "state": state,
                    "industry": industry,
                    "employed_thousands": employed,
                    "unemployment_rate": unemp_rate,
                    "participation_rate": participation,
                })

    pd.DataFrame(labour_data).to_sql("labour_force", conn, if_exists="replace", index=False)
    print(f"  ✓ labour_force: {len(labour_data)} rows")

    # --- Table 2: wage_growth ---
    wage_data = []
    for quarter in quarters:
        for industry in industries:
            q_idx = quarters.index(quarter)
            base_index = 100 + (q_idx * 0.9)
            wage_data.append({
                "quarter": quarter,
                "industry": industry,
                "wage_price_index": round(base_index + random.uniform(-0.3, 0.8), 1),
                "annual_growth_pct": round(random.uniform(2.5, 5.8), 2),
            })

    pd.DataFrame(wage_data).to_sql("wage_growth", conn, if_exists="replace", index=False)
    print(f"  ✓ wage_growth: {len(wage_data)} rows")

    # --- Table 3: state_population ---
    base_pop = {
        "NSW": 8153, "VIC": 6694, "QLD": 5322, "WA": 2785,
        "SA": 1820, "TAS": 571, "ACT": 461, "NT": 250,
    }
    pop_data = []
    for year in [2022, 2023, 2024]:
        for state in states:
            pop = int(base_pop[state] * (1 + (year - 2022) * 0.015))
            pop_data.append({
                "year": year,
                "state": state,
                "population_thousands": pop,
                "interstate_migration_net": random.randint(-5000, 15000),
                "overseas_migration_net": random.randint(2000, 45000),
            })

    pd.DataFrame(pop_data).to_sql("state_population", conn, if_exists="replace", index=False)
    print(f"  ✓ state_population: {len(pop_data)} rows")

    conn.close()
    print(f"\nDatabase created at: {DB_PATH}")


if __name__ == "__main__":
    print("Seeding ABS Labour Force database...")
    seed()