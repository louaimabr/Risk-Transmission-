# Risk Transmission Analysis in G7 Financial Markets
Initially, this project aimed to analyze **risk transmission dynamics** between different sectors (e.g., Tech, Healthcare, Housing). However, to simplify the initial scope, we began by focusing on the financial markets of **G7 countries**. This provided a solid foundation for understanding inter-market dependencies before expanding to sector-specific analysis.

## Purpose
This project analyzes **risk transmission dynamics** between the financial markets of G7 countries. By leveraging **Granger causality tests**, it identifies:
- **Risk Transmitters**: Markets that influence others.
- **Risk Absorbers**: Markets heavily influenced by others.

The project visualizes these relationships as a directed graph, allowing for a better understanding of inter-market dependencies. Additionally, it provides rankings for each country based on cumulative F-statistics for both risk absorption and transmission.
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
- **Daily Price Differences**:
  - The analysis is based on daily price differences: `price[t] - price[t-1]`.
  - This ensures stationarity in the data without applying logarithmic transformations.
- **Time Zone Alignment**:
  - Shifted **Japan's data by -1 day** to align with European and North American markets.
  - Optional **-1 day shift for European markets** to better align with North American close times.

### 3. Granger Causality Analysis
- **Pairwise Tests**:
  - Analyzed causality between all country pairs (source → target).
  - Tested lags from `1 to 5 days`.
- **Thresholds**:
  - P-value < 0.05 for significance.
  - F-statistic > 10 for meaningful causality strength.
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
  - Edges with low F-statistics or insignificant p-values are removed for better readability.

---

## Difficulties and Solutions

### 1. Time Zone Differences
- **Problem**:  
  Financial markets operate in different time zones, causing misalignment:
  - Japan closes before Europe and North America open.
  - Europe closes before North America closes.

- **Solution**:  
  - Shifted **Japan's data by -1 day** to align its closing prices with Europe and North America.
  - Experimented with **shifting European data by -1 day**, testing its impact on causality relationships.
  - This alignment allowed for consistent comparisons between markets and improved the accuracy of the analysis.

---

### 2. Data Availability
- **Problem**:  
  Free access to **intra-day data** was not feasible. Intra-day data would have allowed for more precise alignment of markets, but its high cost posed a challenge.
- **Solution**:  
  - Focused on **daily price differences** as a cost-effective alternative.
  - Conducted experiments with:
    - **Weekly closes prices**. (But we have less data to work on)
    - **Mean prices** using `(Open + High + Low + Close) / 4`.
    - **Volume-Weighted Average Price (VWAP)**.
  - Ultimately settled on **daily close prices**, which were consistent and reliable.

---

### 3. Graph Complexity and Readability
- **Problem**:  
  The Granger causality graph often became cluttered with too many edges, making it difficult to interpret key relationships between countries.

- **Solution**:  
  - Applied strict filtering thresholds:
    - **P-value < 0.05** for statistical significance.
    - **F-statistic > 10** to focus on meaningful relationships.
  - Removed weak or insignificant edges to declutter the graph.
  - Adjusted node sizes and edge widths based on SDI/SDO values and F-statistics, improving visual clarity.

---

### 4. Interpretation of Results
- **Problem**:  
  Rankings of countries (based on SDO/SDI) varied inconsistently during experiments with different shifts and filtering parameters.
- **Solution**:  
  - Standardized preprocessing steps and filtering thresholds to ensure consistency:
    - Fixed the same p-value and F-statistic criteria across all tests.
    - Used consistent shift logic for Japan and European markets.
  - These adjustments ensured repeatability and comparability of results.



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

PS : This project is one of my first ventures into the field of financial market analysis using statistical and programming tools, and there remains significant scope for improvement."
