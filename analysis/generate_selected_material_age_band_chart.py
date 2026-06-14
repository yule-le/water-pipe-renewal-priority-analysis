import os
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", str(Path(__file__).resolve().parents[1] / "analysis" / ".matplotlib"))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
TABLE_PATH = BASE_DIR / "outputs" / "tables"
CHART_PATH = BASE_DIR / "outputs" / "charts"

SOURCE_FILE = TABLE_PATH / "pipe_assets_cleaned.csv"
OUTPUT_TABLE = TABLE_PATH / "pipe_length_by_selected_material_age_band.csv"
OUTPUT_CHART = CHART_PATH / "pipe_length_by_selected_material_age_band.png"

SELECTED_MATERIALS = ["AC", "CI", "PE80", "PE100", "STCL", "Unknown"]
AGE_BAND_ORDER = ["0-20", "21-40", "41-60", "61-80", "80+", "Unknown", "Age data review"]


def assign_age_band(age: float) -> str:
    if pd.isna(age):
        return "Unknown"
    if age > 150:
        return "Age data review"
    if age <= 20:
        return "0-20"
    if age <= 40:
        return "21-40"
    if age <= 60:
        return "41-60"
    if age <= 80:
        return "61-80"
    return "80+"


def main() -> None:
    df = pd.read_csv(SOURCE_FILE)
    df["material_group"] = df["material"].fillna("Unknown")
    df["age_band"] = df["asset_age"].apply(assign_age_band)

    valid_length = df["length_m"].notna() & (df["length_m"] > 0)
    selected_df = df.loc[valid_length & df["material_group"].isin(SELECTED_MATERIALS)].copy()

    summary = (
        selected_df.groupby(["material_group", "age_band"], dropna=False)["length_m"]
        .sum()
        .reset_index(name="total_length_m")
    )
    summary["material_group"] = pd.Categorical(
        summary["material_group"], categories=SELECTED_MATERIALS, ordered=True
    )
    summary["age_band"] = pd.Categorical(
        summary["age_band"], categories=AGE_BAND_ORDER, ordered=True
    )
    summary = summary.sort_values(["material_group", "age_band"]).reset_index(drop=True)
    summary.to_csv(OUTPUT_TABLE, index=False)

    chart_df = (
        summary.pivot(index="material_group", columns="age_band", values="total_length_m")
        .fillna(0)
        .reindex(index=SELECTED_MATERIALS, columns=AGE_BAND_ORDER, fill_value=0)
    )

    ax = chart_df.plot(kind="bar", stacked=True, figsize=(11, 6), colormap="tab20c")
    ax.set_title("Pipe Length by Material and Age Band (Selected Materials)")
    ax.set_xlabel("Material")
    ax.set_ylabel("Total Pipe Length (m)")
    plt.xticks(rotation=0)
    plt.legend(title="Age Band", bbox_to_anchor=(1.02, 1), loc="upper left")
    plt.tight_layout()
    plt.savefig(OUTPUT_CHART, dpi=150)
    plt.close()


if __name__ == "__main__":
    main()
