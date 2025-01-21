# main.py
from store import store_data
from ganger_causality import granger_causality
from graph import graph
import warnings

# Suppress specific warnings
warnings.filterwarnings("ignore", category=FutureWarning)

if __name__ == "__main__":
    start_date = "2000-01-01"
    end_date = "2020-12-31"

    # 1. Fetch data & store aligned log-returns
    #store_data("2000-01-01", "2020-12-31", shift_europe=False)

    # 2. Perform Granger causality tests
    granger_causality()

    # 3. Build and visualize the network
    graph()
