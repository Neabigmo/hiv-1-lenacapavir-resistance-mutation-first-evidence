from pathlib import Path

import pandas as pd


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    data_dir = root / "data" / "processed" / "revision_v2"
    out_dir = root / "results"
    out_dir.mkdir(parents=True, exist_ok=True)

    harmonized = pd.read_csv(data_dir / "harmonized_phenotype_data.csv")
    epistasis = pd.read_csv(data_dir / "epistasis_matrix.csv")

    q67h_k70r = harmonized[
        (harmonized["Mutation"] == "Q67H+K70R") & harmonized["FC_numeric"].notna()
    ].copy()

    min_fc = float(q67h_k70r["FC_numeric"].min())
    max_fc = float(q67h_k70r["FC_numeric"].max())
    fold_range = max_fc / min_fc if min_fc > 0 else float("nan")
    source_records = ";".join(sorted(q67h_k70r["study_source"].dropna().unique().tolist()))

    q67h_n74d = epistasis[epistasis["combination"] == "Q67H+N74D"].iloc[0]

    summary = pd.DataFrame(
        [
            {
                "metric": "Q67H+K70R_min_fc",
                "value": min_fc,
                "source_records": source_records,
            },
            {
                "metric": "Q67H+K70R_max_fc",
                "value": max_fc,
                "source_records": source_records,
            },
            {
                "metric": "Q67H+K70R_fold_range",
                "value": fold_range,
                "source_records": source_records,
            },
            {
                "metric": "Q67H+N74D_interaction_residual_log10",
                "value": float(q67h_n74d["interaction_residual"]),
                "source_records": "PMC9600929",
            },
        ]
    )

    summary.to_csv(out_dir / "03_epistasis_context_summary.csv", index=False)
    q67h_k70r.to_csv(out_dir / "03_q67h_k70r_records.csv", index=False)
    print("Saved:", out_dir / "03_epistasis_context_summary.csv")
    print("Saved:", out_dir / "03_q67h_k70r_records.csv")


if __name__ == "__main__":
    main()
