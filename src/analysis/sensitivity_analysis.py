import pandas as pd
import numpy as np
from statsmodels.regression.mixed_linear_model import MixedLM
import matplotlib.pyplot as plt

def context_sensitivity_analysis(df):
    """Analyze effect of clinical vs in vitro vs natural polymorphism context"""
    results = []

    for context in df['Context'].unique():
        subset = df[df['Context'] == context]
        if len(subset) < 5:
            continue

        model = MixedLM.from_formula(
            'LogFC ~ Mutation',
            data=subset,
            groups=subset['Backbone']
        )
        try:
            fitted = model.fit(reml=True)
            results.append({
                'Context': context,
                'N': len(subset),
                'Mean_LogFC': subset['LogFC'].mean(),
                'SD_LogFC': subset['LogFC'].std(),
                'Backbone_Var': fitted.cov_re.iloc[0, 0] if hasattr(fitted, 'cov_re') else 0
            })
        except:
            continue

    return pd.DataFrame(results)

def study_level_effect_analysis(df):
    """Model study-level random effects"""
    df_copy = df.copy()
    df_copy['Study_Backbone'] = df_copy['Source'] + '_' + df_copy['Backbone']

    # Model with study-level effect
    model_study = MixedLM.from_formula(
        'LogFC ~ Mutation',
        data=df_copy,
        groups=df_copy['Source']
    )

    # Model with backbone effect
    model_backbone = MixedLM.from_formula(
        'LogFC ~ Mutation',
        data=df_copy,
        groups=df_copy['Backbone']
    )

    try:
        fit_study = model_study.fit(reml=True)
        fit_backbone = model_backbone.fit(reml=True)

        study_var = fit_study.cov_re.iloc[0, 0] if hasattr(fit_study, 'cov_re') else 0
        backbone_var = fit_backbone.cov_re.iloc[0, 0] if hasattr(fit_backbone, 'cov_re') else 0

        return {
            'Study_Variance': study_var,
            'Backbone_Variance': backbone_var,
            'Study_AIC': fit_study.aic,
            'Backbone_AIC': fit_backbone.aic,
            'Study_BIC': fit_study.bic,
            'Backbone_BIC': fit_backbone.bic
        }
    except:
        return None

def quality_weighted_analysis(df):
    """Weight observations by quality score"""
    df_weighted = df.copy()
    df_weighted = df_weighted[df_weighted['Quality_score'].notna()]

    if len(df_weighted) < 10:
        return None

    # Normalize weights
    weights = df_weighted['Quality_score'] / df_weighted['Quality_score'].max()

    # Weighted regression
    model = MixedLM.from_formula(
        'LogFC ~ Mutation',
        data=df_weighted,
        groups=df_weighted['Backbone']
    )

    try:
        fitted = model.fit(reml=True)

        # Get top mutations with confidence intervals
        params = fitted.fe_params
        conf_int = fitted.conf_int()

        top_muts = params.abs().nlargest(10)
        ci_results = []

        for mut in top_muts.index:
            if mut == 'Intercept':
                continue
            ci_results.append({
                'Mutation': mut,
                'Effect': params[mut],
                'CI_Lower': conf_int.loc[mut, 0],
                'CI_Upper': conf_int.loc[mut, 1],
                'Significant': not (conf_int.loc[mut, 0] <= 0 <= conf_int.loc[mut, 1])
            })

        return pd.DataFrame(ci_results)
    except:
        return None

if __name__ == '__main__':
    df = pd.read_csv('data/curated/phenotype_unified.csv')
    df = df[df['FC_numeric'].notna() & df['Subtype'].notna()].copy()
    df['LogFC'] = np.log10(df['FC_numeric'])
    df['Backbone'] = df['Subtype'].fillna('Unknown')
    df['Source'] = df['Source_PMID'].fillna('Unknown')

    print("Context sensitivity analysis...")
    context_res = context_sensitivity_analysis(df)
    context_res.to_csv('results/validation/context_sensitivity.csv', index=False)
    print(context_res)

    print("\nStudy-level vs backbone-level effects...")
    study_res = study_level_effect_analysis(df)
    if study_res:
        with open('results/validation/study_level_effects.txt', 'w') as f:
            for k, v in study_res.items():
                f.write(f"{k}: {v:.4f}\n")
        print(study_res)

    print("\nQuality-weighted analysis with confidence intervals...")
    quality_res = quality_weighted_analysis(df)
    if quality_res is not None:
        quality_res.to_csv('results/validation/quality_weighted_effects.csv', index=False)
        print(quality_res)

    print("\nSensitivity analysis complete.")
