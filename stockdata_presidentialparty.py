# Looks at presidential party data (republican or democrat) over the past years
# and determines if there is any correlation between party and stock market trends.
# For example, does the stock market go up when the president is republican?
# Additionally breaks data into different sectors (Healthcare, Energy, Basic Industry)
# to see if certain sectors do better or worse for different parties

import pandas as pd
import matplotlib.pyplot as plt
from math import *
import datetime as dt
import numpy as np
from collections import defaultdict

# Date selection
start_date = '19800101'
end_date = '20180101'

# Load raw data, containing day-by-day stock prices of random subset of all
# companies.
data = pd.read_csv('stocks-us-adjClose.csv', parse_dates=True, index_col=0)

# Get custom dates for data set
data = data.loc[start_date:end_date]

# Drop empty datapoints from our data.
data.dropna()


#######HELPER FUNCTIONS#################
# "19700101" -> "Jan, 1970"
def prettyDate(rawDate):
   monthStrings = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec']
   month = int(rawDate[4:6])
   year = rawDate[:4]
   return monthStrings[month-1] + ', ' + year

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
#######HELPER FUNCTIONS#################

def analyzeData(data, plotTitle):

    # Resample data points, grabbing the last price of each month.
    month_data = data.resample('M').first()

    # Calculate monthly percent change: Feb28 = (Feb28 - Jan31)/Jan31
    pct = month_data.pct_change()
    # Calculate the average percent change (across all stocks)
    average_pct = pct.mean(axis=1)
    average_pct = average_pct[average_pct < 0.5]

    # presidential data
    pres_data = pd.read_csv('pres_party_by_month.csv', parse_dates=True, index_col=0)

    pres_data = pres_data.loc[start_date:end_date]


    # Bin our data based on month and political party
    month_labels = ['jan','feb','mar','apr','may','june','july','aug','sept','oct','nov','dec']
    binned_months = [[],[],[],[],[],[],[],[],[],[],[],[]]
    dem_binned_months = [[],[],[],[],[],[],[],[],[],[],[],[]]
    rep_binned_months = [[],[],[],[],[],[],[],[],[],[],[],[]]
    dem_to_rep_binned = [[],[],[],[],[],[],[],[],[],[],[],[]]
    rep_to_dem_binned = [[],[],[],[],[],[],[],[],[],[],[],[]]
    for index, line in enumerate(average_pct):
        if pres_data.iloc[index,0] == 'republican':
            rep_binned_months[index % 12].append(line)
        else:
            dem_binned_months[index % 12].append(line)
        if pres_data.iloc[index,1] == 1:
            dem_to_rep_binned[index % 12].append(line)       
        if pres_data.iloc[index,1] == 2:
            rep_to_dem_binned[index % 12].append(line)
        binned_months[index % 12].append(line)


    # Average each of our monthly bins.

    def get_averages(binned_data):
        month_averages = []
        for month in binned_data:
            month_averages.append(np.nanmean(month))
        return month_averages

    def get_stds(binned_data):
        month_stds = []
        for month in binned_data:
            month_stds.append(np.nanstd(month)/sqrt(len(month)))   # udpating to be the standard error instead of standard deviation
        return month_stds



    month_averages = get_averages(binned_months)
    dem_month_averages = get_averages(dem_binned_months)
    rep_month_averages = get_averages(rep_binned_months)

    month_stds = get_stds(binned_months)
    dem_month_stds = get_stds(dem_binned_months)
    rep_month_stds = get_stds(rep_binned_months)


    # Transitions
    dem_to_rep_averages = get_averages(dem_to_rep_binned)
    rep_to_dem_averages = get_averages(rep_to_dem_binned)

    dem_to_rep_stds = get_stds(dem_to_rep_binned)
    rep_to_dem_stds = get_stds(rep_to_dem_binned)
    


    # Convert monthly averages to data frames.
    df_month_averages = pd.Series(month_averages,index=month_labels,name = 'month averages')
    df_dem_month_averages = pd.Series(dem_month_averages,index=month_labels,name = 'democratic months')
    df_rep_month_averages = pd.Series(rep_month_averages,index=month_labels,name = 'republican months')
    df_dem_month_stds = pd.Series(dem_month_stds,index=month_labels,name = 'democratic months')
    df_rep_month_stds = pd.Series(rep_month_stds,index=month_labels,name = 'republican months')
    df_dem_to_rep_averages = pd.Series(dem_to_rep_averages,index=month_labels,name = 'dem to rep')
    df_rep_to_dem_averages = pd.Series(rep_to_dem_averages,index=month_labels,name = 'rep to dem')
    df_dem_to_rep_stds = pd.Series(dem_to_rep_stds,index=month_labels,name = 'dem to rep')
    df_rep_to_dem_stds = pd.Series(rep_to_dem_stds,index=month_labels,name = 'rep to dem')

   
    df_dem_to_rep_averages = df_dem_to_rep_averages.dropna()
    df_rep_to_dem_averages = df_rep_to_dem_averages.dropna()
    df_dem_to_rep_stds = df_dem_to_rep_stds.dropna()
    df_rep_to_dem_stds = df_rep_to_dem_stds.dropna()


    combined_averages = pd.concat([df_dem_month_averages,
                                df_rep_month_averages],
                               axis=1)

    combined_stds = pd.concat([df_dem_month_stds,
                                df_rep_month_stds],
                               axis=1)

    combined_averages2 = pd.concat([df_dem_to_rep_averages,
                                df_rep_to_dem_averages],
                               axis=1)

    combined_stds2 = pd.concat([df_dem_to_rep_stds,
                                df_rep_to_dem_stds],
                               axis=1)


    combined_averages = combined_averages[combined_averages['democratic months'] < 0.5]
    combined_averages = combined_averages[combined_averages['republican months'] < 0.5]
    combined_stds = combined_stds[combined_averages['democratic months'] < 0.5]
    combined_stds = combined_stds[combined_averages['republican months'] < 0.5]

    combined_averages2 = combined_averages2[combined_averages2['dem to rep'] < 0.5]
    combined_averages2 = combined_averages2[combined_averages2['rep to dem'] < 0.5]
    combined_stds2 = combined_stds2[combined_averages2['dem to rep'] < 0.5]
    combined_stds2 = combined_stds2[combined_averages2['rep to dem'] < 0.5]


    #Plotting
    fig, axes = plt.subplots(nrows=2, ncols=1)
    fig.canvas.set_window_title(plotTitle)
    
    combined_averages2.plot(kind='bar',color=['b','r'],yerr=combined_stds2,ax=axes[0],label=plotTitle)
    axes[0].set_title(plotTitle + '\nData from %s to %s'%(prettyDate(start_date), prettyDate(end_date)))
    axes[0].set_xlabel('Month')
    axes[0].set_ylabel('Average Percent Change (1.00 = 100%)')
    plt.legend()

    average_pct.plot.hist(bins=100,ax=axes[1],label='Histogram')
    axes[1].set_title('Histogram')
    axes[1].set_xlabel('Percent Change (1.00 = 100%)')

    
    fig.subplots_adjust(hspace=1)


# Data for sectors taken from CSV files on: http://www.nasdaq.com/screening/industries.aspx

analyzeData(data, 'All Data')
analyzeData(getSectorData(data, 'healthcaresector.csv'), 'Healthcare Sector')
analyzeData(getSectorData(data, 'energysector.csv'), 'Energy Sector')
analyzeData(getSectorData(data, 'basicindustriessector.csv'), 'Basic Industries')

plt.show()
