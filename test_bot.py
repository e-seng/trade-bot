#!/usr/bin/env python3

import yfinance as yf

from sys import argv

def main():
    tsla = yf.Ticker("TSLA")
    print(tsla.info)

if __name__ == "__main__": main()