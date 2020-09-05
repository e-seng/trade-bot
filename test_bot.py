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

    @params 
      - stock_ticker {str} The ticker for the desired stock
      - filepath? {str} The filepath to store this data, defaults to the
        root directory
    """
    filename = f"sd-{stock_ticker}.csv"
    filepath = os.path.join(rootdir, "data", filename)

    with open(filepath, "wb+", newline='') as file:
        pass

def main():
    tsla = yf.Ticker("TSLA")
    print(tsla.info)

if __name__ == "__main__": main()