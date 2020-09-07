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

    The csv will contain the following headers:
      - prev_changed:
        The amount has risen or has fallen for the stock
      - avg_drop:
        The average amount the value has dropped when the value has historically
        changed by prev_changed (0 if non-existant)
      - avg_rise:
        The average amount the value has risen when the value has historically
        changed by prev_changed (0 if non-existant)
      - max_drop:
        The maximum amount the value has dropped when the value has historically
        changed by prev_changed (0 if non-existant)
      - min_rise:
        The maximum amoun the value has risen by when the value has historically
        changed by prev_changed (0 if non-existant)

    @params 
      - stock_ticker {str}:
        The ticker for the desired stock
      - filepath? {str}:
        The filepath to store this data, defaults to the current directory
    """
    filename = f"sd-{stock_ticker.lower()}.csv"
    folderpath = os.path.join(rootdir, "data")
    filepath = os.path.join(folderpath, filename)

    if os.path.isfile(filepath):
        print("Attempted to initialize existing stock data file, skipping")
        return

    try:
        os.mkdir(folderpath)
    except FileExistsError:
        pass

    fieldnames = ["prev_change", "avg_drop", "avg_rise", "max-drop", "max-rise"]
    with open(filepath, "+w", newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

def save_stock_data(stock_ticker, data_line, rootdir="."):
    """
    Saves a line of stock data in ascending numeric order.
    This order is based off the Closed value provided within the data line.

    @params:
      - stock_ticker {str}:
        The ticker of the desired stock.
      - data_line {dict}:
        The line of data to be inserted into the stock data file. This
        dictionary contains the fieldnames "prev_change", "avg_drop",
        "avg_rise", "max-drop", "max-rise".
    """
    filename = f"sd-{stock_ticker.lower()}.csv"
    folderpath = os.path.join(rootdir, "data")
    filepath = os.path.join(folderpath, filename)
    return

def main():
    tsla = yf.Ticker("TSLA")
    print(tsla.info)

if __name__ == "__main__": main()