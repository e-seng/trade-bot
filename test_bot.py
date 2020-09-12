#!/usr/bin/env python3

import yfinance as yf
import pandas as pd
import numpy as np
import json

from sys import argv
from collections import OrderedDict
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
        changed by prev_changed (0 if non-existant, [0, inf))
      - avg_rise:
        The average amount the value has risen when the value has historically
        changed by prev_changed (0 if non-existant, [0, inf))
      - max_drop:
        The maximum amount the value has dropped when the value has historically
        changed by prev_changed (0 if non-existant, [0, inf))
      - max_rise:
        The maximum amoun the value has risen by when the value has historically
        changed by prev_changed (0 if non-existant, [0, inf))
      - occurances:
        The dates where prev_change occur, these dates should be in ISO format
        (YYYY-mm-dd)

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

    fieldnames = ["prev_change",
                  "avg_drop",
                  "avg_rise",
                  "max_drop",
                  "max_rise",
                  "occurances"]
    with open(filepath, "+w", newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

def convert_to_dict(keys, values):
    new_dict = {}
    for index, value in enumerate(keys):
        new_dict[value] = values[index]

    return new_dict

def yeet_chars(string, chars=[]):
    for char in chars:
        string = ''.join(string.split(char))

    return string

def parse_date(timestamp):
    return str(timestamp).split(' ')[0]

def handle_data_match(existing_values, update_values):
    date = parse_date(update_values["occurances"][0])
    if(date in existing_values["occurances"]): 
        return existing_values

    n = len(existing_values["occurances"])
    # avg_drop calculations
    drop_sum = float(existing_values["avg_drop"]) * n + update_values["avg_drop"]
    existing_values["avg_drop"] = drop_sum / (n + 1)
    # avg_rise calculations
    rise_sum = float(existing_values["avg_rise"]) * n + update_values["avg_rise"]
    existing_values["avg_rise"] = rise_sum / (n + 1)
    # max_drop
    if(update_values["max_drop"] > float(existing_values["max_drop"])):
        existing_values["max_drop"] = update_values["max_drop"]
    # max_rise
    if(update_values["max_rise"] > float(existing_values["max_rise"])):
        existing_values["max_rise"] = update_values["max_rise"]
    # occurances
    occurances = yeet_chars(existing_values["occurances"], ['\'', '"', '[', ']', ' ']).split(",")
    occurances.append(date)
    existing_values["occurances"] = occurances

    return existing_values

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
        "avg_rise", "max-drop", "max-rise", in this order
    """
    filename = f"sd-{stock_ticker.lower()}.csv"
    folderpath = os.path.join(rootdir, "data")
    filepath = os.path.join(folderpath, filename)

    if not os.path.isfile(filepath): init_stock_data(stock_ticker, rootdir)

    fieldnames = ["prev_change",
                  "avg_drop",
                  "avg_rise",
                  "max_drop",
                  "max_rise",
                  "occurances"]

    existing_data = []
    with open(filepath, "r", newline='') as file:
        for line in csv.reader(file):
            existing_line = convert_to_dict(fieldnames, line)
            existing_data.append(existing_line)

    index = 1 # Start by seeing if the value is 
    while(index <= len(existing_data)):
        if type(data_line["occurances"][0]) != str:
            date = parse_date(data_line["occurances"][0])
            data_line["occurances"][0] = date

        if(index == len(existing_data)):
            existing_data.append(data_line)
            break

        prev_change = float(existing_data[index]["prev_change"])
        if(prev_change < float(data_line["prev_change"])):
            index += 1
            continue

        if(prev_change == float(data_line["prev_change"])):
            new_data = handle_data_match(existing_data[index], data_line) ##
            existing_data[index] = new_data
            break

        existing_data.insert(index, data_line)
        break

    with open(filepath, "w", newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        for dl in existing_data:
            writer.writerow(dl)

def collect_stock_data(stock_ticker, start_date, end_date=None):
    """
    Collects the stock data starting at a desired date over a period of time
    (default) or until a specified end date.

    This will look at each day's stock and calculate the amount the stock has 
    changed by between the previous day and the selected day. These change
    records are then saved in a csv using the save_stock_data function.

    Stock data will be collected between each day, so technically datapoints are
    collected between the first of the start_month to the start of the end month
    (exclusive). There will be missing data points, but as general trends are
    being collected, it doesn't really matter too too much...

    @params:
      - stock_ticker {str}:
        The Ticker of the desired public stock
      - start_month {int}:
        The numerical representation of the starting date, in ISO format
        (YYYY-mm-dd)
      - end_month? {int}:
        The numberical representation of the ending date, in ISO format
        (YYYY-mm-dd), defaults to None so it will parse until the current day
    """
    ticker = yf.Ticker(stock_ticker)
    history = ticker.history(start=start_date, end=end_date)
    dates = history.index
    for index, current_stock in enumerate(history["Close"]):
        if(index + 1 >= len(history["Close"])): break
        if(index == 0): continue
        current_date = dates[index]
        prev_change = current_stock - history["Close"][index - 1]
        change = history["Close"][index + 1] - current_stock
        change_type = "rise" # Either rise or drop

        if(change < 0):
            change_type = "drop"
            change *= -1

        sd = {"prev_change" : prev_change,
              "avg_drop" : 0,
              "avg_rise" : 0,
              "max_drop" : 0,
              "max_rise" : 0,
              "occurances" : [current_date]}
        
        sd[f"max_{change_type}"] = change
        sd[f"avg_{change_type}"] = change

        save_stock_data(stock_ticker, sd)
    return

def main():
    tsla = yf.Ticker("TSLA")
    print(tsla.info)

if __name__ == "__main__": main()