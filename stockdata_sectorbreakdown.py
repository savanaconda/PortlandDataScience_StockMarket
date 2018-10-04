import pandas as pd
import matplotlib.pyplot as plt
from math import *
import datetime as dt
import numpy as np
from collections import defaultdict

# Date selection
start_date = '20070101'
end_date = '20180101'

# Load raw data, containing day-by-day stock prices of random subset of all
# companies.
data = pd.read_csv('stocks-us-adjClose.csv', parse_dates=True, index_col=0)

# Get custom dates for data set
data = data.loc[start_date:end_date]


# Drop empty datapoints from our data.
data.dropna()

# Return new dataframe containing only the selected symbols.
def filterBySymbol(data, symbols):
    return data[symbols].copy()

# Returns the intersection of two lists.
def intersection(a, b):
    intersect = []
    for val in a:
        if val in b:
            intersect.append(val)
    return intersect

# Grab a list of ticker symbols from a file.
def grabSymbolsFromFile(file_name):
    d = pd.read_csv(file_name, parse_dates=True, index_col=0)
    return d.index.values

# Gets the data for only the sector specified in file
def getSectorData(data, file_name):  
    rawDataSymbols = data.columns.values
    symbolsFromFile = grabSymbolsFromFile(file_name)
    sectorData = filterBySymbol(data, intersection(rawDataSymbols, symbolsFromFile))
    return sectorData

healthcareData = getSectorData(data, 'healthcaresector.csv')

print(healthcareData)

print(type(healthcareData))




