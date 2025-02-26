# granger_causality.py
import pandas as pd
from statsmodels.tsa.stattools import grangercausalitytests

def granger_causality():
    """
    Reads the log-returns from 'aligned_data.csv', performs Granger causality tests
    between each pair of countries, and records significant results (p-value < 0.05)
    in 'significant_results.csv'.
    """
    data = pd.read_csv("aligned_data.csv", index_col=0, parse_dates=True)
    results_list = []
    columns = data.columns

    for predictor in columns:
        for target in columns:
            if predictor == target:
                continue

            pair_data = data[[target, predictor]].dropna()
            if len(pair_data) < 10:
                continue

            test_results = grangercausalitytests(pair_data, maxlag=5, verbose=False)
            
            best_lag = None
            best_fstat = float("-inf")
            best_pvalue = 1.0

            for lag in range(1, 6):
                f_stat = test_results[lag][0]["ssr_ftest"][0]
                p_value = test_results[lag][0]["ssr_ftest"][1]
                if f_stat > best_fstat:
                    best_fstat = f_stat
                    best_pvalue = p_value
                    best_lag = lag

            if best_pvalue < 0.05:
                results_list.append({
                    "Source": predictor,
                    "Target": target,
                    "Lag": best_lag,
                    "F-statistic": best_fstat,
                    "p-value": best_pvalue
                })

    df_results = pd.DataFrame(results_list)
    df_results.to_csv("significant_results.csv", index=False)
    print("Granger causality results have been saved in 'significant_results.csv'")
