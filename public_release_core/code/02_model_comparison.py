from pathlib import Path

import pandas as pd


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    data_dir = root / "data" / "processed" / "revision_v2"
    out_dir = root / "results"
    out_dir.mkdir(parents=True, exist_ok=True)

    model_df = pd.read_csv(data_dir / "model_comparison.csv")

    model_df["aic"] = pd.to_numeric(model_df["aic"], errors="coerce")
    model_df["bic"] = pd.to_numeric(model_df["bic"], errors="coerce")
    model_df["r_squared"] = pd.to_numeric(model_df["r_squared"], errors="coerce")

    ranked = model_df[model_df["aic"].notna()].sort_values("aic").copy()
    ranked["aic_rank"] = range(1, len(ranked) + 1)

    best_row = ranked.iloc[0]
    summary = pd.DataFrame(
        [
            {
                "best_model": best_row["model_name"],
                "best_aic": float(best_row["aic"]),
                "best_bic": float(best_row["bic"]),
                "best_r_squared": float(best_row["r_squared"]),
            }
        ]
    )

    ranked.to_csv(out_dir / "02_model_ranking.csv", index=False)
    summary.to_csv(out_dir / "02_model_best_summary.csv", index=False)
    print("Saved:", out_dir / "02_model_ranking.csv")
    print("Saved:", out_dir / "02_model_best_summary.csv")


if __name__ == "__main__":
    main()
