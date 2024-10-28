import pandas as pd
import os


def export_to_json(data: pd.DataFrame, path: str = "./stock_data"):
    """
    Exports MultiIndex DataFrame to JSON files, one per stock.
    """

    os.makedirs(path, exist_ok=True)

    for stock in data.columns.get_level_values(0).unique():
        os.makedirs(f"{path}/stock_data", exist_ok=True)
        stock_data = data[stock]
        stock_data.to_json(f"{path}/stock_data/{stock}.json", orient="index", indent=4)
