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
OUTPUT_TABLE = TABLE_PATH / "selected_material_age_summary.csv"
OUTPUT_CHART = CHART_PATH / "selected_material_median_iqr_age.png"

SELECTED_MATERIALS = ["AC", "CI", "PE80", "PE100", "STCL"]


def main() -> None:
    df = pd.read_csv(SOURCE_FILE)
    df["material_group"] = df["material"].fillna("Unknown")

    age_mask = df["asset_age"].notna() & (df["asset_age"] <= 150)
    material_mask = df["material_group"].isin(SELECTED_MATERIALS)
    summary_df = df.loc[age_mask & material_mask, ["material_group", "asset_age"]].copy()

    summary = (
        summary_df.groupby("material_group")["asset_age"]
        .agg(
            median_asset_age="median",
            p25_asset_age=lambda s: s.quantile(0.25),
            p75_asset_age=lambda s: s.quantile(0.75),
            asset_count="count",
        )
        .reset_index()
    )
    summary["material_group"] = pd.Categorical(
        summary["material_group"], categories=SELECTED_MATERIALS, ordered=True
    )
    summary = summary.sort_values("median_asset_age", ascending=False).reset_index(drop=True)
    summary.to_csv(OUTPUT_TABLE, index=False)

    fig, ax = plt.subplots(figsize=(10, 5.5))
    y_pos = range(len(summary))
    median_vals = summary["median_asset_age"]
    lower_err = median_vals - summary["p25_asset_age"]
    upper_err = summary["p75_asset_age"] - median_vals

    ax.errorbar(
        median_vals,
        list(y_pos),
        xerr=[lower_err, upper_err],
        fmt="o",
        color="#1f5a91",
        ecolor="#8fb3d9",
        elinewidth=3,
        capsize=5,
        markersize=8,
    )

    ax.set_yticks(list(y_pos))
    ax.set_yticklabels(summary["material_group"])
    ax.invert_yaxis()
    ax.set_xlabel("Asset Age (years)")
    ax.set_ylabel("Material")
    ax.set_title("Median Asset Age and IQR by Material")
    ax.grid(axis="x", linestyle="--", alpha=0.35)

    for y, median in zip(y_pos, median_vals):
        ax.text(median + 1.5, y, f"{median:.0f}", va="center", fontsize=9, color="#1f1f1f")

    plt.tight_layout()
    plt.savefig(OUTPUT_CHART, dpi=150)
    plt.close()


if __name__ == "__main__":
    main()
