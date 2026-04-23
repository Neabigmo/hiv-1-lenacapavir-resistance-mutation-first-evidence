from pathlib import Path

import matplotlib
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    data_dir = root / "data" / "processed" / "revision_v2"
    out_dir = root / "results"
    out_dir.mkdir(parents=True, exist_ok=True)

    harmonized = pd.read_csv(data_dir / "harmonized_phenotype_data.csv")
    model_df = pd.read_csv(data_dir / "model_comparison.csv")
    fitness_df = pd.read_csv(data_dir / "fitness_resistance_data.csv")

    fig, axes = plt.subplots(2, 2, figsize=(12, 8), constrained_layout=True)

    mutation_fc = (
        harmonized[harmonized["FC_numeric"].notna()]
        .groupby("Mutation", as_index=False)["FC_numeric"]
        .mean()
        .sort_values("FC_numeric", ascending=False)
        .head(8)
    )
    axes[0, 0].bar(mutation_fc["Mutation"], mutation_fc["FC_numeric"], color="#4c72b0")
    axes[0, 0].set_title("Top Mutation Mean FC")
    axes[0, 0].set_ylabel("Fold-change")
    axes[0, 0].tick_params(axis="x", rotation=45)

    model_plot = model_df[model_df["aic"].notna()].copy()
    axes[0, 1].bar(model_plot["model_name"], model_plot["aic"], color="#dd8452")
    axes[0, 1].set_title("Model AIC Comparison")
    axes[0, 1].set_ylabel("AIC")
    axes[0, 1].tick_params(axis="x", rotation=30)

    q67h_k70r = harmonized[
        (harmonized["Mutation"] == "Q67H+K70R") & harmonized["FC_numeric"].notna()
    ]
    axes[1, 0].scatter(q67h_k70r["study_source"], q67h_k70r["FC_numeric"], color="#55a868")
    axes[1, 0].set_title("Q67H+K70R Context Spread")
    axes[1, 0].set_ylabel("Fold-change")
    axes[1, 0].tick_params(axis="x", rotation=20)

    fitness_plot = fitness_df[
        fitness_df["log10_FC"].notna() & fitness_df["Fitness_pct"].notna()
    ].copy()
    axes[1, 1].scatter(fitness_plot["Fitness_pct"], fitness_plot["log10_FC"], color="#c44e52")
    axes[1, 1].set_title("Fitness vs log10FC (n=6 aggregated)")
    axes[1, 1].set_xlabel("Fitness (% WT)")
    axes[1, 1].set_ylabel("log10 FC")

    figure_png = out_dir / "04_public_core_summary.png"
    figure_pdf = out_dir / "04_public_core_summary.pdf"
    fig.savefig(figure_png, dpi=300)
    fig.savefig(figure_pdf)
    plt.close(fig)

    print("Saved:", figure_png)
    print("Saved:", figure_pdf)


if __name__ == "__main__":
    main()
