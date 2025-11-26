import pandas as pd
import os

def load_data():
    # Hämta mappen där app.py ligger
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Sätt path till data-mappen .
    athletes_file = os.path.join(base_dir, "data", "athlete_events.csv")
    noc_file = os.path.join(base_dir, "data", "noc_regions.csv")

    # Läs CSV-filer
    athletes = pd.read_csv(athletes_file)
    noc_regions = pd.read_csv(noc_file)

    # Merge på NOC
    merged = athletes.merge(noc_regions, how="left", on="NOC")

    # GBR DATA
    gbr = merged[merged["NOC"] == "GBR"].copy()

    # Medaljer per sport
    medals_per_sport = (
        gbr[gbr["Medal"].notna()]
        .groupby("Sport")["Medal"]
        .count()
        .reset_index(name="Medal_Count")
        .sort_values("Medal_Count", ascending=False)
    )

    # Medaljer per år
    medals_per_year = (
        gbr[gbr["Medal"].notna()]
        .groupby("Year")["Medal"]
        .count()
        .reset_index(name="Medal_Count")
        .sort_values("Year")
    )

    # Åldersfördelning
    age_distribution = gbr[gbr["Age"].notna()]["Age"]

    # Gender distribution
    gender_distribution = gbr["Sex"].value_counts().reset_index()
    gender_distribution.columns = ["Gender", "Count"]

    # Medal type distribution
    medal_distribution = gbr["Medal"].value_counts().reset_index()
    medal_distribution.columns = ["Medal", "Count"]

    return merged, {
        "gbr": gbr,
        "medals_per_sport": medals_per_sport,
        "medals_per_year": medals_per_year,
        "age_distribution": age_distribution,
        "gender_distribution": gender_distribution,
        "medal_distribution": medal_distribution
    }
