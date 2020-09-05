#!/usr/bin/env python3

import yfinance as yf
import pandas as pd
import numpy as np

from sys import argv
import os
import csv

def init_stock_data(stock_ticker, rootdir="."):
    """
    Initializes the stock data csv for a given stock.
    This will produce a csv the appropreate headers for the stock history.

    This file will be saved within, unless otherwise specified, the root
    directory in the data folder. Filenames will follow the format of
    sd-<stock ticker name, in lower case>.csv

    @params 
      - stock_ticker {str} The ticker for the desired stock
      - filepath? {str} The filepath to store this data, defaults to the
        root directory
    """
    filename = f"sd-{stock_ticker}.csv"
    filepath = os.path.join(rootdir, "data", filename)

    fieldnames = ["prev-rise-amnt", "avg_drop", "avg_rise", "max-drop", "max-rise"]
    with open(filepath, "a+", newline='') as file:
        pass

def main():
    tsla = yf.Ticker("TSLA")
    print(tsla.info)

if __name__ == "__main__": main()