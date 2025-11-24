import pandas as pd
import os

def load_data():
    # Hämta mappen där app.py ligger
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Sätt path till data-mappen en nivå upp
    athletes_file = os.path.join(base_dir, "..", "data", "athlete_events.csv")
    noc_file = os.path.join(base_dir, "..", "data", "noc_regions.csv")

    # Läs CSV-filer
    athletes = pd.read_csv(athletes_file)
    noc_regions = pd.read_csv(noc_file)

    # Merge på NOC
    merged = athletes.merge(noc_regions, how="left", on="NOC")

    # --- Förbered data för GBR ---
    gbr = merged[merged["NOC"] == "GBR"].copy()

    medals_per_sport = (
        gbr[gbr["Medal"].notna()]
        .groupby("Sport")["Medal"]
        .count()
        .reset_index(name="Medal_Count")
        .sort_values("Medal_Count", ascending=False)
    )

    medals_per_year = (
        gbr[gbr["Medal"].notna()]
        .groupby("Year")["Medal"]
        .count()
        .reset_index(name="Medal_Count")
        .sort_values("Year")
    )

    age_distribution = gbr[gbr["Age"].notna()]["Age"]

    return merged, {
        "gbr": gbr,
        "medals_per_sport": medals_per_sport,
        "medals_per_year": medals_per_year,
        "age_distribution": age_distribution,
    }
