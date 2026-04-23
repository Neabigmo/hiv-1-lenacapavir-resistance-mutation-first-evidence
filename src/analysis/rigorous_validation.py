import pandas as pd
import numpy as np
import pickle
from sklearn.metrics import mean_squared_error, mean_absolute_error
from statsmodels.regression.mixed_linear_model import MixedLM

def leave_one_study_out_cv(df):
    """Leave-one-study-out cross-validation"""
    results = []
    studies = df['Source'].unique()

    for study in studies:
        train = df[df['Source'] != study]
        test = df[df['Source'] == study]

        if len(train) < 10 or len(test) == 0:
            continue

        model = MixedLM.from_formula(
            'LogFC ~ Mutation',
            data=train,
            groups=train['Backbone']
        )
        fitted = model.fit(reml=True)

        for _, row in test.iterrows():
            mut = row['Mutation']
            if mut in fitted.fe_params.index:
                pred = fitted.fe_params['Intercept'] + fitted.fe_params[mut]
            else:
                pred = fitted.fe_params['Intercept']

            results.append({
                'Study': study,
                'True': row['LogFC'],
                'Pred': pred,
                'Mutation': mut
            })

    res_df = pd.DataFrame(results)
    rmse = np.sqrt(mean_squared_error(res_df['True'], res_df['Pred']))
    mae = mean_absolute_error(res_df['True'], res_df['Pred'])

    return res_df, rmse, mae

def leave_one_backbone_out_cv(df):
    """Leave-one-backbone-out cross-validation"""
    results = []
    backbones = df['Backbone'].unique()

    for bb in backbones:
        train = df[df['Backbone'] != bb]
        test = df[df['Backbone'] == bb]

        if len(train) < 10 or len(test) == 0:
            continue

        model = MixedLM.from_formula(
            'LogFC ~ Mutation',
            data=train,
            groups=train['Backbone']
        )
        fitted = model.fit(reml=True)

        for _, row in test.iterrows():
            mut = row['Mutation']
            if mut in fitted.fe_params.index:
                pred = fitted.fe_params['Intercept'] + fitted.fe_params[mut]
            else:
                pred = fitted.fe_params['Intercept']

            results.append({
                'Backbone': bb,
                'True': row['LogFC'],
                'Pred': pred,
                'Mutation': mut
            })

    res_df = pd.DataFrame(results)
    rmse = np.sqrt(mean_squared_error(res_df['True'], res_df['Pred']))
    mae = mean_absolute_error(res_df['True'], res_df['Pred'])

    return res_df, rmse, mae

def leave_one_mutation_combination_out_cv(df):
    """Leave-one-mutation-combination-out CV for complex mutations"""
    results = []
    complex_muts = df[df['Mutation'].str.contains(r'\+', regex=True)]['Mutation'].unique()

    for mut in complex_muts:
        train = df[df['Mutation'] != mut]
        test = df[df['Mutation'] == mut]

        if len(train) < 10 or len(test) == 0:
            continue

        model = MixedLM.from_formula(
            'LogFC ~ Mutation',
            data=train,
            groups=train['Backbone']
        )
        fitted = model.fit(reml=True)

        pred = fitted.fe_params['Intercept']

        for _, row in test.iterrows():
            results.append({
                'Mutation': mut,
                'True': row['LogFC'],
                'Pred': pred,
                'Extrapolation': True
            })

    res_df = pd.DataFrame(results)
    if len(res_df) > 0:
        rmse = np.sqrt(mean_squared_error(res_df['True'], res_df['Pred']))
        mae = mean_absolute_error(res_df['True'], res_df['Pred'])
    else:
        rmse, mae = np.nan, np.nan

    return res_df, rmse, mae

if __name__ == '__main__':
    df = pd.read_csv('data/curated/phenotype_unified.csv')
    df = df[df['FC_numeric'].notna() & df['Subtype'].notna()].copy()
    df['LogFC'] = np.log10(df['FC_numeric'])
    df['Backbone'] = df['Subtype'].fillna('Unknown')
    df['Source'] = df['Source_PMID'].fillna('Unknown')

    print("Leave-one-study-out CV...")
    study_res, study_rmse, study_mae = leave_one_study_out_cv(df)
    study_res.to_csv('results/validation/leave_one_study_out.csv', index=False)
    print(f"RMSE: {study_rmse:.3f}, MAE: {study_mae:.3f}")

    print("\nLeave-one-backbone-out CV...")
    bb_res, bb_rmse, bb_mae = leave_one_backbone_out_cv(df)
    bb_res.to_csv('results/validation/leave_one_backbone_out.csv', index=False)
    print(f"RMSE: {bb_rmse:.3f}, MAE: {bb_mae:.3f}")

    print("\nLeave-one-mutation-combination-out CV...")
    mut_res, mut_rmse, mut_mae = leave_one_mutation_combination_out_cv(df)
    mut_res.to_csv('results/validation/leave_one_mutation_combination_out.csv', index=False)
    print(f"RMSE: {mut_rmse:.3f}, MAE: {mut_mae:.3f}")

    with open('results/validation/rigorous_cv_summary.txt', 'w') as f:
        f.write(f"Leave-one-study-out: RMSE={study_rmse:.3f}, MAE={study_mae:.3f}\n")
        f.write(f"Leave-one-backbone-out: RMSE={bb_rmse:.3f}, MAE={bb_mae:.3f}\n")
        f.write(f"Leave-one-mutation-combination-out: RMSE={mut_rmse:.3f}, MAE={mut_mae:.3f}\n")
