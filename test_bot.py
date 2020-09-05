#!/usr/bin/env python3

import yfinance as yf
import pandas as pd
import numpy as np

from sys import argv

def main():
    tsla = yf.Ticker("TSLA")
    print(tsla.info)

if __name__ == "__main__": main()