from pathlib import Path

import pandas as pd


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    data_dir = root / "data" / "processed" / "revision_v2"
    out_dir = root / "results"
    out_dir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(data_dir / "harmonized_phenotype_data.csv")
    fitness_df = pd.read_csv(data_dir / "fitness_resistance_data.csv")

    complete_case = df[df["log10_FC"].notna()].copy()

    summary = pd.DataFrame(
        [
            {
                "metric": "total_observations",
                "value": int(len(df)),
            },
            {
                "metric": "complete_case_observations",
                "value": int(len(complete_case)),
            },
            {
                "metric": "source_record_count",
                "value": int(df["study_source"].nunique(dropna=True)),
            },
            {
                "metric": "fitness_measurements_n",
                "value": int(fitness_df["Fitness_pct"].notna().sum()),
            },
        ]
    )

    complete_case.to_csv(out_dir / "01_complete_case_dataset.csv", index=False)
    summary.to_csv(out_dir / "01_summary_metrics.csv", index=False)
    print("Saved:", out_dir / "01_complete_case_dataset.csv")
    print("Saved:", out_dir / "01_summary_metrics.csv")


if __name__ == "__main__":
    main()
