# Risk Transmission Analysis in G7 Financial Markets

## Purpose
This project analyzes **risk transmission dynamics** between the financial markets of G7 countries. By leveraging **Granger causality tests**, it identifies:
- **Risk Transmitters**: Markets that influence others.
- **Risk Absorbers**: Markets heavily influenced by others.

The project visualizes these relationships as a **directed graph**, allowing for a better understanding of inter-market dependencies.

---

## Tools and Techniques

### 1. Data Collection
We used **Yahoo Finance** to fetch historical daily price data for major stock indices representing G7 countries:
- **United States**: S&P 500 (^GSPC)
- **United Kingdom**: FTSE 100 (^FTSE)
- **France**: CAC 40 (^FCHI)
- **Germany**: DAX 40 (^GDAXI)
- **Italy**: FTSE MIB (FTSEMIB.MI)
- **Canada**: S&P/TSX Composite (^GSPTSE)
- **Japan**: Nikkei 225 (^N225)

### 2. Data Preprocessing
- **Log Returns**: Computed daily logarithmic returns to ensure stationarity.
- **Time Zone Alignment**:
  - Shifted **Japan's data by -1 day** to align with European and North American markets.
  - Experimented with shifting **European markets by -1 day** for alignment with North America.
- **Mean Prices**: Tested both close prices and mean prices calculated as `(Open + High + Low + Close) / 4`.

### 3. Granger Causality Analysis
- **Pairwise Tests**:
  - Analyzed causality between all country pairs (source → target).
  - Tested lags from `1 to 5 days`.
- **Thresholds**:
  - P-value < 0.05 for significance.
- Results were stored in `significant_results.csv`, including:
  - Source, Target, Lag, F-statistic, and P-value.

### 4. Visualization
- **Directed Graph**:
  - Nodes represent countries.
  - Edges represent significant Granger causality relationships, with widths proportional to F-statistics.
- **Metrics**:
  - **SDO (Sum of Outgoing F-statistics)**: Measures risk transmission.
  - **SDI (Sum of Incoming F-statistics)**: Measures risk absorption.
- **Graph Filtering**:
  - Removed edges with low F-statistics or insignificant p-values to improve readability.

---

## Difficulties and Solutions

### 1. Time Zone Differences
- **Problem**: Financial markets operate in different time zones, causing misalignment and biased analysis:
  - Japan closes before Europe and North America open.
  - Europe closes before North America closes.
- **Solution**:
  - Shifted Japan's data by **-1 day**.
  - Tested with and without shifting European data.

### 2. Data Availability
- **Problem**: Access to intra-day data was not feasible.
- **Solution**:
  - Focused on daily data .
  - Used close prices as the primary metric and tested mean prices as an alternative (it doesn't work).

### 3. Edge Overlap in Graphs
- **Problem**: Too many edges made graphs unreadable.
- **Solution**:
  - Applied thresholds (`p-value < 0.05`, `F-stat > 10`) to retain only significant edges.


## How to Run the Project

### Prerequisites
1. Python 3.x
2. Required libraries:
   - `yfinance`
   - `numpy`
   - `pandas`
   - `matplotlib`
   - `networkx`
   - `statsmodels`

Install them via:
```bash
pip install yfinance numpy pandas matplotlib networkx statsmodels
